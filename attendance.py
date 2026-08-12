import os
import threading
import time
import re
from datetime import datetime

from playwright.sync_api import sync_playwright


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://srkr.lightbooks.io"

LOGIN_URL = "https://srkr.lightbooks.io/login#login"

REPORT_URL = (
    "https://srkr.lightbooks.io/app/query-report/"
    "Student%20Cumulative%20Attendance"
)

REPORT_MAX_AGE_MINUTES = 60
REPORT_GENERATION_WAIT_SECONDS = 120


class AutomationError(Exception):
    """Expected automation failure shown by the GUI."""
    pass



# ============================================================
# GLOBAL STOP EVENT
# ============================================================

_stop_event = threading.Event()


def stop_automation():
    """Request the automation to stop."""
    _stop_event.set()


def reset_stop():
    _stop_event.clear()


def check_stop():
    """Stop immediately if the user requested it."""
    if _stop_event.is_set():
        raise RuntimeError("Automation stopped by user.")


# ============================================================
# MAIN AUTOMATION
# ============================================================

def run_automation(
    username,
    password,
    student_groups,
    status_callback=None,
    download_folder=None
):
    """
    Login, generate and download attendance Excel files.

    Important behavior:
    - Browser stays open after successful downloads.
    - Browser also stays open if an automation error occurs.
    - Browser closes only after stop_automation() is called.
    """

    reset_stop()

    def status(message):
        print(message)
        if status_callback:
            status_callback(message)

    # --------------------------------------------------------
    # DOWNLOAD DIRECTORY
    # --------------------------------------------------------

    if download_folder:
        download_folder = os.path.abspath(os.path.expanduser(download_folder))
    else:
        download_folder = os.path.join(os.getcwd(), "downloads")

    os.makedirs(download_folder, exist_ok=True)
    status(f"Excel output folder: {download_folder}")

    # --------------------------------------------------------
    # NORMALIZE STUDENT GROUPS
    # --------------------------------------------------------

    if isinstance(student_groups, str):
        student_groups = [student_groups]

    student_groups = [
        str(group).strip()
        for group in student_groups
        if str(group).strip()
    ]

    if not student_groups:
        raise ValueError("No Student Groups were provided.")

    playwright = None
    browser = None
    context = None
    downloaded_files = []

    try:
        # ====================================================
        # START PLAYWRIGHT
        # ====================================================

        status("Starting Playwright...")

        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=250
        )

        context = browser.new_context(
            accept_downloads=True
        )

        page = context.new_page()

        # ====================================================
        # LOGIN
        # ====================================================

        status("Opening Lightbooks login page...")

        page.goto(
            LOGIN_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        status("Login page opened.")

        # The inspected page uses #login_email.
        # Fallbacks are included for minor page changes.
        username_candidates = [
            page.locator("#login_email"),
            page.locator(
                'input[name="usr"], '
                'input[name="username"], '
                'input[type="email"], '
                'input[type="text"]'
            )
        ]

        username_box = None

        for candidate in username_candidates:
            try:
                candidate.first.wait_for(
                    state="visible",
                    timeout=5000
                )
                username_box = candidate.first
                break
            except Exception:
                pass

        if username_box is None:
            raise RuntimeError(
                "Could not find the username/email field."
            )

        password_box = page.locator(
            'input[type="password"]'
        ).first

        password_box.wait_for(
            state="visible",
            timeout=30000
        )

        status("Entering credentials...")

        username_box.fill(username)
        password_box.fill(password)

        check_stop()

        # ====================================================
        # LOGIN BUTTON
        # ====================================================

        login_button = page.get_by_role(
            "button",
            name="Login",
            exact=True
        )

        login_button.wait_for(
            state="visible",
            timeout=30000
        )

        login_button.click()

        status("Login clicked.")

        page.wait_for_timeout(5000)

        check_stop()

        if "/login" in page.url.lower():
            raise RuntimeError(
                "Login was not completed. "
                "Please check the username/password."
            )

        status("=" * 65)
        status("LOGIN SUCCESSFUL")
        status("=" * 65)

        # ====================================================
        # OPEN REPORT
        # ====================================================

        status("Opening Student Cumulative Attendance...")

        page.goto(
            REPORT_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        check_stop()

        status("Attendance report page opened.")

        # ====================================================
        # PROCESS EACH SECTION
        # ====================================================

        for section_number, student_group in enumerate(
            student_groups,
            start=1
        ):
            check_stop()

            status("")
            status("=" * 65)
            status(
                f"SECTION {section_number} "
                f"OF {len(student_groups)}"
            )
            status("=" * 65)

            status(
                f"Requested Student Group: {student_group}"
            )

            # =================================================
            # FIND STUDENT GROUP FIELD
            # =================================================

            status("Finding Student Group field...")

            group_input = page.locator(
                'input[data-fieldname="student_group"]'
            ).first

            try:
                group_input.wait_for(
                    state="visible",
                    timeout=15000
                )
            except Exception:
                group_input = page.get_by_placeholder(
                    "Student Group"
                ).first

                group_input.wait_for(
                    state="visible",
                    timeout=15000
                )

            status("Student Group field found.")

            # =================================================
            # ENTER SECTION
            # =================================================

            group_input.click()

            group_input.fill("")

            status(
                f"Entering section: {student_group}"
            )

            group_input.fill(student_group)

            page.wait_for_timeout(2000)

            check_stop()

            status(
                "Waiting for matching sections..."
            )

            # =================================================
            # SELECT EXACT OPTION
            # =================================================

            selected = False

            options = page.locator(
                '[role="option"]:visible'
            )

            for i in range(options.count()):
                check_stop()

                option = options.nth(i)

                try:
                    option_text = (
                        option.inner_text()
                        .strip()
                    )

                    if (
                        option_text == student_group
                        or option_text.startswith(
                            student_group + " "
                        )
                        or option_text.startswith(
                            student_group + "\n"
                        )
                    ):
                        status(
                            "Exact Student Group "
                            "found in suggestions."
                        )

                        option.click()

                        selected = True
                        break

                except Exception:
                    pass

            # =================================================
            # KEYBOARD FALLBACK
            # =================================================

            if not selected:
                status(
                    "Exact option not directly found."
                )
                status(
                    "Trying keyboard selection..."
                )

                group_input.press("ArrowDown")
                group_input.press("Enter")

                page.wait_for_timeout(1000)

                try:
                    selected = (
                        group_input.input_value().strip()
                        == student_group
                    )
                except Exception:
                    selected = False

            # =================================================
            # FINAL OPTION CHECK
            # =================================================

            if not selected:
                options = page.locator(
                    '[role="option"]:visible'
                )

                for i in range(options.count()):
                    check_stop()

                    option = options.nth(i)

                    try:
                        text = (
                            option.inner_text()
                            .strip()
                        )

                        if text.startswith(student_group):
                            option.click()
                            selected = True
                            break

                    except Exception:
                        pass

            if not selected:
                raise RuntimeError(
                    "Could not select Student Group:\n"
                    f"{student_group}\n\n"
                    "Lightbooks did not show an exact "
                    "matching Student Group."
                )

            # =================================================
            # VERIFY SELECTED VALUE
            # =================================================

            page.wait_for_timeout(500)

            selected_value = (
                group_input.input_value()
                .strip()
            )

            status(
                f"Selected value: {selected_value}"
            )

            if selected_value != student_group:
                raise RuntimeError(
                    "Student Group selection verification failed.\n\n"
                    f"Requested: {student_group}\n"
                    f"Selected: {selected_value}"
                )

            status(
                "Student Group selection verified."
            )

            # =================================================
            # CHECK REPORT TIMESTAMP BEFORE GENERATE
            # =================================================

            status("Checking report timestamp before Generate New Report...")

            def get_timestamp_text():
                """Read only the visible Lightbooks report-generated message."""
                candidates = [
                    page.locator("div.form-message.text-muted.small"),
                    page.get_by_text(re.compile(r"This report was generated", re.I)),
                ]

                for locator in candidates:
                    try:
                        for i in range(locator.count()):
                            item = locator.nth(i)
                            if not item.is_visible():
                                continue
                            text = " ".join(item.inner_text().split())
                            if "report was generated" in text.lower():
                                match = re.search(
                                    r"This report was generated\s+(.+?)(?:\.|$)",
                                    text,
                                    flags=re.IGNORECASE,
                                )
                                if match:
                                    return match.group(0).strip()
                    except Exception:
                        pass

                raise AutomationError(
                    "Could not find the Lightbooks report timestamp message.\n"
                    "Expected text like: 'This report was generated 5 minutes ago.'"
                )

            def timestamp_age_minutes(text):
                t = " ".join(text.lower().split())
                if "just now" in t:
                    return 0

                m = re.search(r"\b(\d+)\s+minute(?:s)?\b", t)
                if m:
                    return int(m.group(1))
                if re.search(r"\b(?:a|an)\s+minute\b", t):
                    return 1

                h = re.search(r"\b(\d+)\s+hour(?:s)?\b", t)
                if h:
                    return int(h.group(1)) * 60
                if re.search(r"\b(?:a|an)\s+hour\b", t):
                    return 60

                d = re.search(r"\b(\d+)\s+day(?:s)?\b", t)
                if d:
                    return int(d.group(1)) * 1440
                if "yesterday" in t or re.search(r"\b(?:a|an)\s+day\b", t):
                    return 1440

                raise AutomationError(f"Could not understand report timestamp:\n{text}")

            timestamp = get_timestamp_text()
            age_minutes = timestamp_age_minutes(timestamp)

            status(f"TIMESTAMP READ: {timestamp}")
            status(f"AGE CALCULATED: {age_minutes} minute(s)")

            if age_minutes < REPORT_MAX_AGE_MINUTES:
                status("REPORT IS FRESH (< 1 HOUR).")
                status("TIMESTAMP IS LESS THAN 1 HOUR. DO NOT click Generate New Report.")

            else:
                status("REPORT IS OLDER THAN 1 HOUR.")
                status("Generate New Report is required.")

                # -------------------------------------------------
                # GENERATE NEW REPORT
                # -------------------------------------------------
                status("Clicking Generate New Report...")

                generate_button = page.locator(
                    'button[data-label="Generate%20New%20Report"]'
                )

                if generate_button.count() == 0:
                    generate_button = page.get_by_role(
                        "button",
                        name="Generate New Report",
                        exact=True
                    )

                generate_button.wait_for(
                    state="visible",
                    timeout=15000
                )

                # Pick the visible/enabled Generate button.
                clicked_generate = False
                for i in range(generate_button.count()):
                    candidate = generate_button.nth(i)
                    try:
                        if candidate.is_visible() and candidate.is_enabled():
                            candidate.click()
                            clicked_generate = True
                            break
                    except Exception:
                        pass

                if not clicked_generate:
                    raise AutomationError(
                        "Generate New Report button was found but could not be clicked."
                    )

                status("Generate New Report clicked.")
                status("REPORT GENERATION WAIT: 2 minutes")

                # -------------------------------------------------
                # EXACTLY THE REQUESTED 2-MINUTE WAIT
                # -------------------------------------------------
                remaining = REPORT_GENERATION_WAIT_SECONDS
                while remaining > 0:
                    check_stop()
                    if remaining % 10 == 0 or remaining <= 5:
                        status(f"Waiting for report generation: {remaining} seconds remaining")
                    time.sleep(1)
                    remaining -= 1

                status("2-minute report generation wait completed.")

                # -------------------------------------------------
                # IMPORTANT: LIGHTBOOKS REPORT RELOAD BUTTON
                # NOT browser/page.reload()
                # -------------------------------------------------
                status("Finding Lightbooks 'Reload Report' button...")

                reload_button = page.locator(
                    'button[data-original-title="Reload Report"]'
                )

                reload_candidate = None
                deadline = time.time() + 20

                while time.time() < deadline:
                    check_stop()
                    try:
                        for i in range(reload_button.count()):
                            candidate = reload_button.nth(i)
                            if candidate.is_visible() and candidate.is_enabled():
                                reload_candidate = candidate
                                break
                    except Exception:
                        pass

                    if reload_candidate is not None:
                        break
                    time.sleep(0.5)

                if reload_candidate is None:
                    raise AutomationError(
                        "Lightbooks 'Reload Report' button was not found. "
                        "Browser reload was NOT used."
                    )

                status("Clicking Lightbooks 'Reload Report'...")
                reload_candidate.click()
                status("Lightbooks 'Reload Report' clicked successfully.")

                # -------------------------------------------------
                # WAIT FOR THE REPORT TO REFRESH AND READ TIMESTAMP
                # AGAIN. DO NOT EXPORT BEFORE THIS CHECK.
                # -------------------------------------------------
                status("Waiting for the refreshed report to load...")
                page.wait_for_timeout(3000)

                refreshed_timestamp = None
                refreshed_age = None
                refreshed_deadline = time.time() + 30

                while time.time() < refreshed_deadline:
                    check_stop()
                    try:
                        refreshed_timestamp = get_timestamp_text()
                        refreshed_age = timestamp_age_minutes(refreshed_timestamp)
                        status(f"TIMESTAMP AFTER RELOAD: {refreshed_timestamp}")
                        status(f"AGE AFTER RELOAD: {refreshed_age} minute(s)")
                        break
                    except AutomationError:
                        time.sleep(1)

                if refreshed_timestamp is None or refreshed_age is None:
                    raise AutomationError(
                        "Report Reload was clicked, but the refreshed report timestamp "
                        "could not be read within 30 seconds."
                    )

                if refreshed_age >= REPORT_MAX_AGE_MINUTES:
                    raise AutomationError(
                        "Report Reload completed, but the report is still 1 hour old or older.\n\n"
                        f"Timestamp: {refreshed_timestamp}\n"
                        f"Age: {refreshed_age} minute(s)"
                    )

                status("REPORT IS FRESH AFTER RELOAD (< 1 HOUR).")
                status("Proceeding to Menu -> Export -> Excel.")

            # =================================================
            # EXPORT MENU
            # =================================================

            status("Opening report menu...")

            menu_buttons = page.locator(
                'button[aria-label="Menu"]'
            )

            report_menu = None

            for i in range(menu_buttons.count()):
                candidate = menu_buttons.nth(i)

                try:
                    if candidate.is_visible():
                        report_menu = candidate
                        break
                except Exception:
                    pass

            if report_menu is None:
                raise RuntimeError(
                    "Report Menu button not found."
                )

            report_menu.click()

            page.wait_for_timeout(800)

            # =================================================
            # EXPORT
            # =================================================

            status("Selecting Export...")

            export_items = page.get_by_text(
                "Export",
                exact=True
            )

            export_clicked = False

            for i in range(export_items.count()):
                item = export_items.nth(i)

                try:
                    if item.is_visible():
                        item.click()
                        export_clicked = True
                        break
                except Exception:
                    pass

            if not export_clicked:
                raise RuntimeError(
                    "Export option not found."
                )

            status("Export dialog opened.")

            page.wait_for_timeout(1200)

            # =================================================
            # EXPORT MODAL
            # =================================================

            export_modal = page.locator(
                'div.modal.show[role="dialog"]'
            ).last

            export_modal.wait_for(
                state="visible",
                timeout=10000
            )

            status(
                "Export Report dialog detected."
            )

            # =================================================
            # SELECT EXCEL
            # =================================================

            status("Selecting Excel...")

            format_select = export_modal.locator(
                'select[data-fieldname="file_format"]'
            )

            format_select.wait_for(
                state="visible",
                timeout=10000
            )

            format_select.select_option(
                label="Excel"
            )

            status("Excel selected.")

            # =================================================
            # DOWNLOAD BUTTON
            # =================================================

            status("Finding Download button...")

            download_buttons = export_modal.locator(
                "button.btn-modal-primary"
            )

            visible_download = None

            for i in range(download_buttons.count()):
                candidate = download_buttons.nth(i)

                try:
                    if (
                        candidate.is_visible()
                        and candidate.inner_text().strip()
                        == "Download"
                    ):
                        visible_download = candidate
                        break
                except Exception:
                    pass

            if visible_download is None:
                visible_download = export_modal.get_by_text(
                    "Download",
                    exact=True
                ).last

            visible_download.wait_for(
                state="visible",
                timeout=10000
            )

            # =================================================
            # DOWNLOAD
            # =================================================

            check_stop()

            status("Downloading Excel...")

            with page.expect_download(
                timeout=60000
            ) as download_info:
                visible_download.click()

            download = download_info.value

            # =================================================
            # SAVE FILE
            # =================================================

            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            safe_group = "".join(
                c
                if c.isalnum() or c in "-_"
                else "_"
                for c in student_group
            )

            filename = (
                f"Attendance_"
                f"{safe_group}_"
                f"{timestamp}.xlsx"
            )

            file_path = os.path.join(
                download_folder,
                filename
            )

            download.save_as(file_path)

            downloaded_files.append(file_path)

            status(
                f"Downloaded:\n{file_path}"
            )

            status(
                f"Section completed: {student_group}"
            )

            page.wait_for_timeout(1500)

        # ====================================================
        # SUCCESS
        # ====================================================

        status("")
        status("=" * 65)
        status("ALL SECTIONS COMPLETED")
        status("=" * 65)

        status(
            f"Total Excel files: {len(downloaded_files)}"
        )

        for file_path in downloaded_files:
            status(file_path)

        status("")
        status("Browser will remain OPEN.")
        status(
            "Press STOP AUTOMATION or close the "
            "application when finished."
        )

        # ====================================================
        # WAIT FOREVER UNTIL USER STOPS
        # ====================================================

        while not _stop_event.is_set():
            time.sleep(0.5)

        status("Stop requested.")

        return downloaded_files

    except Exception as error:
        # ====================================================
        # ERROR
        #
        # IMPORTANT:
        # DO NOT CLOSE THE BROWSER HERE.
        # DO NOT immediately re-raise.
        #
        # The browser remains open so the user can inspect it.
        # ====================================================

        status("")
        status("=" * 65)
        status("AUTOMATION ERROR")
        status("=" * 65)
        status(str(error))
        status("")
        status("Browser will remain OPEN.")
        status(
            "Inspect the browser if needed."
        )
        status(
            "Press STOP AUTOMATION to close it."
        )
        status("=" * 65)

        # Wait until the user explicitly stops automation.
        while not _stop_event.is_set():
            time.sleep(0.5)

        status("")
        status("STOP RECEIVED.")
        status("Closing browser...")

        # Re-raise only AFTER the user has stopped.
        raise

    finally:
        # ====================================================
        # BROWSER CLEANUP
        #
        # This runs after success+stop OR error+stop.
        # ====================================================

        try:
            if context:
                context.close()
        except Exception:
            pass

        try:
            if browser:
                browser.close()
        except Exception:
            pass

        try:
            if playwright:
                playwright.stop()
        except Exception:
            pass