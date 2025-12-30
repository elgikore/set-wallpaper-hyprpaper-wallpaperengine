# Getting Started
## Dependencies
The files assume that you have installed ![Hyprland](https://wiki.hypr.land/Getting-Started/Installation/).

After that, install the dependencies from your AUR helper of choice:
```
yay -S hyprpaper linux-wallpaperengine-git python-pillow
```
> [!NOTE]
> `python-pillow` is needed to render preview pictures in `tk.Canvas` for `set_wallpaper_wallpaperengine.py`.

## Installation
Clone/download and make `set_wallpaper.py` and `set_wallpaper_wallpaperengine.py` executable:
```bash
git clone https://github.com/elgikore/set-wallpaper-hyprpaper-wallpaperengine.git
cd set-wallpaper-hyprpaper-wallpaperengine
chmod +x set_wallpaper.py  set_wallpaper_wallpaperengine.py
```

Then in your `hyprland.conf`, put this one below so that the wallpaper applies for every config. reload:
```
$background = path/to/set-wallpaper-hyprpaper-wallpaperengine/background.sh
exec = $background
```
> [!NOTE]
> The path assumes `set-wallpaper-hyprpaper-wallpaperengine` is the name of the folder. `background.sh` is automatically created after running either script.
>
> You can also do a one-liner if you prefer: `exec = path/to/set-wallpaper-hyprpaper-wallpaperengine/background.sh`.

### For multiple monitors (optional)
Ensure it is set up ![correctly](https://wiki.hypr.land/Configuring/Monitors/) in your `hyprland.conf`. Like in the wiki, the recommended rule for random monitors are: `monitor = , preferred, auto, 1`. Both Python scripts handle multiple monitors gracefully.

# Usage
Just run either `./set_wallpaper.py` or `./set_wallpaper_wallpaperengine.py`, and then select your wallpaper of choice and its placement in monitor.

# Troubleshooting/Modifications
**Wallpaper doesn't load at startup!**

Modify the delay in either files. You should see `delay = 0.5` (default value) in the file.
<br><br>

**I want to modify how the wallpaper is set up.**

The default commands being set are:
```python
command_preload = f"hyprctl hyprpaper preload \"{img_path}\""
command_wallpaper = f"hyprctl hyprpaper wallpaper \"{screen},{img_path}\""
```
and
```python
command = f"linux-wallpaperengine {screen} --scaling fill -s {selection_id} &"
```
for `set_wallpaper.py` and `set_wallpaper_wallpaperengine.py` respectively. 

It supports any valid commands for `hyprctl hyprpaper` and `linux-wallpaperengine` respectively. The only thing to remmber is that `{screen}` and `{img_path}` should be present for the former, and `{screen}` and `{selection_id}` for the latter.
