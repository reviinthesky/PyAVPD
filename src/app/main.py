from time import sleep

from src.app.main_ui import MainWindow
import tkinter as tk
from src.app.commands import run_bat, temp_dir
import os
root = tk.Tk()
root.title('PyAVPD')
root.geometry('480x680')
root.resizable(False, False)
app = MainWindow(root)
app.run()
try:
    data = app.preset_data
except AttributeError:
    os._exit(0)

project_dir = app.dir_var.get()
run_bat(project_dir, data)
sleep(10)
try:
    os.remove(temp_dir)
except Exception:
    pass
