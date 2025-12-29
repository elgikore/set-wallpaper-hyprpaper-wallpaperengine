import subprocess, os
from tkinter import *
from tkinter import ttk

window_name = "Set wallpaper from Wallpaper Engine"

def get_monitors() -> list[str]:
    monitors = subprocess.run("hyprctl monitors | awk '/Monitor.*/{print $2}'", 
                              shell=True, capture_output=True, text=True)
    
    return sorted(monitors.stdout.rstrip().split('\n'))

def force_floating_window_hyprland(window_name: str, is_enabled: bool = True) -> None:
    if os.getenv("XDG_CURRENT_DESKTOP") != "Hyprland": 
        return
    
    if is_enabled:
        subprocess.run(f"hyprctl keyword windowrulev2 \"float,class:^(Tk)$,title:^({window_name})\"")
    else:
        subprocess.run(f"hyprctl keyword windowrulev2 \"tile,class:^(Tk)$,title:^({window_name})\"")
    

root = Tk()
root.geometry("500x240")
monitors_list = Listbox(root, 
                        listvariable=Variable(value=get_monitors()), 
                        height=6, 
                        selectmode=SINGLE)

monitors_list.grid(row=0, column=0, padx=4, pady=4)
root.mainloop()