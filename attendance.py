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

# Reports younger than this are exported directly.
REPORT_MAX_AGE_MINUTES = 60

# Wait after clicking Generate New Report.
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
# HELPER: TIMESTAMP
# ============================================================

def timestamp_age_minutes(text):
    """
    Convert Lightbooks report timestamp text into minutes.

    Examples:
        just now       -> 0
        5 minutes ago  -> 5
        1 hour ago     -> 60
        14 hours ago   -> 840
        yesterday      -> 1440
        2 days ago     -> 2880
    """

    t = " ".join(text.lower().split())

    if "just now" in t:
        return 0

    # Minutes
    match = re.search(r"\b(\d+)\s+minute(?:s)?\b", t)

    if match:
        return int(match.group(1))

    if re.search(r"\b(?:a|an)\s+minute\b", t):
        return 1

    # Hours
    match = re.search(r"\b(\d+)\s+hour(?:s)?\b", t)

    if match:
        return int(match.group(1)) * 60

    if re.search(r"\b(?:a|an)\s+hour\b", t):
        return 60

    # Days
    match = re.search(r"\b(\d+)\s+day(?:s)?\b", t)

    if match:
        return int(match.group(1)) * 1440

    if "yesterday" in t:
        return 1440

    if re.search(r"\b(?:a|an)\s+day\b", t):
        return 1440

    raise AutomationError(
        f"Could not understand report timestamp:\n{text}"
    )


# ============================================================
# HELPER: READ REPORT TIMESTAMP
# ============================================================

def get_timestamp_text(page):
    """
    Read the visible Lightbooks report-generated message.
    """

    candidates = [
        page.locator("div.form-message.text-muted.small"),
        page.get_by_text(
            re.compile(
                r"This report was generated",
                re.IGNORECASE
            )
        ),
    ]

    for locator in candidates:

        try:

            count = locator.count()

            for i in range(count):

                item = locator.nth(i)

                try:
                    if not item.is_visible():
                        continue
                except Exception:
                    continue

                try:
                    text = " ".join(
                        item.inner_text().split()
                    )
                except Exception:
                    continue

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
        "Expected text like:\n"
        "'This report was generated 5 minutes ago.'"
    )


# ============================================================
# HELPER: FIND STUDENT GROUP INPUT
# ============================================================

def find_student_group_input(page):
    """
    Always locate a fresh Student Group input.

    This is intentionally called again after every full page reload.
    """

    selectors = [
        'input[data-fieldname="student_group"]',
        'input[placeholder="Student Group"]',
        'input[placeholder*="Student Group"]',
    ]

    deadline = time.time() + 30

    while time.time() < deadline:

        check_stop()

        for selector in selectors:

            try:

                locator = page.locator(selector)

                count = locator.count()

                for i in range(count):

                    candidate = locator.nth(i)

                    try:

                        if candidate.is_visible():

                            candidate.scroll_into_view_if_needed(
                                timeout=3000
                            )

                            return candidate

                    except Exception:
                        pass

            except Exception:
                pass

        page.wait_for_timeout(500)

    raise AutomationError(
        "Could not find Student Group input after page reload."
    )


# ============================================================
# HELPER: SELECT STUDENT GROUP
# ============================================================

