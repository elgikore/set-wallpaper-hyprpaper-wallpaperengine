from tkinter import *
from tkinter import ttk
from utilities import get_monitors

class MonitorList(Frame):
    def __init__(self, root: Tk = None, command: callable = None, **kwargs):
        super().__init__(root, **kwargs)
        
        label2 = ttk.Label(root, text="Monitor to place wallpaper:")
        label2.pack(padx=10, pady=3, anchor='w')

        monitors = get_monitors()
        self.__list_monitors_box = ttk.Combobox(root, values=monitors, state="readonly")
        self.__list_monitors_box.current(0)
        self.__list_monitors_box.pack(pady=1)

        ok_button = ttk.Button(root, text="OK", command=command)
        ok_button.pack(pady=10)
        
    def get(self): 
        return self.__list_monitors_box.get()


