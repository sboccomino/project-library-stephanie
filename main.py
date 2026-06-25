import functions_framework
import re


# =============================================================================
# CONFIGURATION  (named constants instead of "magic strings" buried in the code)
#
# README Part 2.1 (Variables): a variable is a named box for a value. Putting
# these at the top — in ONE place — means if the table name or a language code
# ever changes, you edit it here once instead of hunting through the file.
# =============================================================================

# The fully-qualified BigQuery table: "project.dataset.table".
# README Part 5.1 explains tables; this is the one we INSERT into (Part 5.8).
# Its real schema (4 columns, all REQUIRED):
#     page_number      INTEGER   the page's number
#     page_text        STRING    Portuguese text from Vision (OCR)
#     translated_text  STRING    English text from Translate
#     validated        BOOLEAN   has a human checked it yet?
BQ_TABLE = "library-stephanie.book_translation.scanned_pages"

# Language codes for the Translation API (README Part 6.5 — APIs).
SOURCE_LANGUAGE = "pt-BR"   # Brazilian Portuguese (what the book is written in)
TARGET_LANGUAGE = "en-CA"   # Canadian English (what we want back)

# SAFEGUARD (filtering): we only want to OCR actual images. A bucket can receive
# all sorts of files (a stray .txt, a .DS_Store, a half-uploaded temp file). If
# we blindly ran Vision on every upload we'd waste paid API calls — or crash —
# on files that were never pages. README Part 1.1 (Conditionals): we use this
# list to make a yes/no decision before doing any expensive work.
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".bmp", ".webp")


