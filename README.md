Attendance Report Automation

Windows desktop application for automating multi-section attendance report generation and Excel export using Python, Tkinter, and Playwright.



📌 Overview

Generating attendance reports for multiple student sections can require repeatedly performing the same browser operations:

Login → Select Section → Check Report → Generate/Reload if required → Export → Download Excel

This project automates that workflow through a Windows desktop application.

The user enters the required student sections, selects an output folder, and starts the automation. The application processes sections sequentially, monitors the report state, performs the required browser actions, and saves the resulting Excel files to the selected directory.

The project combines:

Tkinter for the desktop interface

Playwright for browser automation

Python for workflow orchestration and file handling

Background execution to keep the GUI responsive

Git/GitHub for version control and project management

🎯 Problem

Manual attendance-report collection becomes repetitive when the same report-generation and export workflow has to be performed for many sections.

💡 Solution

Build a reusable automation tool that:

Accepts multiple sections.

Verifies the requested section in the web application.

Reads the current report state/timestamp.

Decides whether the existing report can be exported or needs regeneration.

Generates and reloads the report when required.

Navigates through the export workflow.

Downloads the Excel report.

Saves it to the user-selected output folder.

Continues automatically with the next section.

✨ Features

Feature

Description

🖥️ Desktop GUI

Windows interface built with Tkinter

🔐 Runtime Credentials

Credentials are entered at runtime rather than hard-coded

📝 Multi-Section Input

Enter multiple student groups, one per line

🔎 Section Verification

Searches for and verifies the requested student group

⏱️ Timestamp-Aware Processing

Uses the report timestamp to determine the next workflow step

🔄 Report Regeneration

Generates and reloads reports when the current report requires regeneration

📤 Excel Export

Automates the report export process

📥 Download Handling

Waits for and saves the Excel download

📁 Custom Output Folder

User chooses where generated reports are stored

📊 Live Status Log

Displays the current section and detailed automation messages

🛑 Stop Control

Allows the user to request automation termination

🔁 Sequential Processing

Processes sections one after another

🪟 Windows Setup

Includes a setup/launch workflow for Windows users

📸 Screenshots

Store screenshots in docs/screenshots/ using the filenames shown below.

Main Application



The main interface provides credential input, multi-section entry, output-folder selection, live status monitoring, and automation controls.

Automation Status



The status panel shows section verification, report timestamp processing, export operations, and download progress.

Generated Excel Reports



Generated attendance reports are saved to the directory selected through the GUI.

Security: Do not publish screenshots containing real passwords, authentication tokens, or sensitive student information.

🏗️ Architecture

┌──────────────────────────────────────────────────────────────┐
│                           USER                               │
│                                                              │
│  Credentials • Sections • Output Folder • Start / Stop      │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                        TKINTER GUI                           │
│                                                              │
│  • User Input                                                │
│  • Section Management                                        │
│  • Output Folder                                             │
│  • Start / Stop Controls                                     │
│  • Status / Progress                                         │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    AUTOMATION CONTROLLER                     │
│                                                              │
│  • Sequential Section Processing                             │
│  • Timestamp Decision                                        │
│  • Progress Updates                                          │
│  • Stop Handling                                             │
│  • Error Handling                                            │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                         PLAYWRIGHT                           │
│                                                              │
│  Login → Section Search → Verification → Report Processing  │
│                  → Export → Excel Download                   │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       EXCEL OUTPUT                            │
│                                                              │
│                 User-selected directory                      │
└──────────────────────────────────────────────────────────────┘

🔄 End-to-End Workflow

For each requested section:

START
  │
  ▼
Launch Browser
  │
  ▼
Login
  │
  ▼
Find Student Group Field
  │
  ▼
Enter Requested Section
  │
  ▼
Wait for Matching Suggestions
  │
  ▼
Verify Selected Student Group
  │
  ▼
Read Report Timestamp / State
  │
  ├──────────────────────────────┐
  │                              │
  ▼                              ▼
Report Can Be Exported      Report Requires
Under Current Rule          Regeneration
  │                              │
  │                              ▼
  │                         Generate Report
  │                              │
  │                              ▼
  │                         Wait for Report
  │                              │
  │                              ▼
  │                         Reload Report
  │                              │
  └──────────────┬───────────────┘
                 │
                 ▼
          Open Report Menu
                 │
                 ▼
               Export
                 │
                 ▼
               Excel
                 │
                 ▼
          Wait for Download
                 │
                 ▼
       Save to Output Folder
                 │
                 ▼
        Mark Section Complete
                 │
                 ▼
          Process Next Section
                 │
                 ▼
                END

🧠 Core Automation Logic

1. Multi-Section Processing

Sections are entered one per line:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C

The application converts the input into a processing queue and handles each section independently.

Section A → Complete → Section B → Complete → Section C → Complete

This prevents the user from having to repeat the entire browser workflow manually.

2. Student Group Verification

Before report processing, the automation:

Enter Section
     ↓
Wait for Suggestions
     ↓
Find Matching Student Group
     ↓
Select Exact Match
     ↓
Verify Selected Value
     ↓
Continue

This is important because selecting the wrong student group could result in downloading the wrong report.

