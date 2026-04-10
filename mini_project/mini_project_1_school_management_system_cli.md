# Mini Project: Smart Student Management System (CLI)

## Overview

Build a Command Line Application (CLI) to manage student records.
This project will help you apply Python concepts like functions, file handling, regex, and modules.

---

## Objectives

* Work with functions and modular code
* Handle data using JSON files
* Validate inputs using regex
* Use loops and conditions effectively
* Build a real-world mini application

---

## Project Structure

```
student_app/
 ├── main.py
 ├── utils.py
 ├── file_handler.py
 ├── data.json
```

---

## Features

### 1. Menu System

Create a menu:

```
1. Add Student
2. View Students
3. Search Student
4. Update Marks
5. Exit
```

* Use while loop
* Use break to exit

---

### 2. Add Student

Input:

* Name
* Age
* Email
* Marks (multiple values)

Requirements:

* Store data as dictionary
* Save to JSON file

---

### 3. Email Validation (Regex)

Use pattern:

```
\w+@\w+\.\w+
```

* Show error if invalid

---

### 4. File Handling (JSON)

* Use json.load() and json.dump()
* Store data like:

```
[
  {
    "name": "Anbu",
    "age": 22,
    "email": "test@gmail.com",
    "marks": [80, 90, 70]
  }
]
```

---

### 5. View Students

* Display all student records
* Use formatted output (f-strings)

---

### 6. Search Student

* Search by name
* Case-insensitive
* Display details if found

---

### 7. Update Marks

* Select student
* Update marks list

---

### 8. Calculate Average

Create function:

```
def calculate_avg(*marks):
```

* Return average

---

### 9. Generate Report

Display:

```
Name: Anbu
Average: 85
Status: Pass
```

Rule:

* Average ≥ 40 → Pass
* Else → Fail

---

### 10. Exception Handling

Handle:

* File not found
* Invalid input
* JSON errors

---

## Modules

### utils.py

* Average calculation
* Validation functions

### file_handler.py

* Read/write JSON

### main.py

* Menu and program flow

---

## Concepts to Use

* Functions
* *args, **kwargs
* Loops and conditions
* Lists and dictionaries
* Regex (re)
* File handling
* Exception handling
* Modules

---

## Bonus (Optional)

* Sort students (lambda)
* Add timestamp (datetime)
* Delete student
* Improve UI messages

---

## Evaluation

* Functionality
* Code quality
* Concept usage
* Error handling
* File handling

---

## Submission

* Submit all .py files + data.json
* Code should be clean and readable
* Test before submitting

---



Happy Coding