# =============================================================================
# Cloud Function entry point.
#
# This function is triggered automatically every time a new file lands in the
# Cloud Storage bucket (the "file creation / finalization" event). Google
# hands us a `cloud_event` describing the upload, and we kick off the recipe
# from pseudo.txt.
#
# IMPORTANT — why this function is written so defensively:
# Cloud Storage events are delivered "at least once". That means Google may
# call this function MORE THAN ONCE for the same uploaded file — normally if
# our code raised an error last time, but sometimes just because the delivery
# system retried on its own. Our recipe calls TWO paid APIs (Vision, then
# Translate) BEFORE it saves anything. So a function that crashes part-way
# through gets retried... which re-runs those paid APIs... which can loop and
# burn money. The safeguards below (Steps 0a, 0b, and the try/except in
# README Part 6.2 style) exist specifically to stop that loop.
# =============================================================================
@functions_framework.cloud_event
def main(cloud_event):
    # The cloud_event object is everything Google tells us about the upload.
    # `event_data` is the part that describes the file itself. (We name it
    # `event_data` rather than `data` so it can't be confused with the BigQuery
    # row dictionary we build later — README Part 6.3, Scope: two different
    # things should have two different names.)
    event_data = cloud_event.data

    event_id = cloud_event["id"]       # a unique id for THIS delivery attempt
    event_type = cloud_event["type"]   # e.g. "google.cloud.storage.object.v1.finalized"

    bucket = event_data["bucket"]            # e.g. "my-book-pages"
    name = event_data["name"]                # e.g. "chapter-01/page-001.jpg"
    metageneration = event_data["metageneration"]
    timeCreated = event_data["timeCreated"]
    updated = event_data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    # -------------------------------------------------------------------------
    # Step 0a — SAFEGUARD: ignore files that aren't page images.
    # See pseudo.txt step 0a. README Part 1.1 (Conditionals) + 1.3 (the `in`/
    # string check). `.lower()` so "PAGE-001.JPG" matches too.
    #
    # `return` here means "stop, nothing to do, and report success" — which
    # tells Google the event is handled so it WON'T be retried.
    # -------------------------------------------------------------------------
    if not name.lower().endswith(IMAGE_EXTENSIONS):
        print(f"Skipping '{name}' — not an image file. Nothing to do.")
        return

    # -------------------------------------------------------------------------
    # Step 0b — work out the page number (an INTEGER, because that is the column
    # type in BigQuery). See pseudo.txt step 0b. The file name is a STRING like
    # "chapter-01/page-001.jpg", so we pull the page digits out of it and turn
    # them into a number. README Part 1.3 (string operations) + Part 2.1 (the
    # string -> integer type conversion).
    #
    # If we can't find a page number we can't build a valid row (the column is
    # REQUIRED), so we skip rather than crash-loop.
    # -------------------------------------------------------------------------
    page_number = page_number_from_name(name)
    if page_number is None:
        print(f"Skipping '{name}' — couldn't read a page number from the file name.")
        return

    # -------------------------------------------------------------------------
    # Step 0c — SAFEGUARD: idempotency check ("have we already done this one?").
    # See pseudo.txt step 0c.
    #
    # "Idempotent" means: running it twice has the same effect as running it
    # once. Because events can be delivered more than once, we ask BigQuery
    # whether this page is ALREADY saved. If it is, we skip — no Vision call,
    # no Translate call, no duplicate row. This is the main thing that stops
    # the same file being processed (and paid for) over and over.
    #
    # NOTE (a real limitation to be aware of): the table's only identifier is
    # `page_number`, so two different files that share a number — e.g.
    # chapter-01/page-001 and chapter-02/page-001 both become page 1 — look
    # identical to this check. See the question in pseudo.txt step 3 about
    # adding a file_name column if the book has repeating page numbers.
    # -------------------------------------------------------------------------
    if already_processed(page_number):
        print(f"Page {page_number} is already in BigQuery. Skipping to avoid duplicate work.")
        return

    # -------------------------------------------------------------------------
    # The recipe itself (pseudo.txt steps 1-3), wrapped in error handling.
    # README Part 6.2 (Error Handling): if any step fails, we want to log it
    # clearly and STOP — not crash in a way that makes Google retry the whole
    # paid pipeline. So we catch the error here instead of letting it escape.
    # -------------------------------------------------------------------------
    try:
        # Step 1 — SCAN: convert image to text using the Vision API.
        # See pseudo.txt step 1. portuguese_text is pt_BR (Brazilian Portuguese).
        portuguese_text = detect_text(bucket, name)
        print(f"Extracted page text ({len(portuguese_text)} characters):")
        print(portuguese_text)

        # Step 2 — TRANSLATE: Portuguese -> English via the Translation API.
        # See pseudo.txt step 2. If the page was blank, portuguese_text is "" and
        # translate() simply returns "" — we still save a row (below) so this
        # blank page is marked done and never reprocessed. ("" is fine for a
        # REQUIRED column: REQUIRED means "not missing", and "" is not missing.)
        english_text = translate(portuguese_text)
        print(f"Translated text:")
        print(english_text)

        # Step 3 — STORE: save original + translated text to BigQuery.
        # See pseudo.txt step 3. README Part 2.3 (Dictionaries): this dict is one
        # row, and its KEYS are exactly the four table column names. README
        # Part 2.4: `validated=False` marks the row "not yet checked by a human",
        # ready for the Step 4 review.
        row = {
            "page_number": page_number,         # INTEGER — the page's number
            "page_text": portuguese_text,       # STRING  — Portuguese, from Vision
            "translated_text": english_text,    # STRING  — English, from Translate
            "validated": False,                 # BOOLEAN — human hasn't verified it yet
        }

        saveToBQ(row)

    except Exception as error:
        # README Part 6.2 — graceful failure. We log everything we know and then
        # DO NOT re-raise. Returning normally tells Google "handled, don't
        # retry", which is what stops the re-trigger / re-bill loop.
        #
        # Trade-off worth knowing: this also means a *temporary* glitch (e.g. a
        # one-second network blip) won't be auto-retried — this run is simply
        # marked done. For this project that's the safe default, because an
        # unbounded retry that keeps calling Vision + Translate is far more
        # costly than occasionally re-uploading one page by hand. If you later
        # WANT automatic retries for transient errors only, you'd `raise` here
        # for those specific error types and `return` for the permanent ones.
        print(f"ERROR while processing '{name}' (event {event_id}): {error}")
        print("Giving up on this event so it is NOT retried. Re-upload the file "
              "to try again once the cause is fixed.")
        return


