# Introduction to Programming Fundamentals

A practical guide to the building blocks that all programming languages share. This isn't about mastering a specific language — it's about understanding how programs think.

---

## The Universal Pattern

Every program in every language follows the same pattern:

```
INPUT -> ALGORITHM -> OUTPUT
```

- **Input**: data coming in (user typing, a file, a database query, a sensor reading)
- **Algorithm**: the steps you take to process that data
- **Output**: the result (a screen display, a saved file, a response to a user)

That's it. Every program — from a calculator to a video game to a banking system — is just a variation of this pattern.

---

## Part 1: Algorithms — The Steps

An **algorithm** is just a set of instructions. You already use algorithms daily:

> *"If it's raining, take an umbrella. Otherwise, wear sunglasses."*

That's an algorithm. Programming is writing these instructions in a language a computer can follow.

### 1.1 Conditionals (Making Decisions)

Conditionals let a program choose what to do based on a condition.

```python
temperature = 30

if temperature > 25:
    print("It's hot outside")
elif temperature > 15:
    print("It's mild outside")
else:
    print("It's cold outside")
```

**Key concept**: the program only runs ONE of these paths. It checks each condition top-to-bottom and takes the first one that's true.

**Common comparison operators** (same across almost all languages):

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | equals | `x == 5` |
| `!=` | not equals | `x != 5` |
| `>` | greater than | `x > 5` |
| `<` | less than | `x < 5` |
| `>=` | greater or equal | `x >= 5` |
| `<=` | less or equal | `x <= 5` |

**Combining conditions**:

```python
age = 25
has_license = True

if age >= 16 and has_license:
    print("You can drive")

if age < 16 or not has_license:
    print("You cannot drive")
```

- `and` — both must be true
- `or` — at least one must be true
- `not` — flips true to false (and vice versa)

### 1.2 Loops (Repeating Things)

Loops run the same code multiple times. Without loops, you'd have to write the same line hundreds of times.

**For loop** — when you know how many times:

```python
# Print numbers 1 through 5
for i in range(1, 6):
    print(i)
```

Output: `1 2 3 4 5`

**While loop** — when you don't know how many times:

```python
# Keep asking until they say "quit"
answer = ""
while answer != "quit":
    answer = input("Type 'quit' to exit: ")

print("Goodbye!")
```

**Looping through a list**:

```python
names = ["Alice", "Bob", "Charlie"]

for name in names:
    print("Hello, " + name)
```

Output:
```
Hello, Alice
Hello, Bob
Hello, Charlie
```

**Watch out**: an infinite loop happens when the condition never becomes false. The program runs forever (or until you force-stop it).

```python
# DON'T DO THIS - infinite loop
while True:
    print("This never stops")
```

### 1.3 Operations (Doing Math and Logic)

**Arithmetic** (works the same in virtually every language):

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | add | `5 + 3` | `8` |
| `-` | subtract | `5 - 3` | `2` |
| `*` | multiply | `5 * 3` | `15` |
| `/` | divide | `5 / 3` | `1.666...` |
| `//` | integer divide | `5 // 3` | `1` |
| `%` | remainder (modulo) | `5 % 3` | `2` |

**String operations** (text manipulation):

```python
first = "Hello"
last = "World"

# Concatenation (joining strings)
greeting = first + " " + last    # "Hello World"

# Length
length = len(greeting)            # 11

# Uppercase / lowercase
upper = greeting.upper()          # "HELLO WORLD"
lower = greeting.lower()          # "hello world"

# Checking content
has_hello = "Hello" in greeting   # True
```

---

## Part 2: Data — What Programs Work With

Programs need to store and organize information. There are a few fundamental ways to do this, and they're the same across all languages (just with slightly different syntax).

### 2.1 Variables (Single Values)

A variable is a named container for a value. Think of it as a labeled box.

```python
name = "Alice"          # text (called a "string")
age = 30                # whole number (called an "integer")
height = 5.6            # decimal number (called a "float")
is_active = True        # true/false (called a "boolean")
```

