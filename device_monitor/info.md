# Python Intermediate Mini Project (2-Day Assignment)

# Project Title

Smart Local Network File & Device Monitor

---

# Project Overview

Build a desktop-based Python application using Tkinter that monitors files, tracks connected devices, and maintains activity logs.

This application should simulate a lightweight local monitoring tool where users can:

* Monitor files in selected folders
* Track newly added files
* Store activity logs
* Search logs and files
* Export reports
* Manage monitored folders using a GUI

The goal of this project is to combine Python fundamentals with real-world problem-solving.

---

# Project Duration

2 Days

---

# Difficulty Level

Intermediate

---

# Technologies Required

* Python 3
* Tkinter
* JSON / CSV
* Python Standard Library

Optional:

* psutil
* socket

---

# Learning Objectives

By completing this project, you should be able to:

* Build a complete Python desktop application
* Work with modular Python code
* Handle files and logs
* Use regex validation
* Implement exception handling properly
* Build GUI applications using Tkinter
* Work with JSON and CSV files
* Use Python built-in modules effectively

---

# Project Features

## 1. Login Window

Create a basic login screen.

Requirements:

* Username field
* Password field
* Login button
* Hardcoded authentication

Example:

* Username: admin
* Password: admin123

---

## 2. Dashboard

After successful login, display a dashboard.

Dashboard options:

```text
1. Add Folder to Monitor
2. View Monitored Files
3. Search File Activity
4. Export Logs
5. System Information
6. Exit
```

---

## 3. Folder Monitoring

Allow users to select folders.

Requirements:

* Detect files inside folder
* Store file details:

  * File name
  * File size
  * File type
  * Last modified date
* Detect newly added files

Use:

* os module
* datetime module

---

## 4. File Activity Logger

Store activity logs.

Example log:

```text
[2026-05-11 10:30] New file detected: report.pdf
```

Requirements:

* Save logs to JSON or CSV
* Append new logs
* Maintain activity history

---

## 5. Search Functionality

Allow searching:

* File name
* Extension
* Date

Requirements:

* Partial match support
* Case-insensitive search
* Regex-based filtering

---

## 6. File Statistics

Generate simple reports:

* Total monitored files
* Largest file
* Most common extension
* Total folder size

Optional:

* Daily activity summary

---

## 7. Export Reports

Allow exporting logs into:

* CSV
* JSON
* TXT

Requirements:

* Create export directory automatically
* Save timestamped report

---

## 8. System Information

Display:

* Current date/time
* Python version
* Operating system
* Current working directory

Use:

* sys module
* os module
* datetime module

---

## 9. File Handling Requirements

Use:

* read()
* write()
* append mode
* context managers (`with` statement)

Requirements:

* Handle missing files
* Handle invalid paths
* Create files automatically if not found

---

## 10. Exception Handling

Handle:

* FileNotFoundError
* PermissionError
* ValueError
* Invalid folder paths

Use:

* try
* except
* else
* finally

---

## 11. Functions

Create separate functions for:

* Login validation
* Folder scanning
* File searching
* Log saving
* Export generation
* Report generation

Requirements:

* Use return values properly
* Use default arguments
* Use *args or **kwargs at least once
* Use lambda at least once

---

## 12. Modules and Packages

Suggested structure:

```bash
network_monitor/
 ├── main.py
 ├── ui.py
 ├── scanner.py
 ├── logger.py
 ├── reports.py
 ├── utils.py
 ├── data/
 │    ├── logs.json
 │    ├── exports/
```

---

## 13. String and Regex Usage

Use regex for:

* File extension filtering
* Date validation
* Search matching

Use string formatting:

* f-strings
* string methods

---

## 14. Tkinter UI Requirements

Use:

* Label
* Entry
* Button
* Frame
* Treeview/Listbox
* Scrollbar
* MessageBox

Requirements:

* Clean UI layout
* Responsive structure
* Proper spacing and alignment

---

# Python Concepts Covered

This project should include usage of:

* Variables and Data Types
* Lists, Dictionaries, Tuples, Sets
* Operators
* Conditions and Loops
* Functions
* Lambda Functions
* File Handling
* JSON and CSV
* Regex
* Exception Handling
* Modules and Imports
* Tkinter UI
* Python Built-in Modules

---

# Bonus Features (Optional)

Optional advanced features:

* Real-time folder monitoring
* Drag-and-drop folder selection
* Dark mode UI
* SQLite database integration
* Multi-user login
* Password hashing
* File change notifications
* Search filters using regex patterns

---

# Submission Requirements

Submit:

* Complete source code
* JSON/CSV log files
* README.md
* UI screenshots
* requirements.txt (if external libraries used)

---

# Data Management

All application data should be stored locally inside the `data/` folder.

Suggested structure:

```bash
data/
 ├── logs.json
 ├── monitored_files.json
 ├── exports/
 │    ├── report_2026_05_11.csv
```

Requirements:

* Store monitored file details in JSON format
* Save activity logs separately
* Export generated reports into the `exports/` folder
* Automatically create files/folders if they do not exist
* Load saved data automatically when the application starts

---|---|
| Functionality | 30 |
| UI Design | 15 |
| Code Quality | 20 |
| File Handling | 10 |
| Exception Handling | 10 |
| Modular Structure | 10 |
| Bonus Features | 5 |

---

# Important Guidelines

* Write clean and readable code
* Use meaningful variable names
* Avoid duplicate code
* Add comments where required
* Handle errors properly
* Test the application before submission

---

# Day-wise Plan

## Day 1

Complete:

* Project setup
* Login window
* Dashboard UI
* Folder scanning
* File handling
* Save logs

## Day 2

Complete:

* Search functionality
* Reports
* Export system
* Exception handling
* UI cleanup
* Final testing
* README and screenshots

---

# Final Note

Focus on:

* Problem-solving
* Clean code structure
* Understanding the logic
* Real-world implementation

Build step by step and understand every part of the application.
