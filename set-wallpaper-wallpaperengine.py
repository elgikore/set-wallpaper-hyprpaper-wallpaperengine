from tkinter import *
from tkinter import ttk
from utilities import get_monitors, force_floating_window_hyprland, on_close

window_title = "Set wallpaper from Wallpaper Engine"




root = Tk()
root.title(window_title)
root.geometry("500x240")
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, window_title))
force_floating_window_hyprland(window_title)

monitors_list = Listbox(root, listvariable=Variable(value=get_monitors()), 
                        height=6, selectmode=SINGLE)


monitors_list.grid(row=0, column=0, padx=4, pady=4)
root.mainloop()