**Key concept**: variables can change (that's why they're called "variables"):

```python
score = 0
score = score + 10      # score is now 10
score = score + 5       # score is now 15
```

**Data types matter**:

```python
# This is math
result = 5 + 3          # 8

# This is string concatenation
result = "5" + "3"      # "53"
```

The same `+` operator does different things depending on the data type. `5` (number) and `"5"` (text) are different things to a computer.

### 2.2 Arrays / Lists (Multiple Values)

An array (called a "list" in Python) holds multiple values in order.

```python
colors = ["red", "green", "blue"]

# Access by position (starts at 0, not 1!)
first = colors[0]       # "red"
second = colors[1]      # "green"
last = colors[-1]       # "blue" (negative counts from end)

# Modify
colors[0] = "yellow"    # replace "red" with "yellow"

# Add / remove
colors.append("purple") # add to end
colors.remove("green")  # remove by value

# How many?
count = len(colors)      # 3
```

**Why start at 0?** Nearly all programming languages count from 0, not 1. This is a universal convention — just something you get used to.

### 2.3 Dictionaries / Maps (Key-Value Pairs)

A dictionary maps names to values. Like a real dictionary maps words to definitions.

```python
car = {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2024,
    "electric": False
}

# Access by key
print(car["make"])       # "Toyota"
print(car["year"])       # 2024

# Add / modify
car["color"] = "blue"    # add new key
car["year"] = 2025       # update existing

# Check if key exists
if "color" in car:
    print(car["color"])
```

**This is one of the most important data structures in programming.** JSON (the format used by web APIs, config files, and databases) is essentially nested dictionaries:

```python
person = {
    "name": "Alice",
    "age": 30,
    "address": {
        "city": "Toronto",
        "country": "Canada"
    },
    "hobbies": ["reading", "hiking", "coding"]
}

# Nested access
city = person["address"]["city"]        # "Toronto"
first_hobby = person["hobbies"][0]      # "reading"
```

### 2.4 None / Null (The Absence of Value)

Every language has a concept for "no value" — not zero, not empty, but *nothing*.

```python
result = None

if result is None:
    print("No result yet")
```

This matters because:
- `0` is a value (the number zero)
- `""` is a value (an empty string)
- `None` is the absence of any value

---

## Part 3: Wrappers — Organizing Code

As programs grow, you need ways to organize code into reusable pieces. Two fundamental concepts handle this.

### 3.1 Functions (Reusable Actions)

A function is a named block of code you can call whenever you need it. Instead of copying the same code everywhere, you write it once and call it by name.

```python
def greet(name):
    return "Hello, " + name + "!"

# Use it multiple times
message1 = greet("Alice")     # "Hello, Alice!"
message2 = greet("Bob")       # "Hello, Bob!"
```

**Parts of a function**:
- **Name**: `greet` — what you call it
- **Parameters**: `name` — inputs it accepts
- **Body**: the code inside — what it does
- **Return value**: what it gives back

**Functions can take multiple parameters**:

```python
def calculate_tax(price, tax_rate):
    tax = price * tax_rate
    return price + tax

total = calculate_tax(100, 0.13)    # 113.0
```

**Functions can call other functions**:

```python
def is_adult(age):
    return age >= 18

def can_vote(age, is_citizen):
    return is_adult(age) and is_citizen

print(can_vote(25, True))     # True
print(can_vote(15, True))     # False
```

**Why functions matter**: without them, a 1000-line program is one giant block of code. With them, it's 50 small, understandable pieces that you can test and reuse independently.

### 3.2 Classes (Blueprints for Things)

A class groups data and functions together into a single concept. Think of it as a blueprint — the class describes what something looks like, and you create individual instances from it.

```python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0

    def accelerate(self, amount):
        self.speed = self.speed + amount

    def brake(self):
        self.speed = 0

    def describe(self):
        return self.make + " " + self.model + " (" + str(self.year) + ")"

# Create instances
my_car = Car("Toyota", "Corolla", 2024)
your_car = Car("Honda", "Civic", 2023)

# Use them
my_car.accelerate(60)
print(my_car.describe())    # "Toyota Corolla (2024)"
print(my_car.speed)         # 60

your_car.accelerate(80)
print(your_car.speed)       # 80
print(my_car.speed)         # still 60 — they're independent
```

