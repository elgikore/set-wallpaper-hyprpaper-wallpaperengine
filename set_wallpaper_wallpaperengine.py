from tkinter import *
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
from utilities import check_app_and_close, force_floating_window_hyprland, on_close
from monitors_list_gui import MonitorList
from typing import NamedTuple
import sys, subprocess

window_title = "Set wallpaper from Wallpaper Engine"
wallpaperengine_path = Path("~/.steam/steam/steamapps/workshop/content/431960/").expanduser()
selection = ""


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
        # Advance to 10 frames in case the first few frames are black
        wallpaper_img.seek(10)
    
    wallpaper_img = wallpaper_img.resize((preview_canvas.winfo_width(), preview_canvas.winfo_height()), Image.LANCZOS)
        
    tk_img = ImageTk.PhotoImage(wallpaper_img)
    
    preview_canvas.create_image(0, 0, anchor="nw", image=tk_img) 
    preview_canvas.image = tk_img

def apply_wallpaper():
    check_app_and_close("linux-wallpaperengine")
    check_app_and_close("hyprpaper")
    subprocess.run(f"linux-wallpaperengine --screen-root {monitor_list.get()} --scaling fill -s {selection} &", shell=True)

root = Tk()
root.title(window_title)
root.geometry("464x256")
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
                        height=6, selectmode=SINGLE, yscrollcommand=scrollbar.set)
scrollbar.config(command=wallpaper_list.yview)

wallpaper_list.pack(side="left", fill="both", pady=5)
scrollbar.pack(side="right", fill="y", pady=5)
wallpaper_list_frame.pack(padx=10)

# [Bottom] Monitor list
monitor_list = MonitorList(frame, apply_wallpaper)
monitor_list.pack()


# Second column
preview_canvas = Canvas(root, width=240, height=240, bg="white")
preview_canvas.grid(row=0, column=1, padx=10, pady=5)
wallpaper_list.bind("<<ListboxSelect>>", show_preview_picture)

root.mainloop()