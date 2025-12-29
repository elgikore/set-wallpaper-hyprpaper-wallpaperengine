#!/usr/bin/env python3

import sys, subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# File path for wallpaper
img_path = sys.argv[1] if len(sys.argv) != 1 else ""

# Main window title
window_title = "Select monitor"


def on_close() -> None:
    root.destroy()
    force_floating_window(window_title, is_enabled=False)

def reload_hyprpaper() -> None:
    subprocess.run("if pgrep -x \"hyprpaper\" > /dev/null; then killall -9 hyprpaper; fi", shell=True)
    subprocess.run("hyprpaper &", shell=True)

# Get list of monitors
def get_monitors() -> list:
    result = subprocess.run( 
        "hyprctl monitors | awk '/Monitor.*:/{print $2}'", 
        shell=True,
        capture_output=True,
        text=True
    )

    return sorted(result.stdout.rstrip().split('\n'))

# Set wallpaper
def set_wallpaper() -> None:
    if not img_path:
        messagebox.showerror("Invalid path!", "No picture selected.",
                             detail="Please select a picture.", 
                             parent=root)
        return

    selected_monitor = list_monitors_box.get()
    hyprpaper_path = f"{Path.home()}/.config/hypr/hyprpaper.conf"

    # Get current hyprpaper conf
    settings = ""

    try:
        with open(hyprpaper_path, 'r') as conf:
            settings = conf.read()
    except FileNotFoundError:
        print("hyprpaper.conf not found!")
        sys.exit(1)

    is_monitor_in_conf = False # In case the monitor is a new entry

    # Change the wallpaper
    for line in settings.splitlines():
        if selected_monitor in line:
            old_wallpaper = line.split(',')[1]
            settings = settings.replace(old_wallpaper, img_path)
            is_monitor_in_conf = True
            break

    if not is_monitor_in_conf:
        to_append = f"\npreload = {img_path}\nwallpaper = {selected_monitor},{img_path}\n"
        settings += to_append

    # Write changes to file, reload, and close
    with open(hyprpaper_path, "w") as conf:
        conf.write(settings)

    reload_hyprpaper()
    on_close()

# Force floating window (Hyprland); if false, set it back to normal (tiled)
def force_floating_window(window_title: str, is_enabled: bool = True) -> None:
    if is_enabled: 
        subprocess.run(f"hyprctl keyword windowrulev2 \"float, title:^({window_title})$\"", shell=True)
    else:
        subprocess.run(f"hyprctl keyword windowrulev2 \"tile, title:^({window_title})$\"", shell=True)

def file_picker() -> None:
    global img_path

    img_path = filedialog.askopenfilename(
        initialdir=Path.home(),
        title="Select a picture as wallpaper",
        filetypes = (
            ("All image files", "*.png"),
            ("All image files", "*.jpg"),
            ("All image files", "*.jpeg"),
            ("All image files", "*.gif"),
            ("All image files", "*.bmp"),
            ("All image files", "*.tiff"),
        )
    )

    path_show.config(state=ACTIVE)
    path_show.insert(0, img_path)
    path_show.config(state="readonly")



# Main Window
root = Tk()
root.title(window_title)
root.geometry("240x200")
force_floating_window(window_title)
root.protocol("WM_DELETE_WINDOW", on_close) # If the user presses the X button

# File picker
label1 = ttk.Label(root, text="Pick a picture")
label1.pack(padx=10, pady=3, anchor='w')

path_show = ttk.Entry()
path_show.insert(0, img_path)
path_show.config(state="readonly", width=200)
path_show.pack(padx=10, pady=3)

file_picker_button = ttk.Button(root, text="Open", command=file_picker)
file_picker_button.pack(pady=5)

# Combobox and Button
label2 = ttk.Label(root, text="Monitor to place wallpaper:")
label2.pack(padx=10, pady=3, anchor='w')

monitors = get_monitors()
list_monitors_box = ttk.Combobox(root, values=monitors, state="readonly")
list_monitors_box.current(0)
list_monitors_box.pack(pady=1)

ok_button = ttk.Button(root, text="OK", command=set_wallpaper)
ok_button.pack(pady=10)

# Set styling on the readonly fields
readonly_color = [("readonly", "white")]
readonly_style = {
    "fieldbackground": readonly_color, 
    "background": readonly_color 
}

style = ttk.Style()
style.map("TCombobox", **readonly_style)
style.map("TEntry", **readonly_style)

root.mainloop()
