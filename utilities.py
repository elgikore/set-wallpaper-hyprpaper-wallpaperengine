import os, subprocess

def force_floating_window_hyprland(window_name: str, is_enabled: bool = True) -> None:
    if os.getenv("XDG_CURRENT_DESKTOP") != "Hyprland": 
        return
    
    if is_enabled:
        subprocess.run(f"hyprctl keyword windowrulev2 \"float,class:^(Tk)$,title:^({window_name})\"")
    else:
        subprocess.run(f"hyprctl keyword windowrulev2 \"tile,class:^(Tk)$,title:^({window_name})\"")
    

def get_monitors() -> list[str]:
    monitors = subprocess.run("hyprctl monitors | awk '/Monitor.*/{print $2}'", 
                              shell=True, capture_output=True, text=True)
    
    return sorted(monitors.stdout.rstrip().split('\n'))