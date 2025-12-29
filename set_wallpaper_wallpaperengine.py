from tkinter import *
from tkinter import ttk, messagebox
from pathlib import Path
from utilities import get_monitors, force_floating_window_hyprland, on_close
from monitors_list_gui import MonitorList
from typing import NamedTuple
import sys

window_title = "Set wallpaper from Wallpaper Engine"
wallpaperengine_path = Path("~/.steam/steam/steamapps/workshop/content/431960/").expanduser()


class Wallpaper(NamedTuple):
    id: str
    path: Path
    preview_pic: Path


def list_wallpaperengine_wallpapers():
    if wallpaperengine_path.exists():
        return [Wallpaper(pic_dir.name, pic_dir, pic_dir / "preview.jpg") 
                    for pic_dir in wallpaperengine_path.iterdir() 
                    if pic_dir.is_dir()]
    else:
        messagebox.showerror("Path for Wallpaper Engine doesn't exist", "Wallpaper Engine isn't installed.",
                             detail=f"Please install Wallpaper Engine from Steam, and put the wallpapers in here: {wallpaperengine_path}.", 
                             parent=frame)
        sys.exit(1)


root = Tk()
root.title(window_title)
root.geometry("500x240")
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, window_title))
force_floating_window_hyprland(window_title)

# Frame to mix layouts, similar to JFrame
frame = Frame(root)
frame.grid(row=0, column=0)
wallpapers = list_wallpaperengine_wallpapers()
wallpaper_ids = sorted([wallpaper.id for wallpaper in wallpapers])

wallpaper_list_frame = Frame(frame)
scrollbar = Scrollbar(wallpaper_list_frame, orient="vertical")
wallpaper_list = Listbox(wallpaper_list_frame, listvariable=Variable(value=wallpaper_ids), 
                        height=6, selectmode=SINGLE, yscrollcommand=scrollbar.set)
scrollbar.config(command=wallpaper_list.yview)
wallpaper_list.pack(side="left", fill="both", pady=5)
scrollbar.pack(side="right", fill="y", pady=5)
wallpaper_list_frame.pack(padx=10)

monitor_list = MonitorList(frame)
monitor_list.pack()
root.mainloop()