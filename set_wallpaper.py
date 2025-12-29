#!/usr/bin/env python3

import sys, subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from utilities import *
from monitors_list_gui import MonitorList

# File path for wallpaper
img_path = sys.argv[1] if len(sys.argv) != 1 else ""

# Main window title
window_title = "Select monitor"

# Delay between Hyprpaper and IPC commands to load the wallpaper properly
delay = 0.5


# Set wallpaper
def set_wallpaper() -> None:
    if not img_path:
        messagebox.showerror("Invalid path!", "No picture selected.",
                             detail="Please select a picture.",
                             parent=root)
        return

    screen = monitor_list.get()
    pkill_regex = f"wallpaper..{screen}"
    command_preload = f"hyprctl hyprpaper preload \"{img_path}\""
    command_wallpaper = f"hyprctl hyprpaper wallpaper \"{screen},{img_path}\""
    
    # Close specific monitor of hyprpaper if selection is same with screen
    close_app(pkill_regex)
    
    # Kill all linux-wallpaperengine instances if there is one
    close_app("linux-wallpaperengine")
    
    # Check if script exists; if not, create, else does nothing
    check_and_create_script()
        
    # If for some reason the file is not executable
    ensure_executable_script()

    current_text = ""
    
    # Need "hyprpaper &" below it because the IPC commands need a running Hyprpaper instance
    # Need sleep to run the IPC commands properly (because of Hyprpaper being loaded)
    new_lines = ["#!/bin/bash", "hyprpaper &", f"sleep {delay}"]
    skip_keywords = {"sleep", "#!/bin/bash", "hyprpaper &", "linux-wallpaperengine"}
    
    is_monitor_in_setting = False # In case the monitor is a new entry
    
    with open(bg_script_path, 'r') as bg_script:
        current_text = bg_script.read()

    for line in current_text.splitlines(): 
        # Skip these keywords; the first 2 are already added, the last one is not needed
        if any(keyword in line for keyword in skip_keywords):
            continue
        
        if screen in line:
            old_preload = line.replace(f"hyprctl hyprpaper wallpaper \"{screen},",
                    "hyprctl hyprpaper preload \"")
            
            new_lines.remove(old_preload)
            new_lines.append(command_preload)
            new_lines.append(command_wallpaper)
            is_monitor_in_setting = True
            continue
        
        new_lines.append(line)

    if not is_monitor_in_setting:
        new_lines.append(command_preload)
        new_lines.append(command_wallpaper)
    
    with open(bg_script_path, 'w') as bg_script:
        bg_script.write("\n".join(new_lines))

    subprocess.run("hyprctl reload", shell=True)


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
    path_show.delete(0, "end")
    path_show.insert(0, img_path)
    path_show.config(state="readonly")



# Main Window
root = Tk()
root.title(window_title)
root.geometry("240x200")
force_floating_window_hyprland(window_title)
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, window_title)) # If the user presses the X button

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
monitor_list = MonitorList(root, command=set_wallpaper)
monitor_list.pack()

# Set styling on the readonly fields
readonly_field_styling()

root.mainloop()
