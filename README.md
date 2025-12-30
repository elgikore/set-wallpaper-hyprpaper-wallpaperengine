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
