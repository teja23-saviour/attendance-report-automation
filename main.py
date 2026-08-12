import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import re

from attendance import run_automation, stop_automation, AutomationError


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()
root.title("Attendance Report Automation")
root.geometry("1100x760")
root.minsize(900, 620)
root.configure(bg="#f4f6f8")

# IMPORTANT:
# Use GRID for the whole window. This keeps the bottom buttons
# visible even when the window is resized.
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


# ============================================================
# VARIABLES
# ============================================================

username_var = tk.StringVar()
password_var = tk.StringVar()
show_password_var = tk.BooleanVar(value=False)
output_folder_var = tk.StringVar()
current_section_var = tk.StringVar(value="Ready")
progress_var = tk.DoubleVar(value=0)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Action.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(20, 9),
)

style.configure(
    "Stop.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(20, 9),
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root, bg="#f4f6f8")
header.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=28,
    pady=(16, 8),
)

tk.Label(
    header,
    text="ATTENDANCE REPORT AUTOMATION",
    font=("Segoe UI", 22, "bold"),
    bg="#f4f6f8",
).pack(anchor="w")

tk.Label(
    header,
    text="SRKR Lightbooks  •  Multi-section Excel Report Automation",
    font=("Segoe UI", 10),
    fg="#5f6368",
    bg="#f4f6f8",
).pack(anchor="w", pady=(2, 0))


# ============================================================
# MAIN AREA
# ============================================================

main = tk.Frame(root, bg="#f4f6f8")
main.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=28,
    pady=(0, 8),
)

main.grid_rowconfigure(1, weight=1)
main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)


# ============================================================
# LOGIN
# ============================================================

login_frame = ttk.LabelFrame(
    main,
    text="  Teacher Login  ",
    padding=12,
)

login_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 6),
    pady=(0, 8),
)

login_frame.grid_columnconfigure(1, weight=1)

ttk.Label(
    login_frame,
    text="Username / Email:",
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=5,
)

username_entry = ttk.Entry(
    login_frame,
    textvariable=username_var,
    font=("Segoe UI", 10),
)

username_entry.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=(12, 0),
    pady=5,
)

ttk.Label(
    login_frame,
    text="Password:",
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=5,
)

password_entry = ttk.Entry(
    login_frame,
    textvariable=password_var,
    show="*",
    font=("Segoe UI", 10),
)

password_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=(12, 0),
    pady=5,
)


def toggle_password():
    password_entry.configure(
        show="" if show_password_var.get() else "*"
    )


ttk.Checkbutton(
    login_frame,
    text="Show password",
    variable=show_password_var,
    command=toggle_password,
).grid(
    row=2,
    column=1,
    sticky="w",
    padx=(12, 0),
    pady=(1, 0),
)


# ============================================================
# OUTPUT FOLDER
# ============================================================

output_frame = ttk.LabelFrame(
    main,
    text="  Excel Output Folder  ",
    padding=12,
)

output_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(6, 0),
    pady=(0, 8),
)

output_frame.grid_columnconfigure(0, weight=1)

output_entry = ttk.Entry(
    output_frame,
    textvariable=output_folder_var,
    font=("Segoe UI", 10),
)

output_entry.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 8),
    pady=5,
)


def choose_output_folder():
    folder = filedialog.askdirectory(
        title="Choose Excel Output Folder"
    )

    if folder:
        output_folder_var.set(folder)


ttk.Button(
    output_frame,
    text="Browse...",
    command=choose_output_folder,
).grid(
    row=0,
    column=1,
    pady=5,
)


# ============================================================
# SECTIONS
# ============================================================

section_frame = ttk.LabelFrame(
    main,
    text="  Student Groups / Sections  ",
    padding=10,
)

section_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=(0, 6),
)

section_frame.grid_rowconfigure(1, weight=1)
section_frame.grid_columnconfigure(0, weight=1)

ttk.Label(
    section_frame,
    text="Enter one section per line. Press Enter for the next section.",
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=(0, 6),
)

section_container = tk.Frame(section_frame)
section_container.grid(
    row=1,
    column=0,
    sticky="nsew",
)

section_container.grid_rowconfigure(0, weight=1)
section_container.grid_columnconfigure(1, weight=1)

line_numbers = tk.Text(
    section_container,
    width=4,
    padx=5,
    pady=7,
    font=("Consolas", 10),
    bg="#e9ecef",
    fg="#6c757d",
    relief="flat",
    state="disabled",
    takefocus=0,
)

