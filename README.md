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