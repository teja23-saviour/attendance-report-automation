# Attendance Report Automation

A Windows desktop application that automates multi-section attendance report generation and Excel export using Python, Tkinter, and Playwright.

---

## Problem Statement

Generating attendance reports for multiple student sections requires repeatedly performing the same manual browser operations:

Login -> Select Section -> Check Report -> Generate / Reload -> Export -> Download Excel

Performing this manually for every section is repetitive, time-consuming, and prone to human error.

---

## Solution

This project automates the complete attendance report workflow through a native Windows desktop application.

The user enters multiple student sections, selects a custom output folder, and triggers the automation. The application processes each section sequentially, evaluates the report's current state, generates or reloads the report when required, exports it as an Excel file, and saves the download directly to the specified directory.

---

## Features

* **Windows Desktop GUI** – Intuitive control panel built with Tkinter.
* **Runtime Login Credentials** – Securely handles credentials during active sessions without hardcoding.
* **Batch Input Processing** – Supports multi-line input for bulk section processing.
* **Student-Group Verification** – Automatically searches, selects, and validates student groups.
* **Timestamp & State Awareness** – Evaluates report timestamps to determine if regeneration is required.
* **Automatic Reload & Regeneration** – Handles dynamic wait times and report regeneration cycles automatically.
* **Excel Export Automation** – Navigates export menus and handles direct `.xlsx` downloads.
* **Custom File Management** – Automatically routes downloaded reports to user-defined directories.
* **Live Status Tracking** – Real-time terminal/status display for operations, progress, and errors.
* **Execution Controls** – Start, Stop, and Exit capabilities with thread safety.
* **Non-Blocking Architecture** – Built with multithreading to keep the UI fully responsive during long automation runs.
* **Automated Environment Setup** – Includes Windows batch scripts for simple one-click installation and startup.

---

## Technology Stack

| Component | Technology | Role / Usage |
| :--- | :--- | :--- |
| **Language** | Python | Core logic and automation driver |
| **GUI Framework** | Tkinter | Native desktop user interface |
| **Automation** | Playwright | Headless/Headed browser automation |
| **Concurrency** | Threading | Decouples UI thread from automation execution |
| **Parsing** | re (Regex) | Text extraction and timestamp analysis |
| **FileSystem** | pathlib / os | Directory creation and path resolution |
| **Tooling** | Batch Scripts | Environment setup (.bat) and launcher |
| **VCS** | Git / GitHub | Source control and release management |

---

## Prerequisites & System Requirements

Before running the project manually, ensure your system meets the following requirements:

* **Operating System:** Windows 10 or Windows 11 (64-bit)
* **Python:** Python 3.8 or higher installed and added to PATH
* **Playwright Dependencies:**
  * playwright (Python package)
  * Chromium browser binaries installed via Playwright

### Quick Installation

If not using setup.bat, install the required packages using pip:

pip install playwright
playwright install chromium

---

## Workflow

1. **Initialize & Authenticate:** Launches browser via Playwright and logs into the target portal using active session credentials.
2. **Group Selection & Verification:** Navigates to the section management page, searches for the specified student group, and verifies selection.
3. **State & Timestamp Inspection:** Checks current report timestamp. If the report is up to date, it skips directly to export. If stale or missing, it triggers a background regeneration and polls for completion.
4. **Export & File Handling:** Triggers the Excel export option via DOM interaction, captures the browser download stream, and writes the file to the chosen local directory.
5. **Sequential Loop:** Iterates to the next section in the queue until all input sections are processed.

---

## Example Input Format

When supplying sections in the GUI multi-line text area, format each section on a new line:

BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C

---

## Application Interface Structure

The desktop interface is structured into clear functional components:

* **Authentication Panel:** Input controls for username and password with toggleable password visibility.
* **Section Batch Input:** Multi-line text field for queuing section IDs.
* **Output Configuration:** File picker dialog to select destination directory for Excel exports.
* **Live Telemetry & Logs:** Status log box showing real-time operational messages, errors, and progress updates.
* **Execution Controls:** Quick-action buttons for starting (`GENERATE EXCEL`), stopping (`STOP AUTOMATION`), or closing the application.

---

## Setup & Installation

1. **Clone the Repository:**
   git clone https://github.com/teja23-saviour/attendance-report-automation.git
   cd attendance-report-automation

2. **Run Windows Setup:**
   Double-click `setup.bat` or execute via command prompt:
   setup.bat

3. **Launch the Application:**
   Double-click `launch.bat` or run:
   python main.py

---

## Skills Demonstrated

Python · Tkinter · Playwright · Browser Automation · GUI Development · Multithreading · File I/O · Error Handling · Git · GitHub

---

## Author

**Teja Rayavarapu**

* **GitHub:** [teja23-saviour](https://github.com/teja23-saviour)
* **Repository:** [attendance-report-automation](https://github.com/teja23-saviour/attendance-report-automation)

---

## License

This project is intended for educational and authorized institutional use.

Use the automation only when you have appropriate permission to access and automate the target attendance system.