**Key concepts**:
- `__init__` is the constructor — runs when you create a new instance
- `self` refers to the specific instance (my_car vs your_car)
- **Properties** (`self.make`, `self.speed`) are the data
- **Methods** (`accelerate`, `brake`) are the functions

**You don't always need classes.** Many programs work perfectly with just functions and data structures. Classes are useful when you're modeling real-world things with both data and behavior.

---

## Part 4: Putting It Together

Here's a small but complete program using everything above:

```python
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)

def get_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

# INPUT
students = {
    "Alice": [95, 87, 92],
    "Bob": [78, 85, 72],
    "Charlie": [60, 55, 68]
}

# ALGORITHM + OUTPUT
for name, scores in students.items():
    avg = calculate_average(scores)
    grade = get_grade(avg)
    print(name + ": average " + str(round(avg, 1)) + " = " + grade)
```

Output:
```
Alice: average 91.3 = A
Bob: average 78.3 = C
Charlie: average 61.0 = D
```

Notice the pattern: **Input** (student data) -> **Algorithm** (calculate averages, determine grades) -> **Output** (print results).

---

## Part 5: SQL — Talking to Databases

SQL (Structured Query Language) is a different kind of language. It's **declarative** — you describe *what* you want, not *how* to get it. The database figures out the "how."

### 5.1 The Basics: Tables and Rows

A database is just organized tables — like spreadsheets:

**`employees` table:**

| id | name | department | salary | hire_date |
|----|------|-----------|--------|-----------|
| 1 | Alice | Engineering | 95000 | 2020-03-15 |
| 2 | Bob | Marketing | 72000 | 2019-07-01 |
| 3 | Charlie | Engineering | 88000 | 2021-01-10 |
| 4 | Diana | Marketing | 78000 | 2022-06-20 |

### 5.2 SELECT — Reading Data

```sql
-- Get everything
SELECT * FROM employees;

-- Get specific columns
SELECT name, salary FROM employees;

-- Get one row
SELECT * FROM employees WHERE id = 1;
```

### 5.3 WHERE — Filtering

```sql
-- Simple filter
SELECT * FROM employees WHERE department = 'Engineering';

-- Multiple conditions
SELECT * FROM employees WHERE department = 'Engineering' AND salary > 90000;

-- Pattern matching
SELECT * FROM employees WHERE name LIKE 'A%';    -- starts with A
SELECT * FROM employees WHERE name LIKE '%li%';  -- contains "li"

-- List matching
SELECT * FROM employees WHERE department IN ('Engineering', 'Marketing');

-- Null checks
SELECT * FROM employees WHERE hire_date IS NOT NULL;
```

### 5.4 ORDER BY and LIMIT — Sorting and Paging

```sql
-- Sort by salary, highest first
SELECT * FROM employees ORDER BY salary DESC;

-- Sort ascending (default)
SELECT * FROM employees ORDER BY name ASC;

-- Get top 3 earners
SELECT * FROM employees ORDER BY salary DESC LIMIT 3;

-- Pagination: skip 10, get next 10
SELECT * FROM employees ORDER BY name LIMIT 10 OFFSET 10;
```

### 5.5 Aggregate Functions — Summarizing Data

```sql
-- Count rows
SELECT COUNT(*) FROM employees;                           -- 4

-- Sum, average, min, max
SELECT SUM(salary) FROM employees;                        -- 333000
SELECT AVG(salary) FROM employees;                        -- 83250
SELECT MIN(salary) FROM employees;                        -- 72000
SELECT MAX(salary) FROM employees;                        -- 95000

-- Group by a column
SELECT department, COUNT(*) as headcount, AVG(salary) as avg_salary
FROM employees
GROUP BY department;
```

