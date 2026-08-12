# Attendance Report Automation

A Windows desktop application that automates multi-section attendance report generation and Excel export using Python, Tkinter, and Playwright.

## Problem Statement

Generating attendance reports for multiple student sections requires repeatedly performing the same browser operations:

**Login → Select Section → Check Report → Generate/Reload if Required → Export → Download Excel**

Performing this manually for every section is repetitive, time-consuming, and can lead to mistakes.

## Solution

This project automates the complete attendance report workflow through a Windows desktop application.

The user can enter multiple student sections, select an output folder, and start the automation. The application processes each section sequentially, checks the report state, generates or reloads the report when required, exports it as Excel, and saves the downloaded file to the selected folder.

## Features

- Windows desktop GUI
- Runtime login credentials
- Multiple student-section input
- Student-group selection and verification
- Report timestamp/state checking
- Automatic report generation when required
- Automatic report reload
- Excel export automation
- Automatic download handling
- Custom output-folder selection
- Live automation status
- Start/Stop controls
- Sequential processing of multiple sections
- Windows setup and launch scripts

## Technology Stack

- **Python** – Core application and automation logic
- **Tkinter** – Desktop GUI
- **Playwright** – Browser automation
- **Threading** – Background execution and GUI responsiveness
- **Regular Expressions** – Timestamp and text processing
- **pathlib / os** – File and directory management
- **Batch Scripts** – Windows setup and launching
- **Git & GitHub** – Version control and project hosting

## How It Works

For each requested section, the application follows this workflow:

```text
Start
  ↓
Launch Browser
  ↓
Login
  ↓
Find Student Group
  ↓
Select and Verify Section
  ↓
Check Report Timestamp / State
  ↓
 ┌──────────────────────────────┐
 │                              │
 ▼                              ▼
Report Ready              Regeneration Required
 │                              │
 │                              ▼
 │                       Generate Report
 │                              │
 │                              ▼
 │                       Wait and Reload
 │                              │
 └──────────────┬───────────────┘
                ↓
          Open Export Menu
                ↓
             Select Excel
                ↓
          Wait for Download
                ↓
        Save to Output Folder
                ↓
        Process Next Section
                ↓
               End
## Example Sections

Multiple sections can be entered, one per line:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C

The application processes each section sequentially.

GUI

The application provides the following main controls and areas:

Login
Username/email
Password
Show/hide password
Student Sections
Multi-line section input
One section per line
Sequential processing
Excel Output
Output-folder selection
Browse option
User-defined destination
Automation Status

Displays:

Current section
Current operation
Progress messages
Completion status
Error information
Controls
GENERATE EXCEL
STOP AUTOMATION
CLOSE APPLICATION
Project Highlights
Automated a repetitive browser-based attendance-report workflow using Python and Playwright.
Developed a Tkinter desktop GUI for section management, output selection, status monitoring, and execution control.
Implemented timestamp-aware report processing to determine whether a report requires regeneration.
Added multi-section sequential processing.
Implemented automatic Excel download handling.
Added configurable output directories.
Used background execution to keep the GUI responsive.
Created a Windows setup and desktop-launch workflow.
Managed the project using Git and GitHub.
Skills Demonstrated

Python · Tkinter · Playwright · Browser Automation · GUI Development · Threading · File Handling · Error Handling · Git · GitHub
Author

Teja Rayavarapu

GitHub: https://github.com/teja23-saviour

Repository: https://github.com/teja23-saviour/attendance-report-automation

License

This project is intended for educational and authorized institutional use.

Use the automation only when you have appropriate permission to access and automate the target attendance system.