3. Timestamp-Based Report Processing

The application reads the report timestamp and applies the configured report-freshness rule.

Conceptually:

                 Read Timestamp
                       │
                       ▼
              Parse Report Age
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Export Allowed      Regeneration
          by rule             Required
              │                 │
              │                 ▼
              │            Generate Now
              │                 │
              │                 ▼
              │             Wait / Reload
              │                 │
              └────────┬────────┘
                       │
                       ▼
                     Export

The freshness threshold is an implementation/configuration rule rather than a hard-coded assumption in the documentation.

4. Report Regeneration

When the report requires regeneration:

Generate Now
     ↓
Wait for report generation
     ↓
Reload report
     ↓
Continue export workflow

This avoids proceeding with a report that does not satisfy the application's configured processing condition.

5. Excel Download Handling

The application waits for the browser's download event rather than assuming the file has already been written.

Open Export
     ↓
Select Excel
     ↓
Wait for Download
     ↓
Save File
     ↓
Verify / Report Download Status

🖥️ GUI

The application is designed around four primary areas:

Teacher Login

Username / email

Password

Show/hide password

Student Groups / Sections

Multi-line section input

One section per line

Sequential processing

Excel Output Folder

Manual path selection

Browse dialog

User-defined destination

Automation Status

Current section

Current operation

Detailed status messages

Completion/error information

Bottom controls provide:

GENERATE EXCEL

STOP AUTOMATION

CLOSE APPLICATION

🛠️ Technology Stack

Technology

Role

Python

Core application and automation logic

Tkinter

Desktop GUI

Playwright

Browser automation

Threading / Background Execution

Keeps the GUI responsive during long-running automation

Regular Expressions

Timestamp and text parsing

pathlib / os

File and directory management

Batch Scripts

Windows setup and launch

Git

Version control

GitHub

Source-code hosting

📂 Project Structure

attendance-report-automation/
│
├── main.py
├── attendance.py
├── requirements.txt
├── setup.bat
├── run.bat
├── .gitignore
├── README.md
│
└── docs/
    └── screenshots/
        ├── main-gui.png
        ├── automation-status.png
        └── excel-output.png

main.py

Desktop application and Tkinter presentation layer.

Typical responsibilities:

Build the GUI

Collect user input

Manage section input

Select output folder

Start/stop automation

Display status information

attendance.py

Browser automation and workflow layer.

Typical responsibilities:

Initialize Playwright

Authenticate

Find and select student groups

Process report timestamps

Generate/reload reports

Navigate export workflow

Download Excel files

Process multiple sections

Handle automation errors

requirements.txt

Python dependencies required by the project.

setup.bat

Windows first-time setup script used to prepare the required environment and browser dependencies.

run.bat

Windows launcher/debug entry point. Useful during development when console output needs to remain visible.

.gitignore

Prevents generated files and local artifacts from being committed.

Typical entries include:

__pycache__/
*.pyc
downloads/
*.xlsx
build/
dist/

⚙️ Installation

Prerequisites

Windows 10 or later

Python 3.x

Internet connection during initial setup

Authorized access to the target attendance system

Clone the Repository

git clone https://github.com/teja23-saviour/attendance-report-automation.git
cd attendance-report-automation

First-Time Setup

Run:

setup.bat

The setup workflow prepares the required Python environment/dependencies and Playwright browser components.

After setup, the application can be launched using the Windows desktop shortcut created by the setup process.

Development / Debugging

During development, run.bat can be used when console output is useful for troubleshooting.

🚀 Usage

Step 1 — Launch

Open:

Attendance Report Automation

from the desktop shortcut.

Step 2 — Enter Authorized Credentials

Enter the username/email and password for the target attendance system.

Credentials are supplied at runtime and should not be stored in source code.

Step 3 — Add Sections

Enter one section per line:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C

Step 4 — Select Output Folder

Click Browse... and choose the destination for Excel reports.

Example:

C:\Users\tejar\OneDrive\Desktop\operation Shershaah

Step 5 — Start

Click:

GENERATE EXCEL

The application begins processing the sections sequentially.

Step 6 — Monitor

Use the Automation Status panel to monitor:

Current section

Student-group selection

Timestamp processing

Report generation

Export

Download

Completion/errors

Step 7 — Verify Output

Open the selected output folder and verify the generated .xlsx files.

📊 Example Output

A completed output directory may look like:

operation Shershaah/
│
├── Attendance_BTECH-ECE-AY2627-SEM-07-....xlsx
├── Attendance_BTECH-ME-AY2627-SEM-03-....xlsx
└── Attendance_BTECH-ME-AY2627-SEM-03-....xlsx

The exact filenames depend on the application's file-naming implementation.

🧪 Testing Strategy

The application should be tested across the following scenarios.

Test 1 — Report Eligible for Direct Export

Login
  ↓
Select Section
  ↓
Read Timestamp
  ↓
Current rule allows export
  ↓
Export
  ↓
Download Excel

Expected: The application proceeds to export without unnecessary report regeneration.

Test 2 — Report Requires Regeneration

Login
  ↓
Select Section
  ↓