Result:

| department | headcount | avg_salary |
|-----------|-----------|------------|
| Engineering | 2 | 91500 |
| Marketing | 2 | 75000 |

### 5.6 JOIN — Combining Tables

Most databases have multiple related tables. JOINs combine them.

**`departments` table:**

| id | name | budget |
|----|------|--------|
| 1 | Engineering | 500000 |
| 2 | Marketing | 300000 |

```sql
-- Combine employee data with department data
SELECT e.name, e.salary, d.name as department, d.budget
FROM employees e
JOIN departments d ON e.department = d.name;
```

Result:

| name | salary | department | budget |
|------|--------|-----------|--------|
| Alice | 95000 | Engineering | 500000 |
| Bob | 72000 | Marketing | 300000 |
| Charlie | 88000 | Engineering | 500000 |
| Diana | 78000 | Marketing | 300000 |

**Types of JOINs**:
- `JOIN` (or `INNER JOIN`) — only rows that match in BOTH tables
- `LEFT JOIN` — all rows from the left table, matching rows from the right (NULL if no match)
- `RIGHT JOIN` — all rows from the right table, matching rows from the left

```sql
-- LEFT JOIN: show all employees even if department doesn't exist in departments table
SELECT e.name, d.budget
FROM employees e
LEFT JOIN departments d ON e.department = d.name;
```

### 5.7 CASE — Conditional Logic in SQL

CASE is SQL's version of if/elif/else:

```sql
SELECT name, salary,
    CASE
        WHEN salary >= 90000 THEN 'Senior'
        WHEN salary >= 75000 THEN 'Mid'
        ELSE 'Junior'
    END as level
FROM employees;
```

Result:

| name | salary | level |
|------|--------|-------|
| Alice | 95000 | Senior |
| Bob | 72000 | Junior |
| Charlie | 88000 | Mid |
| Diana | 78000 | Mid |

### 5.8 INSERT, UPDATE, DELETE — Modifying Data

```sql
-- Add a new row
INSERT INTO employees (name, department, salary, hire_date)
VALUES ('Eve', 'Engineering', 82000, '2024-01-15');

-- Update existing rows
UPDATE employees SET salary = 80000 WHERE name = 'Bob';

-- Delete rows
DELETE FROM employees WHERE name = 'Eve';
```

**Be careful with UPDATE and DELETE** — without a WHERE clause, they affect ALL rows:

```sql
-- THIS DELETES EVERYTHING (no WHERE clause!)
DELETE FROM employees;

-- Always use WHERE to target specific rows
DELETE FROM employees WHERE id = 5;
```

### 5.9 Subqueries — Queries Inside Queries

```sql
-- Find employees earning above average
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Find departments with more than 1 employee
SELECT department
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```

### 5.10 How SQL Differs from Programming Languages

| Aspect | Programming (Python, etc.) | SQL |
|--------|---------------------------|-----|
| Approach | Imperative: you describe *how* | Declarative: you describe *what* |
| Flow | Step by step, line by line | One statement, database decides execution order |
| Loops | You write explicit loops | The database loops internally (you just say WHERE/JOIN) |
| Data | In memory (variables) | On disk (tables) |
| State | Variables change over time | Each query is independent (stateless) |

SQL is powerful because you don't write the algorithm — the database has already optimized algorithms for searching, sorting, and joining. You just describe what you want.

---

## Part 6: General Concepts Worth Knowing

### 6.1 Comments

Every language lets you add notes that the computer ignores:

```python
# This is a comment in Python
x = 5  # This explains what x is for
```

```sql
-- This is a comment in SQL
SELECT * FROM employees;  -- Get all employees
```

Comments are for humans reading the code later (including your future self).

### 6.2 Error Handling

Programs can fail — files might not exist, users might enter garbage, networks might be down. Good programs handle errors gracefully:

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number
    print("Result:", result)
except ValueError:
    print("That's not a valid number")
except ZeroDivisionError:
    print("Can't divide by zero")
