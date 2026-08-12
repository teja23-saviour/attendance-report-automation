# Attendance Report Automation

A Windows desktop application that automates multi-section attendance report generation and Excel export using Python, Tkinter, and Playwright.

## Overview

Generating attendance reports for multiple student sections can involve repeatedly performing the same browser operations:

**Login → Select Section → Check Report → Generate/Reload if Required → Export → Download Excel**

This project automates that repetitive workflow through a Windows desktop application.

The user enters the required student sections, selects an output folder, and starts the automation. The application processes sections sequentially, verifies the selected section, checks the report state, performs the required browser actions, and saves the resulting Excel files to the selected directory.

## Problem

Manually collecting attendance reports becomes repetitive when the same report-generation and export workflow has to be performed for multiple sections.

## Solution

The application provides a reusable automation workflow that:

- Accepts multiple student sections.
- Searches for and verifies the requested section.
- Checks the current report timestamp/state.
- Determines whether the existing report can be exported.
- Generates and reloads the report when required.
- Navigates through the export workflow.
- Downloads the Excel report.
- Saves it to the user-selected output folder.
- Continues automatically with the next section.

## Features

- 🖥️ Windows desktop GUI using Tkinter
- 🔐 Runtime credential input
- 📝 Multiple section input
- 🔎 Student-group search and verification
- ⏱️ Timestamp-based report processing
- 🔄 Automatic report generation and reload when required
- 📤 Automated Excel export
- 📥 Automatic download handling
- 📁 Custom output folder selection
- 📊 Live automation status
- 🛑 Start/Stop automation controls
- 🔁 Sequential multi-section processing

## How It Works

```text
User
 │
 ├── Credentials
 ├── Student Sections
 └── Output Folder
          │
          ▼
     Tkinter GUI
          │
          ▼
  Start Automation
          │
          ▼
      Playwright
          │
          ▼
        Login
          │
          ▼
   Select & Verify Section
          │
          ▼
  Check Report Timestamp
          │
       ┌──┴──┐
       │     │
       ▼     ▼
    Ready   Regeneration
       │     Required
       │        │
       │        ▼
       │    Generate Report
       │        │
       │        ▼
       │     Reload Report
       │        │
       └────┬───┘
            │
            ▼
          Export
            │
            ▼
      Download Excel
            │
            ▼
     Save to Output Folder
            │
            ▼
      Process Next Section