Read Timestamp
  ↓
Regeneration required
  ↓
Generate Now
  ↓
Wait
  ↓
Reload
  ↓
Export
  ↓
Download Excel

Expected: The report is regenerated before export.

Test 3 — Multiple Sections

Section A
   ↓
Download
   ↓
Section B
   ↓
Download
   ↓
Section C
   ↓
Download

Expected: Each section is processed sequentially and produces its corresponding output.

Test 4 — Custom Output Directory

Select Folder
     ↓
Run Automation
     ↓
Download
     ↓
Verify File Location

Expected: Files are stored in the selected folder.

Test 5 — Stop Automation

Automation Running
       ↓
STOP AUTOMATION
       ↓
Stop Request
       ↓
Workflow Stops According to Current State

Expected: The user can request that the automation stop.

🧩 Engineering Challenges & Solutions

Dynamic Web Elements

Challenge:The target application contains dynamically loaded fields, suggestions, menus, and report states.

Approach:Use Playwright's browser/page interaction model and state-based waits instead of relying only on fixed screen coordinates.

Correct Section Selection

Challenge:Processing the wrong student group could produce an incorrect attendance report.

Approach:Search for the requested section, select the matching suggestion, and verify the selected value before continuing.

Report State Management

Challenge:The automation cannot blindly export every existing report because the report may require regeneration.

Approach:Read and interpret the report timestamp/state and route execution through the appropriate processing branch.

Long-Running Browser Operations

Challenge:Browser operations can take time because of network requests and report generation.

Approach:Run the automation separately from the main GUI event handling so the interface can continue displaying status and responding to controls.

Download Management

Challenge:The browser download may not be immediately available after clicking Excel.

Approach:Wait for the download event and save the resulting file to the configured output directory.

Windows Deployment

Challenge:A Python application with Playwright requires dependencies and browser components that may not exist on another machine.

Approach:Provide a Windows setup workflow that prepares the environment and browser dependencies, followed by a desktop launch workflow.

🔐 Security & Privacy

The application is designed to receive credentials at runtime.

Never commit the following to GitHub:

Passwords
API keys
Authentication tokens
Session cookies
Private credentials
.env files containing secrets

Also avoid publishing:

Student personal information

Attendance records

Private institutional data

Screenshots containing credentials

The automation should only be used with appropriate authorization to access the target system.

⚠️ Limitations

The automation depends on the current behavior and structure of the target web application.

Changes to the website may require updates to:

Element selectors

HTML structure

Login flow

Student-group search

Report generation

Report reload behavior

Export menu

Excel download behavior

Authentication flow

The application is currently intended for Windows.

🔮 Future Improvements

Planned or possible improvements include:

More robust retry and recovery mechanisms

Browser crash recovery

Network-failure recovery

Stronger download verification

More resilient selectors

Structured logging

Configurable automation settings

Unit tests for timestamp parsing

Integration tests for browser workflows

Improved progress visualization

Automatic application updates

Standalone executable distribution

Better user notifications

Centralized configuration

💼 Project Highlights

Attendance Report Automation | Python, Tkinter, Playwright

Developed a Windows desktop application that automates multi-section attendance report generation and Excel export using Python and Playwright. Built a Tkinter GUI with timestamp-aware report processing, section verification, configurable output directories, live status monitoring, background execution, download handling, and user-controlled execution.

Key Contributions

Developed a Python + Playwright browser automation workflow for multi-section attendance report generation and Excel export.

Built a Tkinter desktop GUI for section management, configurable output folders, live automation status, and execution controls.

Implemented timestamp-based report processing logic to determine whether a report can proceed to export or requires regeneration and reload.

Designed separation between the GUI layer and browser-automation layer, improving maintainability and debugging.

Implemented background execution and download handling for long-running browser workflows while keeping the GUI responsive.

Created a Windows setup and launch workflow and maintained the project using Git and GitHub.

🎯 Technical Skills Demonstrated

Programming

Python

Modular programming

Exception handling

File and directory management

Regular expressions

Background execution

Browser Automation

Playwright

Browser lifecycle management

Dynamic web-element interaction

Page navigation

State-based workflow handling

Download automation

GUI Development

Tkinter

Event-driven programming

User input handling

Status/progress interfaces

Background task integration

Software Engineering

Separation of concerns

Workflow design

Error handling

Deployment scripting

Git

GitHub

📈 Project Value

This project demonstrates the complete engineering cycle:

Identify Repetitive Task
        ↓
Analyze Existing Workflow
        ↓
Design Automation Logic
        ↓
Build Desktop Interface
        ↓
Implement Browser Automation
        ↓
Handle State + Downloads
        ↓
Add Deployment Workflow
        ↓
Test and Iterate

Rather than being only a browser script, the project combines automation, GUI development, asynchronous/background execution, file management, error handling, and Windows deployment into a reusable desktop application.

👨‍💻 Author

Teja Rayavarapu

GitHub:https://github.com/teja23-saviour

Repository:https://github.com/teja23-saviour/attendance-report-automation

📄 License

This project is intended for educational and authorized institutional use.

Use the automation only when you have appropriate permission to access and automate the target attendance system.