def select_student_group(page, student_group, status):
    """
    Enter and select the exact Student Group.

    This does NOT rely only on [role='option'] because
    Lightbooks can render autocomplete suggestions using
    different HTML structures.
    """

    status("Finding Student Group field...")

    group_input = find_student_group_input(page)

    status("Student Group field found.")

    # --------------------------------------------------------
    # CLEAR OLD VALUE
    # --------------------------------------------------------

    try:
        group_input.click()
    except Exception:
        pass

    try:
        group_input.press("Control+A")
        group_input.press("Backspace")
    except Exception:
        pass

    try:
        group_input.fill("")
    except Exception:
        pass

    # --------------------------------------------------------
    # ENTER NEW SECTION
    # --------------------------------------------------------

    status(
        f"Entering section: {student_group}"
    )

    group_input.fill(student_group)

    check_stop()

    status("Waiting for matching sections...")

    # Give autocomplete time to appear.
    page.wait_for_timeout(2000)

    # --------------------------------------------------------
    # POSSIBLE AUTOCOMPLETE SELECTORS
    # --------------------------------------------------------

    dropdown_selectors = [

        '[role="option"]:visible',

        '.awesomplete li:visible',

        '.ui-autocomplete li:visible',

        '.ui-menu-item:visible',

        '.dropdown-menu li:visible',

        '.awesomplete ul li:visible',

        'ul[role="listbox"] li:visible',

        'li:visible',

    ]

    deadline = time.time() + 20

    while time.time() < deadline:

        check_stop()

        # ====================================================
        # FIRST: LOOK FOR EXACT TEXT
        # ====================================================

        for selector in dropdown_selectors:

            try:

                elements = page.locator(selector)

                count = elements.count()

                for i in range(count):

                    check_stop()

                    item = elements.nth(i)

                    try:

                        if not item.is_visible():
                            continue

                    except Exception:
                        continue

                    try:
                        text = " ".join(
                            item.inner_text().split()
                        )
                    except Exception:
                        continue

                    # Exact match
                    if text == student_group:

                        status(
                            "Exact Student Group found in suggestions."
                        )

                        try:
                            item.scroll_into_view_if_needed(
                                timeout=3000
                            )
                        except Exception:
                            pass

                        try:
                            item.click(timeout=5000)

                        except Exception:

                            try:
                                item.click(
                                    timeout=5000,
                                    force=True
                                )
                            except Exception:
                                continue

                        page.wait_for_timeout(1000)

                        # Verify
                        try:

                            selected_value = (
                                group_input.input_value()
                                .strip()
                            )

                        except Exception:

                            selected_value = ""

                        if selected_value == student_group:

                            status(
                                f"Selected value: {selected_value}"
                            )

                            status(
                                "Student Group selection verified."
                            )

                            return group_input

                    # Some Lightbooks entries may contain
                    # extra information after the section.
                    if text.startswith(student_group + " "):
                        try:

                            item.scroll_into_view_if_needed(
                                timeout=3000
                            )

                            item.click(timeout=5000)

                            page.wait_for_timeout(1000)

                            selected_value = (
                                group_input.input_value()
                                .strip()
                            )

                            if selected_value == student_group:

                                status(
                                    f"Selected value: {selected_value}"
                                )

                                status(
                                    "Student Group selection verified."
                                )

                                return group_input

                        except Exception:
                            pass

            except Exception:
                pass

        # ====================================================
        # SECOND: USE PAGE TEXT SEARCH
        # ====================================================

        try:

            exact_text = page.get_by_text(
                student_group,
                exact=True
            )

            count = exact_text.count()

            for i in range(count):

                check_stop()

                item = exact_text.nth(i)

                try:

                    if not item.is_visible():
                        continue

                    item.scroll_into_view_if_needed(
                        timeout=3000
                    )

                    item.click(timeout=5000)

                    page.wait_for_timeout(1000)

                    selected_value = (
                        group_input.input_value()
                        .strip()
                    )

                    if selected_value == student_group:

                        status(
                            "Exact Student Group selected."
                        )

                        status(
                            f"Selected value: {selected_value}"
                        )

                        status(
                            "Student Group selection verified."
                        )

                        return group_input

                except Exception:
                    pass

        except Exception:
            pass

        # ====================================================
        # THIRD: KEYBOARD FALLBACK
        # ====================================================

        try:

            group_input.press("ArrowDown")

            page.wait_for_timeout(300)

            group_input.press("Enter")

            page.wait_for_timeout(1000)

            selected_value = (
                group_input.input_value()
                .strip()
            )

            if selected_value == student_group:

                status(
                    f"Selected value: {selected_value}"
                )

                status(
                    "Student Group selection verified."
                )

                return group_input

        except Exception:
            pass

        page.wait_for_timeout(500)

    # --------------------------------------------------------
    # FINAL FAILURE
    # --------------------------------------------------------

    try:
        current_value = group_input.input_value().strip()
    except Exception:
        current_value = ""

    raise AutomationError(
        "Could not select Student Group:\n"
        f"{student_group}\n\n"
        f"Current input value: {current_value}\n\n"
        "The exact section was not selected."
    )


