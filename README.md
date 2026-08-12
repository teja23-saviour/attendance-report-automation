# Attendance Report Automation

**A Windows desktop automation application that streamlines multi-section attendance report generation and Excel export using Python, Tkinter, and Playwright.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF9800)
![Playwright](https://img.shields.io/badge/Browser%20Automation-Playwright-2EAD33?logo=playwright&logoColor=white)
![Git](https://img.shields.io/badge/Version%20Control-Git-F05032?logo=git&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

## 📌 Overview

Attendance report generation can involve repeatedly performing the same browser actions for every student section: logging in, selecting a section, checking the report status, generating a report when required, reloading the report, navigating through the export menu, selecting Excel, and downloading the file.

This project converts that repetitive workflow into a **desktop automation application**.

The application provides a Tkinter-based interface where an authorized user can enter multiple sections, choose an Excel output folder, start the automation, monitor progress, and stop the process when required. Playwright handles the browser interaction and download workflow.

### Project goal

> **Reduce repetitive manual browser operations and make multi-section attendance report collection more consistent and efficient.**

---

## ✨ Key Features

### 🖥️ Desktop GUI
- Clean Windows desktop interface built with Tkinter
- Username/email and password fields
- Show/hide password option
- Multi-section input
- Output-folder selection
- Start/Generate Excel control
- Stop automation control
- Live status and progress information

### 🌐 Browser Automation
Playwright automates the required browser workflow, including:
- Login
- Student-group/section selection
- Report inspection
- Report generation
- Report reload
- Export-menu navigation
- Excel selection
- File download

### 🔄 Multi-Section Processing
Multiple sections can be entered one per line and processed sequentially.

Example:

```text
BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C
```

The application completes the workflow for one section before moving to the next.

### ⏱️ Timestamp-Based Decision Logic
Before exporting a report, the automation reads the report timestamp.

The workflow distinguishes between a report that satisfies the configured freshness condition and a report that requires regeneration.

```text
Check Report Timestamp
          │
          ├── Report is fresh
          │       │
          │       ▼
          │     Export
          │
          └── Report requires regeneration
                  │
                  ▼
             Generate Now
                  │
                  ▼
             Wait for Report
                  │
                  ▼
             Reload Report
                  │
                  ▼
                Export
```

This helps avoid unnecessary report generation when the existing report can proceed directly to export.

### 📥 Automatic Excel Export
After the export workflow is completed, the Excel report is downloaded automatically.

### 📁 Custom Output Directory
The user can choose the destination directory from the GUI.

Example:

```text
C:\Users\tejar\OneDrive\Desktop\operation Shershaah
```

The generated Excel files are saved in the selected location.

### 📊 Live Automation Status
The GUI displays the current operation and automation messages, for example:

```text
Current: Section completed

Requested Student Group: BTECH-ME-AY2627-SEM-03-A
Finding Student Group field...
Student Group field found.
Entering section...
Student Group selection verified.
Checking report timestamp...
Report is fresh...
Opening report menu...
Selecting Export...
Excel selected...
Downloading Excel...
Downloaded successfully.
```

### 🛑 User-Controlled Execution
The user can start the automation and request that it stop through the GUI.

---

# 📸 Screenshots

## Main Application

![Attendance Report Automation GUI](docs/screenshots/main-gui.png)

The GUI provides credential input, section management, output-folder selection, status monitoring, and automation controls.

## Automation in Progress / Completed

![Automation Status](docs/screenshots/automation-status.png)

The status panel displays the current section and detailed automation messages, including section selection, timestamp processing, export, and download progress.

## Generated Excel Reports

![Excel Output](docs/screenshots/excel-output.png)

Generated attendance Excel files are stored in the user-selected output directory.

> **Privacy note:** Screenshots included in the repository should not contain real passwords, authentication tokens, or sensitive student information.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │        Tkinter GUI          │
                    │                             │
                    │ • Credentials               │
                    │ • Sections                  │
                    │ • Output Folder             │
                    │ • Start / Stop              │
                    │ • Status / Progress         │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │   Automation Controller     │
                    │                             │
                    │ • Section Processing        │
                    │ • Timestamp Decision        │
                    │ • Progress Updates          │
                    │ • Stop Handling             │
                    │ • Error Handling             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │          Playwright         │
                    │                             │
                    │ • Browser Control           │
                    │ • Login                     │
                    │ • Section Selection         │
                    │ • Report Generation         │
                    │ • Report Reload             │
                    │ • Export                    │
                    │ • Download                  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Excel Output          │
                    │     User-selected folder    │
                    └─────────────────────────────┘
```

---

# 🔄 End-to-End Workflow

For each section, the application follows this general workflow:

```text
START
  │
  ▼
Launch Browser
  │
  ▼
Login
  │
  ▼
Find Student Group / Section
  │
  ▼
Select and Verify Section
  │
  ▼
Read Report Timestamp
  │
  ├───────────────┐
  │               │
  ▼               ▼
Fresh Report   Report Requires
              Regeneration
  │               │
  │               ▼
  │          Generate Now
  │               │
  │               ▼
  │          Wait for Report
  │               │
  │               ▼
  │          Reload Report
  │               │
  └───────┬───────┘
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
    Download File
          │
          ▼
     Next Section
          │
          ▼
         END
```

---

# 🧠 Important Technical Logic

## 1. Section Verification

The requested student group is entered into the web application's section field.

The automation waits for matching suggestions and verifies the selected value before continuing.

This reduces the risk of processing the wrong section.

## 2. Report Timestamp Processing

The automation reads the report timestamp and converts the relevant time information into a comparable value.

The timestamp determines whether the application:

- proceeds toward export, or
- generates the report and follows the regeneration workflow.

## 3. Report Regeneration

When regeneration is required:

```text
Generate Now
     ↓
Wait
     ↓
Reload Report
     ↓
Continue Report Processing
```

The browser workflow is kept separate from the GUI so the application can manage long-running browser operations without making the interface itself responsible for every browser action.

## 4. Download Handling

The application waits for the Excel download event and saves the resulting file to the selected output directory.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and automation logic |
| **Tkinter** | Desktop GUI |
| **Playwright** | Browser automation |
| **Threading** | Background execution and GUI responsiveness |
| **Regular Expressions** | Timestamp/text processing |
| **pathlib / os** | File and directory management |
| **Batch Scripts** | Windows setup and launching |
| **Git** | Version control |
| **GitHub** | Repository hosting |

---

# 📂 Project Structure

```text
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
```

### `main.py`

Contains the Tkinter presentation layer and user interaction logic.

Responsibilities include:
- GUI layout
- Credential input
- Section input
- Output-folder selection
- Start/stop controls
- Status/progress display
- Starting the automation workflow

### `attendance.py`

Contains the browser automation workflow.

Responsibilities include:
- Playwright browser initialization
- Login
- Student-group selection
- Report timestamp processing
- Report generation
- Report reload
- Export workflow
- Excel download
- Multi-section processing
- Automation error handling

### `requirements.txt`

Contains the Python dependencies required by the application.

### `setup.bat`

Provides the Windows first-time setup workflow for preparing the required environment and Playwright browser components.

### `run.bat`

Provides a simple Windows launcher/debug entry point. It is useful when runtime output needs to be inspected during development or troubleshooting.

### `.gitignore`

Prevents generated/local files from being committed to the repository.

Typical ignored files include:

```text
__pycache__/
*.pyc
downloads/
*.xlsx
build/
dist/
```

---

# ⚙️ Installation

## Prerequisites

The current application is intended for Windows.

You need:

- Windows 10 or later
- Python 3.x
- Internet connection during first-time setup
- Authorized credentials/access to the target attendance system

## First-Time Setup

Clone or download the repository:

```bash
git clone https://github.com/teja23-saviour/attendance-report-automation.git
cd attendance-report-automation
```

Then run:

```text
setup.bat
```

The setup script prepares the Python dependencies and Playwright browser environment.

After setup, the application can be launched using the desktop shortcut created by the setup process.

> For development/debugging, `run.bat` can be used to launch the application while keeping the command window visible.

---

# 🚀 Usage

### 1. Launch the application

Open the desktop shortcut:

```text
Attendance Report Automation
```

### 2. Enter authorized credentials

Enter the attendance-system username/email and password.

Credentials should be entered at runtime and should not be hard-coded into the source code.

### 3. Enter sections

Enter one section per line:

```text
BTECH-ME-AY2627-SEM-03-A
BTECH-ME-AY2627-SEM-03-B
BTECH-ME-AY2627-SEM-03-C
```

### 4. Select the Excel output folder

Use **Browse...** to select the destination directory.

### 5. Start automation

Click:

```text
GENERATE EXCEL
```

The application processes the sections sequentially.

### 6. Monitor status

The status panel shows the current section and detailed progress.

### 7. Verify output

Open the selected output folder and verify the generated Excel files.

---

# 📊 Example Output

A typical output directory can contain:

```text
operation Shershaah/
│
├── Attendance_BTECH-ECE-AY2627-SEM-07-....xlsx
├── Attendance_BTECH-ME-AY2627-SEM-03-....xlsx
└── Attendance_BTECH-ME-AY2627-SEM-03-....xlsx
```

The exact filename depends on the section and the application's file-naming logic.

---

# 🧪 Testing

The automation should be tested against the following scenarios.

### Test 1 — Fresh Report

```text
Login
  ↓
Select Section
  ↓
Read Timestamp
  ↓
Report satisfies freshness condition
  ↓
Export
  ↓
Excel
  ↓
Download
```

**Expected:** The existing report proceeds to export without unnecessary regeneration.

### Test 2 — Report Requires Regeneration

```text
Login
  ↓
Select Section
  ↓
Read Timestamp
  ↓
Generate Now
  ↓
Wait
  ↓
Reload Report
  ↓
Continue
  ↓
Export
  ↓
Excel
  ↓
Download
```

**Expected:** The report is regenerated before export.

### Test 3 — Multiple Sections

```text
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
```

**Expected:** Sections are processed sequentially.

### Test 4 — Custom Output Folder

```text
Select Folder
      ↓
Run Automation
      ↓
Download Excel
      ↓
Verify File Location
```

**Expected:** The Excel file is saved in the selected directory.

### Test 5 — Stop Automation

```text
Automation Running
      ↓
STOP AUTOMATION
      ↓
Stop Request
      ↓
Automation Stops According to Current State
```

**Expected:** The user can request interruption of the running workflow.

---

# 🧩 Engineering Challenges

### Dynamic Web Application

The target website contains dynamically loaded elements and changing report states. The automation therefore interacts with browser elements and page states rather than relying only on fixed screen coordinates.

### Timestamp-Driven Workflow

A key challenge was determining when an existing report could be exported and when a new report needed to be generated.

The solution was to make report freshness part of the automation decision process.

### Multiple Sections

The automation must keep the correct section associated with its report and download before moving to the next section.

### Download Management

The application must wait for the Excel download and save it to the correct user-selected directory.

### GUI Responsiveness

Browser automation can involve network requests and waiting periods. Background execution helps prevent long-running automation from blocking the Tkinter interface.

### Deployment

The project also addresses the practical problem of running the application on Windows by providing a setup script and desktop-launch workflow.

---

# 🔐 Security

Credentials are entered at runtime.

**Never commit the following to GitHub:**

```text
Passwords
API keys
Authentication tokens
Session cookies
Private credentials
.env files containing secrets
```

The repository should contain the application source code and setup documentation, not authentication secrets.

---

# ⚠️ Limitations

This application is designed around the current workflow and interface of the target attendance web application.

Changes to the target website may require updates to the automation code, including changes to:

- HTML structure
- Element selectors
- Button names
- Login flow
- Student-group search
- Report-generation behavior
- Report reload behavior
- Export-menu structure
- Download behavior
- Authentication flow

The automation should only be used by users who are authorized to access the target system.

---

# 🔮 Future Improvements

Potential improvements include:

- More robust retry/recovery mechanisms
- Structured application logging
- Better download verification
- Network-failure recovery
- More resilient selectors
- Browser-crash recovery
- Unit tests for timestamp parsing
- Integration tests for the browser workflow
- Centralized configuration
- Standalone executable packaging
- Automatic update support
- Improved progress visualization
- More detailed user notifications

---

# 💼 Resume-Ready Project Description

### Attendance Report Automation | Python, Tkinter, Playwright

> Developed a Windows desktop application that automates multi-section attendance report generation and Excel export using Python and Playwright. Built a Tkinter GUI with timestamp-aware report processing, section verification, custom output directories, live status monitoring, background execution, download handling, and user-controlled start/stop functionality.

### Resume Bullet Points

- Developed a **Python + Playwright browser automation tool** to streamline multi-section attendance report generation and Excel export.
- Built a **Tkinter desktop GUI** supporting section management, custom output directories, live status monitoring, and user-controlled execution.
- Implemented **timestamp-aware decision logic** to determine whether an existing report can be exported or requires regeneration and reload.
- Designed a modular architecture separating **GUI and browser-automation responsibilities**, improving maintainability and debugging.
- Implemented **background execution and download handling** for long-running browser workflows while keeping the desktop interface responsive.
- Created a **Windows setup/launch workflow** and maintained the project using Git and GitHub.

---

# 🎯 Skills Demonstrated

### Programming
- Python
- Modular programming
- Exception handling
- File and directory management
- Regular expressions
- Background execution

### Automation
- Playwright
- Browser lifecycle management
- Dynamic web-element interaction
- Page navigation
- Report-state handling
- Download automation

### GUI Development
- Tkinter
- Event-driven programming
- User input handling
- Status/progress interfaces
- Background task integration

### Software Engineering
- Separation of concerns
- Workflow design
- Error handling
- Deployment scripting
- Version control
- Git/GitHub

---

# 📈 Project Impact

The project targets a repetitive administrative workflow and converts the repeated browser operations into a reusable desktop automation process.

Instead of manually repeating the report workflow for every section, the user can provide the required sections once and allow the application to process them sequentially.

This demonstrates practical application of:

**Problem identification → workflow analysis → automation design → GUI development → browser automation → file management → deployment**

---

# 👨‍💻 Author

**Teja Rayavarapu**

GitHub:  
https://github.com/teja23-saviour

Project Repository:  
https://github.com/teja23-saviour/attendance-report-automation

---

# 📄 License

This project is intended for educational and authorized institutional use.

Use the automation only when you have appropriate permission to access and automate the target attendance system.