line_numbers.grid(
    row=0,
    column=0,
    sticky="ns",
)

section_box = tk.Text(
    section_container,
    wrap="none",
    undo=True,
    font=("Consolas", 10),
    padx=8,
    pady=7,
    relief="solid",
    borderwidth=1,
)

section_box.grid(
    row=0,
    column=1,
    sticky="nsew",
)

section_scroll = ttk.Scrollbar(
    section_container,
    orient="vertical",
    command=section_box.yview,
)

section_scroll.grid(
    row=0,
    column=2,
    sticky="ns",
)

section_box.configure(
    yscrollcommand=section_scroll.set
)

section_box.insert(
    "1.0",
    "BTECH-ME-AY2627-SEM-03-A"
)


def update_line_numbers(event=None):
    try:
        count = int(
            section_box.index("end-1c").split(".")[0]
        )

        numbers = "\n".join(
            str(i) for i in range(1, count + 1)
        )

        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        line_numbers.insert("1.0", numbers)
        line_numbers.config(state="disabled")

        first, _ = section_box.yview()
        line_numbers.yview_moveto(first)

    except tk.TclError:
        pass


section_box.bind(
    "<KeyRelease>",
    update_line_numbers
)

section_box.bind(
    "<MouseWheel>",
    update_line_numbers
)

update_line_numbers()


ttk.Label(
    section_frame,
    text="Example: BTECH-ME-AY2627-SEM-03-A",
    font=("Segoe UI", 8),
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=(6, 0),
)


# ============================================================
# STATUS
# ============================================================

status_frame = ttk.LabelFrame(
    main,
    text="  Automation Status  ",
    padding=10,
)

status_frame.grid(
    row=1,
    column=1,
    sticky="nsew",
    padx=(6, 0),
)

status_frame.grid_rowconfigure(2, weight=1)
status_frame.grid_columnconfigure(0, weight=1)

status_header = tk.Frame(status_frame)
status_header.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 6),
)

ttk.Label(
    status_header,
    text="Current:",
).pack(
    side="left"
)

ttk.Label(
    status_header,
    textvariable=current_section_var,
    font=("Segoe UI", 9, "bold"),
).pack(
    side="left",
    padx=(8, 0)
)

progress = ttk.Progressbar(
    status_frame,
    variable=progress_var,
    maximum=100,
    mode="determinate",
)

progress.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=(0, 7),
)

status_container = tk.Frame(status_frame)
status_container.grid(
    row=2,
    column=0,
    sticky="nsew",
)

status_container.grid_rowconfigure(0, weight=1)
status_container.grid_columnconfigure(0, weight=1)

status_box = tk.Text(
    status_container,
    wrap="word",
    font=("Consolas", 9),
    state="disabled",
    padx=8,
    pady=7,
    relief="solid",
    borderwidth=1,
)

status_box.grid(
    row=0,
    column=0,
    sticky="nsew",
)

status_scroll = ttk.Scrollbar(
    status_container,
    orient="vertical",
    command=status_box.yview,
)

status_scroll.grid(
    row=0,
    column=1,
    sticky="ns",
)

status_box.configure(
    yscrollcommand=status_scroll.set
)


# ============================================================
# STATUS FUNCTIONS
# ============================================================

def update_status(message):
    def update():
        try:
            status_box.config(state="normal")
            status_box.insert("end", str(message) + "\n")
            status_box.see("end")
            status_box.config(state="disabled")

            match = re.search(
                r"(?:PROCESSING SECTION|SECTION)\s+(\d+)\s+OF\s+(\d+)",
                str(message),
                re.IGNORECASE,
            )

            if match:
                current = int(match.group(1))
                total = max(int(match.group(2)), 1)
                progress_var.set(
                    ((current - 1) / total) * 100
                )

        except tk.TclError:
            pass

    try:
        root.after(0, update)
    except tk.TclError:
        pass


def clear_status():
    status_box.config(state="normal")
    status_box.delete("1.0", "end")
    status_box.config(state="disabled")

    progress_var.set(0)
    current_section_var.set("Ready")