# ============================================================
# HELPER: FULL PAGE RELOAD BEFORE NEW SECTION
# ============================================================

def reload_page_before_section(page, status):
    """
    IMPORTANT:

    This is a FULL browser page reload.

    It is NOT the Lightbooks 'Reload Report' button.

    This function is called before every section after
    the first section.
    """

    status("")
    status(
        "Reloading the FULL attendance webpage "
        "before the next section..."
    )

    check_stop()

    page.reload(
        wait_until="domcontentloaded",
        timeout=60000
    )

    status("Full webpage reload completed.")

    # Allow Lightbooks frontend to initialize.
    page.wait_for_timeout(5000)

    check_stop()

    # Make sure Student Group field has returned.
    status(
        "Waiting for Student Group field after page reload..."
    )

    find_student_group_input(page)

    status(
        "Attendance page is ready for the next section."
    )


# ============================================================
# HELPER: GENERATE NEW REPORT
# ============================================================

def generate_new_report(page, status):
    """
    Find and click Generate New Report.

    The button is located fresh on every attempt.
    """

    status(
        "Preparing Generate New Report button..."
    )

    selectors = [

        'button[data-label="Generate%20New%20Report"]',

        'button[data-label="Generate New Report"]',

        'button:has-text("Generate New Report")',

    ]

    deadline = time.time() + 45

    last_error = None

    while time.time() < deadline:

        check_stop()

        for selector in selectors:

            try:

                buttons = page.locator(selector)

                count = buttons.count()

                for i in range(count):

                    check_stop()

                    button = buttons.nth(i)

                    try:

                        if not button.is_visible():
                            continue

                    except Exception:
                        continue

                    try:

                        button.scroll_into_view_if_needed(
                            timeout=3000
                        )

                    except Exception:
                        pass

                    try:

                        if not button.is_enabled():
                            continue

                    except Exception:
                        continue

                    # Normal click
                    try:

                        button.click(
                            timeout=5000
                        )

                        status(
                            "Generate New Report clicked."
                        )

                        return

                    except Exception as error:

                        last_error = error

                    # Force click fallback
                    try:

                        if (
                            button.is_visible()
                            and button.is_enabled()
                        ):

                            button.click(
                                timeout=3000,
                                force=True
                            )

                            status(
                                "Generate New Report clicked."
                            )

                            return

                    except Exception as error:

                        last_error = error

            except Exception as error:

                last_error = error

        # Give Lightbooks time to finish rendering.
        page.wait_for_timeout(1000)

    detail = ""

    if last_error:
        detail = (
            f"\nLast click error: {last_error}"
        )

    raise AutomationError(
        "Generate New Report button was found "
        "but could not be clicked after 45 seconds."
        + detail
    )


# ============================================================
# HELPER: WAIT FOR REPORT GENERATION
# ============================================================

def wait_for_generation(status):
    """
    Wait exactly 2 minutes after Generate New Report.
    """

    status(
        "REPORT GENERATION WAIT: 2 minutes"
    )

    remaining = REPORT_GENERATION_WAIT_SECONDS

    while remaining > 0:

        check_stop()

        if (
            remaining % 10 == 0
            or remaining <= 5
        ):

            status(
                "Waiting for report generation: "
                f"{remaining} seconds remaining"
            )

        time.sleep(1)

        remaining -= 1

    status(
        "2-minute report generation wait completed."
    )


# ============================================================
# HELPER: LIGHTBOOKS RELOAD REPORT
# ============================================================

