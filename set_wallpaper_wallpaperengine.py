#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
from utilities import *
from monitors_list_gui import MonitorList
from typing import NamedTuple
import sys, subprocess

# Main window title
window_title = "Set wallpaper from Wallpaper Engine"

# Wallpaper Engine wallpaper path
wallpaperengine_path = Path("~/.steam/steam/steamapps/workshop/content/431960/").expanduser()

# Listbox selection
selection = ""

# Delay in case the wallpaper fails to load
delay = 0.5


class Wallpaper(NamedTuple):
    id: str
    path: Path
    preview_pic_path: Path


def list_wallpaperengine_wallpapers() -> None | dict[Wallpaper]:
    if wallpaperengine_path.exists():
        return {
            # preview_path needs next because globbing returns an iterator and we only need the first result
            pic_dir.name: Wallpaper(pic_dir.name, pic_dir, pic_dir / next(pic_dir.glob("preview.*"), None))
            for pic_dir in wallpaperengine_path.iterdir() 
            if pic_dir.is_dir()
        }
    else:
        messagebox.showerror("Path for Wallpaper Engine doesn't exist", "Wallpaper Engine isn't installed.",
                             detail=f"Please install Wallpaper Engine from Steam, and put the wallpapers in here: {wallpaperengine_path}.", 
                             parent=frame)
        on_close(root, window_title)
        sys.exit(1)


def show_preview_picture(event) -> None:
    global selection
    
    selection = wallpaper_list.curselection()
    
    if not selection:
        return
    else:
        selection = wallpaper_list.get(selection)
        
    preview_pic_path = wallpapers[selection].preview_pic_path
    wallpaper_img = Image.open(preview_pic_path) 
    
    if preview_pic_path.suffix == ".gif":
        # Advance to 5 frames in case the first few frames are black
        wallpaper_img.seek(5)
    
    wallpaper_img = wallpaper_img.resize((preview_canvas.winfo_width(), preview_canvas.winfo_height()), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(wallpaper_img)
    
    preview_canvas.create_image(0, 0, anchor="nw", image=tk_img) 
    preview_canvas.image = tk_img


def apply_wallpaper():
    screen = f"--screen-root {monitor_list.get()}"
    command = f"linux-wallpaperengine {screen} --scaling fill -s {selection} &"
    
    # Close specific monitor of linux-wallpaperengine if selection is same with screen
    close_app(screen) 
    
    # Kill all hyprpaper instances if there is one
    close_app("hyprpaper")

    # Check if script exists; if not, create, else does nothing
    check_and_create_script()
        
    # If for some reason the file is not executable
    ensure_executable_script()
    
    current_text = ""
    new_lines = ["#!/bin/bash", f"sleep {delay}"]
    skip_keywords = {"sleep", "#!/bin/bash", "hyprpaper"}
    
    is_monitor_in_setting = False # In case the monitor is a new entry
    
    with open(bg_script_path, 'r') as bg_script:
        current_text = bg_script.read()
        
    for line in current_text.splitlines():
        # Skip these keywords; the first 2 are already added, the last one is not needed
        if any(keyword in line for keyword in skip_keywords):
            continue
        
        if screen in line:
            new_lines.append(command)
            is_monitor_in_setting = True
            continue
        
        new_lines.append(line)
    
    if not is_monitor_in_setting:
        new_lines.append(command)
    
    with open(bg_script_path, 'w') as bg_script:
        bg_script.write("\n".join(new_lines))

    subprocess.run("hyprctl reload", shell=True)


# Main Window
root = Tk()
root.title(window_title)
root.geometry("848x360")
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, window_title))
force_floating_window_hyprland(window_title)

# Frame for the first column
frame = Frame(root)
frame.grid(row=0, column=0)


# First column
# [Top] Listbox of wallpapers
wallpapers = dict(sorted(list_wallpaperengine_wallpapers().items()))
wallpaper_ids = [wallpaper_id for wallpaper_id in wallpapers.keys()]
wallpaper_list_frame = Frame(frame)

scrollbar = Scrollbar(wallpaper_list_frame, orient="vertical")
wallpaper_list = Listbox(wallpaper_list_frame, listvariable=Variable(value=wallpaper_ids), 
                        height=12, width=55, selectmode=SINGLE, yscrollcommand=scrollbar.set)
scrollbar.config(command=wallpaper_list.yview)

wallpaper_list.pack(side="left", fill="both", pady=5)
scrollbar.pack(side="right", fill="y", pady=5)
wallpaper_list_frame.pack(padx=10)

# [Bottom] Monitor list
monitor_list = MonitorList(frame, apply_wallpaper)
monitor_list.pack()


# Second column
preview_canvas = Canvas(root, width=340, height=340, bg="white")
preview_canvas.grid(row=0, column=1, padx=10, pady=5)
wallpaper_list.bind("<<ListboxSelect>>", show_preview_picture)

# Set styling on the readonly fields
readonly_field_styling()

root.mainloop()