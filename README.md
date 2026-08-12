# Attendance Report Automation

A Python-based desktop automation application that automates attendance report generation and Excel export from a web-based attendance management system.

The application provides a graphical interface for entering multiple sections, monitoring automation progress, selecting an output directory, and automatically downloading attendance reports as Excel files.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Automation Workflow](#automation-workflow)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Workflow](#application-workflow)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Output](#output)
- [Error Handling](#error-handling)
- [Security](#security)
- [Limitations](#limitations)
- [Testing Scenarios](#testing-scenarios)
- [Future Improvements](#future-improvements)
- [Skills Demonstrated](#skills-demonstrated)
- [What I Learned](#what-i-learned)
- [Author](#author)

---

## Overview

Generating attendance reports manually can involve repeatedly performing the same browser operations:

1. Login to the attendance system.
2. Search for a section.
3. Check the existing attendance report.
4. Determine whether the report is recent.
5. Generate a new report when required.
6. Wait for report generation.
7. Reload the report.
8. Open the export menu.
9. Select Excel.
10. Download the file.
11. Repeat the entire process for other sections.

This project automates that repetitive workflow using **Python, Tkinter, and Playwright**.

The application is designed as a desktop automation tool rather than a simple browser script. It combines a user-friendly GUI with browser automation, timestamp-based decision making, multi-section processing, download management, and configurable output locations.

---

## Problem Statement

Attendance report generation becomes repetitive when reports need to be generated for multiple sections.

For example, processing several sections manually requires repeatedly navigating through the same workflow:

```text
Login
  ↓
Search Section
  ↓
Check Report
  ↓
Generate Report if Required
  ↓
Wait
  ↓
Reload Report
  ↓
Export
  ↓
Excel
  ↓
Download
  ↓
Repeat for Next Section
This increases manual effort and creates opportunities for inconsistent processing.

The goal of this project is to automate this workflow while still allowing the user to control the process through a desktop interface.

Solution

The application provides a GUI where the user enters:

Login credentials
One or more sections
Excel output directory

After the automation starts, Playwright controls the browser and processes each section sequentially.

The application determines whether the current report can be exported or whether the report-generation workflow needs to be performed.

The downloaded Excel files are saved directly to the directory selected by the user.

Key Features
Desktop GUI

Built using Tkinter to provide a simple interface for:

Login
Section entry
Output-folder selection
Automation control
Status monitoring
Progress information
Browser Automation

Playwright automates the web-based attendance workflow, including:

Login
Section selection
Report generation
Report reload
Export navigation
Excel selection
File downloads
Multiple Section Processing

Multiple sections can be entered at once.

Example:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C

The application processes them sequentially.

Timestamp-Based Processing

The application checks the report timestamp before deciding whether to proceed directly to export or generate a new report.

Automatic Excel Download

After the export workflow is completed, the Excel file is automatically downloaded.

Custom Output Directory

The user can select any folder for storing the generated Excel reports.

Example:

C:\Users\Teacher\Desktop\Attendance Reports
Real-Time Status

The GUI provides information about:

Current section
Total sections
Current operation
Waiting status
Download status
Output directory
Stop Automation

The user can request the automation to stop through the GUI.

Easy Windows Setup

A setup script is provided for first-time installation and environment preparation.

How It Works

The application consists of two major layers:

┌──────────────────────────────────────┐
│              GUI Layer               │
│                                      │
│  Tkinter                             │
│  • Login                             │
│  • Section Input                     │
│  • Output Folder                     │
│  • Start / Stop                      │
│  • Progress / Status                 │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Automation Layer            │
│                                      │
│  Playwright                           │
│  • Login                             │
│  • Section Selection                 │
│  • Timestamp Checking                │
│  • Report Generation                 │
│  • Report Reload                     │
│  • Export                            │
│  • Excel Download                    │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            File Output               │
│                                      │
│       User-selected folder           │
└──────────────────────────────────────┘

The GUI is responsible for user interaction, while the automation module performs the browser operations.

Automation Workflow

For every section, the application follows a controlled workflow.

                         START
                           │
                           ▼
                    User Login
                           │
                           ▼
                    Select Section
                           │
                           ▼
                 Check Report Timestamp
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        Recent Report              Older Report
              │                         │
              │                         ▼
              │                  Generate Report
              │                         │
              │                         ▼
              │                    Wait / Process
              │                         │
              │                         ▼
              │                    Reload Report
              │                         │
              │                         ▼
              │                  Check Timestamp
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                         Menu
                           │
                           ▼
                         Export
                           │
                           ▼
                         Excel
                           │
                           ▼
                    Download File
                           │
                           ▼
                    Next Section
                           │
                           ▼
                         END
Report Timestamp Logic

The timestamp is used to determine which workflow should be followed.

Recent Report

If the report meets the application's freshness condition:

Check Timestamp
       ↓
Report is Recent
       ↓
Open Menu
       ↓
Export
       ↓
Excel
       ↓
Download

The application does not unnecessarily regenerate the report.

Older Report

If the report is older than the configured freshness condition:

Check Timestamp
       ↓
Report is Older
       ↓
Generate Now
       ↓
Wait for Report Generation
       ↓
Reload Report
       ↓
Check Timestamp
       ↓
Continue to Export
       ↓
Excel
       ↓
Download

This decision-making logic is one of the main automation features of the project.

Multiple Section Processing

The application supports processing multiple sections sequentially.

For example:

Section A
    ↓
Report Processing
    ↓
Excel Download
    ↓
Section B
    ↓
Report Processing
    ↓
Excel Download
    ↓
Section C
    ↓
Report Processing
    ↓
Excel Download

This allows a user to start the process once instead of manually repeating the same browser workflow for every section.

System Architecture
                    ┌───────────────────────┐
                    │       User            │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Tkinter GUI       │
                    │                       │
                    │ • Credentials         │
                    │ • Sections            │
                    │ • Output Folder       │
                    │ • Start / Stop        │
                    │ • Status              │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Automation Controller  │
                    │                       │
                    │ • Section Queue       │
                    │ • Progress            │
                    │ • Stop Handling       │
                    │ • Error Handling       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      Playwright       │
                    │                       │
                    │ Browser Automation    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Attendance Web System │
                    │                       │
                    │ • Login               │
                    │ • Sections            │
                    │ • Reports             │
                    │ • Export              │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Excel File        │
                    │                       │
                    │ User-selected folder  │
                    └───────────────────────┘
Technology Stack
Technology	Purpose
Python	Core application and automation logic
Tkinter	Desktop GUI
Playwright	Browser automation
Threading	Background automation and GUI responsiveness
Regular Expressions	Timestamp and text processing
OS / pathlib	File and directory management
Batch Scripts	Windows setup and launching
Git	Version control
GitHub	Source-code hosting
Project Structure
attendance-report-automation/
│
├── main.py
├── attendance.py
├── requirements.txt
├── setup.bat
├── run.bat
├── .gitignore
└── README.md
File Responsibilities
main.py

Contains the Tkinter desktop application.

Responsible for:

GUI layout
Login fields
Section input
Output-folder selection
Start button
Stop button
Progress/status display
Communication with the automation module
attendance.py

Contains the browser automation logic.

Responsible for:

Playwright initialization
Login workflow
Section processing
Report timestamp handling
Report generation
Report reload
Export navigation
Excel download
Multi-section processing
Automation errors
requirements.txt

Contains the Python dependencies required to run the application.

setup.bat

Provides first-time Windows setup.

It is intended to install the required Python dependencies and prepare the Playwright browser environment.

run.bat

Provides a simple Windows launcher.

It is also useful during development and debugging because the command window can display runtime errors.

.gitignore

Prevents generated files and unnecessary development artifacts from being committed to Git.

Examples include:

__pycache__/
*.pyc
downloads/
*.xlsx
build/
dist/
README.md

Project documentation containing the architecture, workflow, setup instructions, technical details, limitations, and development information.

Installation
Prerequisites

The current application is designed for Windows.

Required:

Windows 10 or later
Python 3.10 or newer
Internet connection during initial setup
Access to the authorized attendance system
First-Time Setup
Download or clone this repository.
Extract the project folder if downloaded as a ZIP.
Open the project folder.
Double-click:
setup.bat

The setup script prepares the Python environment and installs the required dependencies and Playwright browser components.

After successful setup, the application can be launched using the desktop shortcut created by the setup process.

Running the Application

After first-time setup:

Windows Desktop
       ↓
Attendance Report Automation
       ↓
Application GUI

For normal use, the user does not need to manually type Python or Playwright commands into a terminal.

The run.bat file is mainly useful as a backup/debug launcher.

Using the Application
1. Login

Enter the authorized account credentials into the GUI.

Credentials are entered by the user at runtime.

They should not be hard-coded into the source code.

2. Enter Sections

Enter each section on a separate line.

Example:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C
BTECH-ME-AY2627-SEM-03-D

The application processes them sequentially.

3. Select Output Folder

Use the output-folder selection control to choose where Excel reports should be stored.

Example:

C:\Users\Teacher\Desktop\Attendance Reports

The selected path is displayed in the GUI.

4. Start Automation

Click:

GENERATE EXCEL

The application begins processing the sections.

5. Monitor Progress

The GUI provides status information while the automation is running.

Example:

Total sections: 4

Current section: 2 / 4

Processing:
BTECH-ME-AY2627-SEM-03-B

Status:
Checking report timestamp...

During report generation:

Status:
Generating report...

Waiting for report...

After download:

Status:
Excel file downloaded successfully.
6. Stop Automation

The GUI provides a stop control that allows the user to request termination of the automation process.

Output

The generated Excel files are saved in the output directory selected by the user.

Example:

Attendance Reports/
│
├── Attendance_BTECH-ME-AY2627-SEM-03-A_2026-08-12_23-38-54.xlsx
├── Attendance_BTECH-ME-AY2627-SEM-03-B_2026-08-12_23-42-10.xlsx
└── Attendance_BTECH-ME-AY2627-SEM-03-C_2026-08-12_23-45-32.xlsx

The exact filename depends on the section and the application's download-naming logic.

Error Handling

The automation includes handling for common runtime situations such as:

Browser startup failures
Missing browser components
Page navigation failures
Missing page elements
Report generation issues
Export failures
Download failures
Automation interruption
Invalid section processing

When running through the debug launcher, runtime errors can be inspected in the command window.

Security

This project does not require credentials to be stored in the source code.

Users should enter credentials through the application interface.

Never commit the following to GitHub
Passwords
API keys
Authentication tokens
Session cookies
Personal credentials
.env files containing secrets

A .gitignore file should also be used to prevent accidental commits of generated files and local configuration.

Limitations

This application is designed around the current behavior of a specific web-based attendance system.

Browser automation depends on the structure and behavior of the target website.

Changes to the website may require changes to the automation logic.

Potential changes include:

HTML structure
Element selectors
Button names
Search behavior
Login workflow
Report-generation workflow
Export menu structure
Download behavior
Authentication mechanisms

Therefore, the automation should be maintained if the target website changes.

The application is intended for authorized users and legitimate institutional workflows.

Testing Scenarios

The application should be tested using several scenarios.

Scenario 1 — Recent Report
Login
  ↓
Select Section
  ↓
Check Timestamp
  ↓
Recent Report
  ↓
Export
  ↓
Excel
  ↓
Download

Expected result:

The existing report is exported without unnecessarily generating a new report.

Scenario 2 — Older Report
Login
  ↓
Select Section
  ↓
Check Timestamp
  ↓
Older Report
  ↓
Generate Now
  ↓
Wait
  ↓
Reload Report
  ↓
Check Timestamp
  ↓
Export
  ↓
Excel
  ↓
Download

Expected result:

The report is regenerated and then exported.

Scenario 3 — Multiple Sections
Section 1
   ↓
Excel Download
   ↓
Section 2
   ↓
Excel Download
   ↓
Section 3
   ↓
Excel Download

Expected result:

Each section is processed sequentially and produces its corresponding Excel report.

Scenario 4 — Custom Output Folder
User selects folder
        ↓
Automation downloads Excel
        ↓
File appears in selected folder

Expected result:

The report is stored in the folder selected through the GUI rather than being restricted to a hard-coded directory.

Scenario 5 — Stop Automation
Automation Running
        ↓
User clicks STOP
        ↓
Automation receives stop request
        ↓
Process terminates according to the current operation state

Expected result:

The user can interrupt the automation instead of being forced to wait for every section to complete.

Development Challenges

Several practical engineering challenges were encountered during development.

Dynamic Browser Interaction

The target web application contains dynamically changing elements and report states.

The automation therefore needs to identify and interact with the correct page elements rather than relying on fixed screen coordinates.

Report State Handling

The application needs to distinguish between an existing usable report and a report that requires regeneration.

This led to the timestamp-based workflow.

Multiple Sections

Processing several sections required a sequential execution model so that each section could complete its browser and download workflow before the next section begins.

Download Management

The application needs to detect downloaded Excel files and ensure that they are stored in the user-selected output directory.

GUI and Automation Interaction

Browser automation can take significant time.

Running the automation directly on the GUI thread can make the interface appear frozen.

Background execution is therefore used so that the GUI can continue updating status information and respond to user controls.

Deployment

The project also required consideration of how a non-developer user can install and run the application without manually configuring the entire Python and Playwright environment.

This led to the creation of setup and launcher scripts.

Engineering Decisions
Why Playwright?

Playwright provides browser automation capabilities suitable for interacting with modern web applications.

It allows the application to:

Launch a browser
Navigate pages
Locate elements
Click controls
Enter text
Wait for page states
Handle downloads
Why Tkinter?

Tkinter is included with standard Python installations and is sufficient for building a lightweight Windows desktop interface without introducing a separate frontend framework.

Why Separate main.py and attendance.py?

The GUI and automation logic have different responsibilities.

Keeping them separate improves maintainability:

main.py
   │
   │ GUI
   │
   ▼
attendance.py
   │
   │ Automation
   │
   ▼
Playwright

This separation also makes it easier to modify the interface without rewriting the browser automation logic.

Why Use Background Execution?

The browser automation includes waiting periods and network operations.

Running those operations independently from the GUI prevents the interface from becoming unresponsive during long-running tasks.

Future Improvements

Possible future improvements include:

Automated retry mechanisms
Better handling of temporary network failures
More detailed logging
Structured application logs
Configurable report freshness thresholds
More robust selector strategies
Automated download verification
Improved recovery from browser crashes
Unit tests for timestamp parsing
Integration tests for the automation workflow
Better configuration management
Application packaging into a standalone executable
Automatic application updates
Cross-platform support
Improved user notifications
More advanced progress visualization
Skills Demonstrated

This project demonstrates practical experience in several areas.

Python Development
Python programming
Modular application design
Exception handling
File handling
Directory management
Regular expressions
GUI Development
Tkinter
Event-driven programming
User input handling
GUI state management
Progress/status updates
Background task integration
Browser Automation
Playwright
Web element interaction
Page navigation
Dynamic page handling
Browser lifecycle management
Download automation
Report workflow automation
Software Engineering
Modular architecture
Separation of concerns
Error handling
User-controlled workflows
Deployment scripting
Configuration management
Development Tools
Git
GitHub
PowerShell
Windows batch scripting
Python package management
What I Learned

This project provided practical experience beyond implementing a basic automation script.

Key learning areas include:

Designing a desktop application around a browser automation workflow
Building a GUI for a long-running process
Keeping the GUI responsive while automation runs
Handling dynamic web pages
Designing timestamp-based decision logic
Processing multiple tasks sequentially
Managing browser downloads
Managing user-selected directories
Handling automation failures
Providing user-controlled start/stop functionality
Creating repeatable Windows setup procedures
Using Git and GitHub for version control
Structuring an application into separate GUI and automation modules
Thinking about deployment from the perspective of a non-technical user
Project Status

The project currently provides:

Desktop GUI
Browser automation
Multiple section processing
Timestamp-based report handling
Automatic Excel export
Custom output folder selection
Status/progress display
Stop automation control
Windows setup workflow
GitHub source-code management
Repository

GitHub:

https://github.com/teja23-saviour/attendance-report-automation

Author

Teja Rayavarapu

GitHub:

https://github.com/teja23-saviour

License

This project is intended for educational and authorized institutional use.

The automation should only be used with appropriate permission to access and automate the target attendance system.