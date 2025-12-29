# Shared utilites across scripts

import os, subprocess
from tkinter import Tk

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
    result = subprocess.run(f"pkill -f -- \"{regex}\"", shell=True)
    
    return True if result.returncode == 0 else False