def reload_report(page, status):
    """
    Click Lightbooks' Reload Report button.

    This is NOT page.reload().
    """

    status(
        "Finding Lightbooks 'Reload Report' button..."
    )

    selector = (
        'button[data-original-title="Reload Report"]'
    )

    deadline = time.time() + 30

    while time.time() < deadline:

        check_stop()

        try:

            buttons = page.locator(selector)

            for i in range(buttons.count()):

                candidate = buttons.nth(i)

                try:

                    if (
                        candidate.is_visible()
                        and candidate.is_enabled()
                    ):

                        candidate.scroll_into_view_if_needed(
                            timeout=3000
                        )

                        status(
                            "Clicking Lightbooks "
                            "'Reload Report'..."
                        )

                        candidate.click(
                            timeout=5000
                        )

                        status(
                            "Lightbooks 'Reload Report' "
                            "clicked successfully."
                        )

                        return

                except Exception:
                    pass

        except Exception:
            pass

        page.wait_for_timeout(500)

    raise AutomationError(
        "Lightbooks 'Reload Report' button "
        "was not found."
    )


# ============================================================
# HELPER: VERIFY FRESH REPORT AFTER RELOAD
# ============================================================

def wait_for_fresh_report(page, status):
    """
    After Generate New Report + Reload Report,
    repeatedly check the timestamp.

    We do NOT assume that one reload immediately
    produces 'just now'.
    """

    status(
        "Waiting for the refreshed report to load..."
    )

    deadline = time.time() + 60

    last_timestamp = None
    last_age = None

    while time.time() < deadline:

        check_stop()

        try:

            timestamp = get_timestamp_text(page)

            age = timestamp_age_minutes(timestamp)

            # Only print when the value changes.
            if (
                timestamp != last_timestamp
                or age != last_age
            ):

                status(
                    f"TIMESTAMP AFTER RELOAD: {timestamp}"
                )

                status(
                    f"AGE AFTER RELOAD: {age} minute(s)"
                )

                last_timestamp = timestamp
                last_age = age

            if age < REPORT_MAX_AGE_MINUTES:

                status(
                    "REPORT IS FRESH AFTER RELOAD "
                    "(< 1 HOUR)."
                )

                return

        except Exception:
            pass

        # Give Lightbooks time to update.
        page.wait_for_timeout(3000)

    raise AutomationError(
        "Report generation/reload completed, "
        "but the report did not become fresh "
        "within the allowed waiting period.\n\n"
        f"Last timestamp: {last_timestamp}\n"
        f"Last age: {last_age} minute(s)"
    )


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
    Login, process multiple Student Groups,
    generate/reload reports when required,
    and download Excel files.

    IMPORTANT:
    Before every new section after Section 1,
    the ENTIRE WEBPAGE is reloaded using page.reload().
    """

    reset_stop()

    def status(message):
        print(message)

        if status_callback:
            status_callback(message)

    # ========================================================
    # DOWNLOAD DIRECTORY
    # ========================================================

    if download_folder:

        download_folder = os.path.abspath(
            os.path.expanduser(download_folder)
        )

    else:

        download_folder = os.path.join(
            os.getcwd(),
            "downloads"
        )

    os.makedirs(
        download_folder,
        exist_ok=True
    )

    status(
        f"Excel output folder: {download_folder}"
    )

    # ========================================================
    # NORMALIZE STUDENT GROUPS
    # ========================================================

    if isinstance(student_groups, str):

        student_groups = [
            student_groups
        ]

    student_groups = [
        str(group).strip()
        for group in student_groups
        if str(group).strip()
    ]

    if not student_groups:

        raise ValueError(
            "No Student Groups were provided."
        )

    # ========================================================
    # PLAYWRIGHT VARIABLES
    # ========================================================

    playwright = None
    browser = None
    context = None

    downloaded_files = []

    try:

        # ====================================================
        # START PLAYWRIGHT
        # ====================================================

        status(
            "Starting Playwright..."
        )

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

        status(
            "Opening Lightbooks login page..."
        )

        page.goto(
            LOGIN_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        status(
            "Login page opened."
        )

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        username_candidates = [

            page.locator(
                "#login_email"
            ),

            page.locator(
                'input[name="usr"]'
            ),

            page.locator(
                'input[name="username"]'
            ),

            page.locator(
                'input[type="email"]'
            ),

            page.locator(
                'input[type="text"]'
            ),

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

            raise AutomationError(
                "Could not find username/email field."
            )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password_box = page.locator(
            'input[type="password"]'
        ).first

        password_box.wait_for(
            state="visible",
            timeout=30000
        )

        # ----------------------------------------------------
        # ENTER CREDENTIALS
        # ----------------------------------------------------

        status(
            "Entering credentials..."
        )

        username_box.fill(username)

        password_box.fill(password)

        check_stop()

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

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

        status(
            "Login clicked."
        )

        page.wait_for_timeout(5000)

        check_stop()

        if "/login" in page.url.lower():

            raise AutomationError(
                "Login was not completed. "
                "Please check username/password."
            )

        status("=" * 65)

        status(
            "LOGIN SUCCESSFUL"
        )

        status("=" * 65)

        # ====================================================
        # OPEN REPORT
        # ====================================================

        status(
            "Opening Student Cumulative Attendance..."
        )

        page.goto(
            REPORT_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        check_stop()

        status(
            "Attendance report page opened."
        )

        # ====================================================
        # PROCESS EVERY SECTION
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
                f"Requested Student Group: "
                f"{student_group}"
            )

            # =================================================
            # IMPORTANT:
            # FULL PAGE RELOAD BEFORE EVERY NEW SECTION
            # =================================================

            if section_number > 1:

                reload_page_before_section(
                    page,
                    status
                )

            # =================================================
            # SELECT STUDENT GROUP
            # =================================================

            group_input = select_student_group(
                page,
                student_group,
                status
            )

            # =================================================
            # WAIT FOR SELECTED SECTION REPORT
            # =================================================

            status(
                "Waiting for the selected section "
                "report to load..."
            )

            page.wait_for_timeout(3000)

            check_stop()

            # =================================================
            # READ REPORT TIMESTAMP
            # =================================================

            status(
                "Checking report timestamp before "
                "Generate New Report..."
            )

            timestamp = get_timestamp_text(page)

            age_minutes = timestamp_age_minutes(
                timestamp
            )

            status(
                f"TIMESTAMP READ: {timestamp}"
            )

            status(
                f"AGE CALCULATED: "
                f"{age_minutes} minute(s)"
            )

            # =================================================
            # FRESH REPORT
            # =================================================

            if age_minutes < REPORT_MAX_AGE_MINUTES:

                status(
                    "REPORT IS FRESH (< 1 HOUR)."
                )

                status(
                    "TIMESTAMP IS LESS THAN 1 HOUR. "
                    "DO NOT click Generate New Report."
                )

            # =================================================
            # OLD REPORT
            # =================================================

            else:

                status(
                    "REPORT IS OLDER THAN 1 HOUR."
                )

                status(
                    "Generate New Report is required."
                )

                # -------------------------------------------------
                # GENERATE
                # -------------------------------------------------

                generate_new_report(
                    page,
                    status
                )

                # -------------------------------------------------
                # WAIT 2 MINUTES
                # -------------------------------------------------

                wait_for_generation(
                    status
                )

                # -------------------------------------------------
                # LIGHTBOOKS RELOAD REPORT
                # -------------------------------------------------

                reload_report(
                    page,
                    status
                )

                # -------------------------------------------------
                # WAIT UNTIL REPORT ACTUALLY BECOMES FRESH
                # -------------------------------------------------

                wait_for_fresh_report(
                    page,
                    status
                )

                status(
                    "Proceeding to Menu -> Export -> Excel."
                )

            # =================================================
            # OPEN REPORT MENU
            # =================================================

            status(
                "Opening report menu..."
            )

            menu_buttons = page.locator(
                'button[aria-label="Menu"]'
            )

            report_menu = None

            for i in range(
                menu_buttons.count()
            ):

                candidate = menu_buttons.nth(i)

                try:

                    if candidate.is_visible():

                        report_menu = candidate

                        break

                except Exception:
                    pass

            if report_menu is None:

                raise AutomationError(
                    "Report Menu button not found."
                )

            report_menu.click()

            page.wait_for_timeout(800)

            # =================================================
            # EXPORT
            # =================================================

            status(
                "Selecting Export..."
            )

            export_items = page.get_by_text(
                "Export",
                exact=True
            )

            export_clicked = False

            for i in range(
                export_items.count()
            ):

                item = export_items.nth(i)

                try:

                    if item.is_visible():

                        item.click()

                        export_clicked = True

                        break

                except Exception:
                    pass

            if not export_clicked:

                raise AutomationError(
                    "Export option not found."
                )

            status(
                "Export dialog opened."
            )

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

            status(
                "Selecting Excel..."
            )

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

            status(
                "Excel selected."
            )

            # =================================================
            # FIND DOWNLOAD BUTTON
            # =================================================

            status(
                "Finding Download button..."
            )

            download_buttons = export_modal.locator(
                "button.btn-modal-primary"
            )

            visible_download = None

            for i in range(
                download_buttons.count()
            ):

                candidate = (
                    download_buttons.nth(i)
                )

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

                visible_download = (
                    export_modal
                    .get_by_text(
                        "Download",
                        exact=True
                    )
                    .last
                )

            visible_download.wait_for(
                state="visible",
                timeout=10000
            )

            # =================================================
            # DOWNLOAD
            # =================================================

            check_stop()

            status(
                "Downloading Excel..."
            )

            with page.expect_download(
                timeout=60000
            ) as download_info:

                visible_download.click()

            download = download_info.value

            # =================================================
            # SAVE FILE
            # =================================================

            timestamp_now = datetime.now().strftime(
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
                f"{timestamp_now}.xlsx"
            )

            file_path = os.path.join(
                download_folder,
                filename
            )

            download.save_as(
                file_path
            )

            downloaded_files.append(
                file_path
            )

            status(
                f"Downloaded:\n{file_path}"
            )

            status(
                f"Section completed: "
                f"{student_group}"
            )

            # =================================================
            # IMPORTANT:
            # DO NOT immediately reuse the old page state.
            # The next loop will perform a FULL page reload.
            # =================================================

            page.wait_for_timeout(1500)

        # ====================================================
        # ALL SECTIONS COMPLETED
        # ====================================================

        status("")

        status("=" * 65)

        status(
            "ALL SECTIONS COMPLETED"
        )

        status("=" * 65)

        status(
            f"Total Excel files: "
            f"{len(downloaded_files)}"
        )

        for file_path in downloaded_files:

            status(file_path)

        status("")

        status(
            "Browser will remain OPEN."
        )

        status(
            "Press STOP AUTOMATION or close "
            "the application when finished."
        )

        # ====================================================
        # KEEP BROWSER OPEN
        # ====================================================

        while not _stop_event.is_set():

            time.sleep(0.5)

        status(
            "Stop requested."
        )

        return downloaded_files

    # ========================================================
    # ERROR
    # ========================================================

    except Exception as error:

        status("")

        status("=" * 65)

        status(
            "AUTOMATION ERROR"
        )

        status("=" * 65)

        status(
            str(error)
        )

        status("")

        status(
            "Browser will remain OPEN."
        )

        status(
            "Inspect the browser if needed."
        )

        status(
            "Press STOP AUTOMATION to close it."
        )

        status("=" * 65)

        # Keep browser open until user stops.
        while not _stop_event.is_set():

            time.sleep(0.5)

        status("")

        status(
            "STOP RECEIVED."
        )

        status(
            "Closing browser..."
        )

        raise

    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

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