def get_sections():
    raw = section_box.get(
        "1.0",
        "end-1c"
    )

    sections = []

    for line in raw.splitlines():
        section = line.strip()

        # Allows users to type:
        # 1. BTECH...
        # 1) BTECH...
        section = re.sub(
            r"^\s*\d+\s*[\.\)]\s*",
            "",
            section,
        ).strip()

        if section and section not in sections:
            sections.append(section)

    return sections


def set_running(running):
    start_button.config(
        state="disabled" if running else "normal"
    )

    stop_button.config(
        state="normal" if running else "disabled"
    )


# ============================================================
# START AUTOMATION
# ============================================================

def start_automation():
    username = username_var.get().strip()
    password = password_var.get()
    sections = get_sections()

    if not username:
        messagebox.showwarning(
            "Missing Username",
            "Please enter the teacher username/email."
        )
        username_entry.focus_set()
        return

    if not password:
        messagebox.showwarning(
            "Missing Password",
            "Please enter the password."
        )
        password_entry.focus_set()
        return

    if not sections:
        messagebox.showwarning(
            "Missing Sections",
            "Please enter at least one Student Group."
        )
        section_box.focus_set()
        return

    clear_status()
    set_running(True)

    update_status("=" * 70)
    update_status("STARTING ATTENDANCE AUTOMATION")
    update_status("=" * 70)
    update_status(
        f"Total sections: {len(sections)}"
    )
    update_status("")

    def worker():
        try:
            # Keep this compatible with the current attendance.py.
            files = run_automation(
                username=username,
                password=password,
                student_groups=sections,
                status_callback=update_status,
            )

            def success():
                progress_var.set(100)
                current_section_var.set("Completed")
                set_running(False)

                count = len(files) if files else 0

                messagebox.showinfo(
                    "Automation Finished",
                    "Attendance automation completed.\n\n"
                    f"Files downloaded: {count}\n\n"
                    "Check the selected/default output folder."
                )

            root.after(0, success)

        except AutomationError as exc:
            error_message = str(exc)

            def show_automation_error():
                set_running(False)
                current_section_var.set("Error")
                messagebox.showerror(
                    "Automation Error",
                    error_message
                )

            root.after(
                0,
                show_automation_error
            )

        except Exception as exc:
            error_message = str(exc)

            def show_error():
                set_running(False)
                current_section_var.set("Error")
                messagebox.showerror(
                    "Automation Error",
                    error_message
                )

            root.after(
                0,
                show_error
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# ============================================================
# STOP
# ============================================================

def stop_current_automation():
    try:
        stop_automation()
    except Exception as exc:
        update_status(
            f"Stop request error: {exc}"
        )

    update_status("")
    update_status("=" * 70)
    update_status("STOP REQUEST SENT")
    update_status(
        "Automation will stop after the current Playwright operation."
    )
    update_status("=" * 70)

    stop_button.config(
        state="disabled"
    )


# ============================================================
# CLOSE
# ============================================================

def close_application():
    try:
        stop_automation()
    except Exception:
        pass

    root.destroy()


# ============================================================
# FIXED BOTTOM BUTTON BAR
# ============================================================
#
# This is a GRID row of the ROOT window, NOT part of the
# expandable main area. Therefore it will ALWAYS remain visible.
#

button_bar = tk.Frame(
    root,
    bg="#e8ebef",
    height=72,
)

button_bar.grid(
    row=2,
    column=0,
    sticky="ew",
)

button_bar.grid_propagate(False)

button_bar.grid_columnconfigure(0, weight=1)

button_inner = tk.Frame(
    button_bar,
    bg="#e8ebef",
)

button_inner.pack(
    fill="both",
    expand=True,
    padx=28,
    pady=10,
)

start_button = ttk.Button(
    button_inner,
    text="▶  GENERATE EXCEL",
    command=start_automation,
    style="Action.TButton",
)

start_button.pack(
    side="left",
    padx=(0, 10),
)

stop_button = ttk.Button(
    button_inner,
    text="■  STOP AUTOMATION",
    command=stop_current_automation,
    style="Stop.TButton",
    state="disabled",
)

stop_button.pack(
    side="left",
    padx=10,
)

close_button = ttk.Button(
    button_inner,
    text="CLOSE APPLICATION",
    command=close_application,
)

close_button.pack(
    side="right",
)


# ============================================================
# IMPORTANT:
# Do NOT bind Enter globally.
# Enter inside section_box only creates another section line.
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

username_entry.focus_set()

root.mainloop()