# =============================================================================
# Step 0b helper — turn a file name into an integer page number.
#
# Input:  the file name (e.g. "chapter-01/page-001.jpg")
# Output: the page number as an int (e.g. 1), or None if we can't find one
#
# README Part 3.1 (Functions): pulled into its own small function so main()
# stays readable and this fiddly text-parsing lives in one place.
# =============================================================================
def page_number_from_name(name):
    """Extract the page number (int) from a file name, or None if absent."""
    # Look at just the file part, dropping any "folder/" in front, so the digits
    # in "chapter-01" don't get mistaken for the page number.
    basename = name.rsplit("/", 1)[-1]      # "chapter-01/page-001.jpg" -> "page-001.jpg"

    # re.findall(r"\d+", ...) returns every run of digits it finds, in order.
    # For "page-001.jpg" that's ["001"]; we take the LAST group as the page.
    digit_groups = re.findall(r"\d+", basename)
    if not digit_groups:
        return None

    # int("001") -> 1. README Part 2.1: converting a STRING of digits into a
    # real INTEGER, which is what the BigQuery column needs.
    return int(digit_groups[-1])


# =============================================================================
# Step 0c helper — has this page already been saved?  (idempotency check)
#
# Input:  the page number (int)
# Output: True if a row for that page already exists in BigQuery, else False
#
# README Part 5.2/5.3 (SELECT ... WHERE) + 5.5 (COUNT). README Part 3.1: we put
# this in its own function so main() reads as one clear sentence ("if already
# processed, skip") and the database details live down here.
# =============================================================================
def already_processed(page_number):
    """Return True if BigQuery already has a row for this page number."""
    from google.cloud import bigquery

    client = bigquery.Client()

    # README Part 5.9 hints at this: we ask the database to COUNT matching rows.
    # The `@page_number` is a *query parameter*, not the value pasted straight
    # into the text. This is the safe way to put a value into SQL — it avoids
    # the classic "SQL injection" bug where crafted input could change what the
    # query does.
    query = f"""
        SELECT COUNT(*) AS match_count
        FROM `{BQ_TABLE}`
        WHERE page_number = @page_number
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("page_number", "INT64", page_number),
        ]
    )

    try:
        results = client.query(query, job_config=job_config).result()
        # `results` is a list of rows; we asked for one number, so read row 0.
        match_count = list(results)[0].match_count
        return match_count > 0
    except Exception as error:
        # If the *check itself* fails (e.g. the table doesn't exist yet), we
        # "fail open": assume not-yet-processed and let the recipe run. The
        # try/except in main() is still there to catch any later problem, so we
        # don't risk turning a check failure into a crash loop.
        print(f"Could not run the idempotency check ({error}); processing anyway.")
        return False


# =============================================================================
# Step 1 — SCAN
#
# Input:  the storage bucket name + the file name of the page image
# Output: a single string containing all the text on that page (Portuguese)
#
# This function follows pseudo.txt step 1 letter-by-letter. The comments
# below mark which sub-step (a.i, a.ii, b.iii, ...) each block of code is.
# =============================================================================
def detect_text(bucket, name):
    """Run Vision API OCR on a Cloud Storage image and return the text."""
    from google.cloud import vision

    # a.i / a.ii — `bucket` and `name` were passed in from the cloud_event
    #              above, so we already have them.
    # a.iii      — build the Vision API "filename" as a gs:// URI. The
    #              gs:// prefix tells Vision to read the file directly out
    #              of Cloud Storage; we don't have to download it ourselves.
    gcs_uri = f"gs://{bucket}/{name}"
    print(f"Vision API source: {gcs_uri}")

    # b.i — create the Vision client. Inside a Cloud Run function, the
    #       authentication is handled automatically by the function's
    #       attached service account (no API keys to manage).
    client = vision.ImageAnnotatorClient()

    # b.ii — build a Vision Image object that points at the GCS URI.
    image = vision.Image()
    image.source.image_uri = gcs_uri

    # b.iii — call OCR ("text detection") on the image and get the response.
    response = client.text_detection(image=image)

    # b.iv — if Vision reports an error, stop here and raise. The try/except in
    #        main() will catch it, log it, and stop the event (no retry loop).
    if response.error.message:
        raise Exception(
            f"{response.error.message}\n"
            "For more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    # c.i — `text_annotations` is a list of detected text regions.
    texts = response.text_annotations

    # c.iv — if the page was blank (or Vision found no readable text),
    #        return an empty string so step 2 can decide what to do.
    if not texts:
        print("No text detected on page")
        return ""

    # c.ii / c.iii — the FIRST entry holds the full page text combined.
    #                The remaining entries are individual words/lines with
    #                bounding-box coordinates — useful for highlighting on
    #                the original image, but we don't need them here.
    page_text = texts[0].description

    # d — return the OCR'd text so step 2 (translation) can use it.
    return page_text


# =============================================================================
# Step 2 — TRANSLATE
#
# Input:  the Portuguese text from step 1
# Output: the same text translated into English
#
# See pseudo.txt step 2. README Part 3.1: `destination_language` is a parameter
# with a DEFAULT value, so callers can just write translate(text) and get
# English, or override the target language when they need to.
# =============================================================================
def translate(page_text, destination_language=TARGET_LANGUAGE):
    """Translate Portuguese text to English using the Translation API."""
    from google.cloud import translate_v2 as translate

    # A blank page from step 1 has nothing to translate. Returning "" early
    # skips a pointless (paid) API call. README Part 1.1 (Conditionals).
    if not page_text:
        return ""

    translate_client = translate.Client()
    result = translate_client.translate(
        page_text,
        source_language=SOURCE_LANGUAGE,
        target_language=destination_language,
    )
    # README Part 2.3 — the API hands back a dictionary; we pull out the one
    # key we care about, "translatedText".
    return result["translatedText"]


# =============================================================================
# Step 3 — STORE
#
# Input:  one `row` dictionary (built in main) whose keys match the table columns
# Output: that row appended as a new record in the BigQuery table
#
# See pseudo.txt step 3. README Part 5.8 (INSERT) is the SQL idea here; the
# BigQuery client library does the insert for us from the dictionary.
# =============================================================================
def saveToBQ(row):
    """Append one page-translation row to the BigQuery table."""
    from google.cloud import bigquery

    client = bigquery.Client()

    # `load_table_from_json` accepts a LIST of rows; we have exactly one.
    rows_to_insert = [row]

    # We spell out the schema explicitly so the columns and their types are
    # unambiguous, and so a typo or a wrong type in the `row` dict fails loudly
    # HERE (with a clear message) instead of writing to the wrong place. These
    # names + types + REQUIRED modes match the real table exactly — that match
    # is what the old code got wrong (it put the STRING file name into the
    # INTEGER page_number column, which BigQuery rejected every time).
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # add, don't overwrite
        schema=[
            bigquery.SchemaField("page_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("page_text", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("translated_text", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("validated", "BOOLEAN", mode="REQUIRED"),
        ],
    )

    # Trigger the write and WAIT for it to finish. `.result()` blocks until the
    # load job completes; if BigQuery rejected the data it raises here, and the
    # `load_job.errors` list (logged below) explains exactly which column or
    # value it didn't like.
    load_job = client.load_table_from_json(rows_to_insert, BQ_TABLE, job_config=job_config)
    try:
        load_job.result()
    except Exception as error:
        # Surface BigQuery's per-row reasons, which are far more specific than
        # the generic exception message, then re-raise so main()'s handler logs
        # it and stops the event.
        print(f"BigQuery load failed: {error}")
        print(f"BigQuery details: {load_job.errors}")
        raise

    print(f"Successfully loaded {load_job.output_rows} row(s) for page {row['page_number']}.")