```

Without error handling, the program would crash. With it, the user gets a helpful message.

### 6.3 Scope

Variables exist only within the block where they're created:

```python
def my_function():
    x = 10          # x only exists inside this function
    print(x)        # works: 10

my_function()
print(x)            # ERROR: x doesn't exist out here
```

This is called **scope** — it prevents variables in one part of a program from accidentally interfering with another part.

### 6.4 Indentation and Syntax

Every language has rules about formatting. Python uses indentation to define code blocks:

```python
if True:
    print("This is inside the if")
    print("This too")
print("This is outside the if")
```

Other languages (JavaScript, PHP, Java, C) use curly braces `{}` instead:

```javascript
if (true) {
    console.log("This is inside the if");
    console.log("This too");
}
console.log("This is outside the if");
```

Different syntax, same concept. Once you understand one language's patterns, others are mostly just different punctuation.

### 6.5 APIs — Programs Talking to Programs

An API (Application Programming Interface) is how programs communicate. When a website loads weather data, your phone gets notifications, or a payment processes — APIs are making it happen.

Most modern APIs use HTTP (the same protocol as websites) with JSON data:

```
Request:  GET https://api.example.com/weather?city=Toronto
Response: {"temperature": 22, "condition": "sunny", "humidity": 45}
```

The requesting program sends a URL with parameters, the API returns structured data. The requesting program then uses that data however it needs to.

### 6.6 Debugging — Finding and Fixing Problems

When code doesn't work, you debug it. The simplest technique: **print statements**.

```python
def calculate_discount(price, discount):
    print("Price:", price)          # What did we receive?
    print("Discount:", discount)    # What did we receive?
    result = price * discount       # Bug: should be price * (1 - discount)
    print("Result:", result)        # What did we calculate?
    return result

# Expected: 80 (20% off $100)
# Actual: 20 (oops)
calculate_discount(100, 0.20)
```

By printing intermediate values, you can see exactly where the logic goes wrong. Professional tools (debuggers) do this more elegantly, but print statements work everywhere.

---

## Quick Reference

### The Building Blocks (Every Language Has These)

| Concept | What It Does | Example |
|---------|-------------|---------|
| Variable | Stores a value | `x = 5` |
| Conditional | Makes decisions | `if x > 0:` |
| Loop | Repeats code | `for item in list:` |
| Function | Reusable code block | `def greet(name):` |
| Array/List | Ordered collection | `[1, 2, 3]` |
| Dictionary/Map | Key-value pairs | `{"name": "Alice"}` |
| Class | Blueprint for objects | `class Car:` |
| Comment | Note for humans | `# this is ignored` |
| Error handling | Graceful failure | `try: ... except:` |

### SQL Quick Reference

| Operation | SQL | Purpose |
|-----------|-----|---------|
| Read | `SELECT ... FROM` | Get data |
| Filter | `WHERE` | Narrow results |
| Sort | `ORDER BY` | Arrange results |
| Limit | `LIMIT` / `OFFSET` | Pagination |
| Count/Sum | `COUNT()` / `SUM()` / `AVG()` | Aggregate |
| Group | `GROUP BY` | Summarize by category |
| Combine tables | `JOIN ... ON` | Link related data |
| Conditional | `CASE WHEN ... THEN` | Logic in queries |
| Create | `INSERT INTO` | Add rows |
| Modify | `UPDATE ... SET` | Change rows |
| Remove | `DELETE FROM` | Remove rows |

---

## What Next?

This document covers the **foundations** — the concepts that don't change between languages. Once you're comfortable with these, the next steps are:

1. **Pick a language and build something small** — a calculator, a to-do list, a simple quiz
2. **Learn to read documentation** — every language and tool has docs; learning to navigate them is a core skill
3. **Understand version control (Git)** — how teams track and collaborate on code changes
4. **Explore web basics** — HTML (structure), CSS (styling), JavaScript (interactivity)
5. **Practice SQL with real data** — set up a small database and query it

The best way to learn programming is by doing — reading about it only gets you so far. Write code, break things, fix them, repeat.
