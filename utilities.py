# Shared utilites and variables across scripts

import os, subprocess
from tkinter import *
from tkinter import Tk, ttk
from pathlib import Path

bg_script_path = Path(__file__).resolve().parent / "background.sh"


def force_floating_window_hyprland(window_name: str, is_enabled: bool = True) -> None:
    if os.getenv("XDG_CURRENT_DESKTOP") != "Hyprland": 
        return
    
    if is_enabled:
        subprocess.run(f"hyprctl keyword windowrulev2 \"float,class:^(Tk)$,title:^({window_name})\"", 
                       shell=True)
    else:
        subprocess.run(f"hyprctl keyword windowrulev2 \"tile,class:^(Tk)$,title:^({window_name})\"", 
                       shell=True)
    

def get_monitors() -> list[str]:
    monitors = subprocess.run("hyprctl monitors | awk '/Monitor.*/{print $2}'", shell=True, 
                              capture_output=True, text=True)
    
    return sorted(monitors.stdout.rstrip().split('\n'))


def on_close(root: Tk, window_title: str) -> None:
    root.destroy()
    force_floating_window_hyprland(window_title, is_enabled=False)
    

def close_app(regex: str) -> bool:
    result = subprocess.run(f"pkill -9 -f -- \"{regex}\"", shell=True)
    
    return True if result.returncode == 0 else False


def readonly_field_styling() -> None:
    readonly_color = [("readonly", "white")]
    readonly_style = {
        "fieldbackground": readonly_color, 
        "background": readonly_color 
    }

    style = ttk.Style()
    style.map("TCombobox", **readonly_style)
    style.map("TEntry", **readonly_style)


def check_and_create_script() -> bool:
    """
    True if it creates a script.
    
    False if the path is invalid (not .py or .sh) or file exists.
    """
    if bg_script_path.suffix not in {".py", ".sh"}:
        return False
    
    if not bg_script_path.exists():
        bg_script_path.touch()
        bg_script_path.chmod(0o755) # Make it executable
        
        with open(bg_script_path, 'w') as bg_script:
            bg_script.write("#!/bin/bash\n")
        
        return True
    else:
        return False


def ensure_executable_script() -> bool:
    """True if the file isn't executable. False if it already is."""
    
    if not os.access(bg_script_path, os.X_OK):
        bg_script_path.chmod(0o755)
        return True
    else:
        return False
    

class MonitorList(Frame):
    def __init__(self, root: Tk = None, command: callable = None, **kwargs):
        super().__init__(root, **kwargs)
        
        label2 = ttk.Label(root, text="Monitor to place wallpaper:")
        label2.pack(padx=10, pady=3, anchor='w')

        monitors = get_monitors()
        self.__list_monitors_box = ttk.Combobox(root, values=monitors, state="readonly")
        self.__list_monitors_box.current(0)
        self.__list_monitors_box.pack(pady=1, fill="both", padx=10)

        ok_button = ttk.Button(root, text="OK", command=command)
        ok_button.pack(pady=10)
        
    def get(self): 
        return self.__list_monitors_box.get()