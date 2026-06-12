import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import Any
from pathlib import Path


class SetupApp():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        main_frame = tk.Frame(
            self.root,
            bg="#0E0E0E")
        main_frame.pack(fill='both', expand=1)

        # find python folder
        find_dir_frame = tk.Frame(
            main_frame
        )
        find_dir_frame.grid(row=0)
        self.dir_var = tk.StringVar()
        dir_label = tk.Label(
            find_dir_frame,
            textvariable=self.dir_var,
            justify='left',
            fg='white',
            bg="#353535",)
        dir_label.grid(columnspan=6, column=0, row=0)
        browse_button = tk.Button(
            find_dir_frame,
            text='Select python folder',
            command=self.browse_folders
        )
        browse_button.grid(column=10, row=0)

        # make pip list
        entry_frame = tk.Frame(main_frame)
        entry_frame.grid(row=1)
        self.package_entry = tk.Entry(entry_frame, bg='white', width=30)
        self.package_entry.grid(row=0)
        self.package_entry.bind('<Return>', self.add_to_listbox)
        self.package_list = tk.Listbox(entry_frame, selectmode='multiple')
        add_button = tk.Button(
            entry_frame,
            text='Add package',
            command=self.add_to_listbox
        )
        add_button.grid(row=1, column=0)
        self.package_list.grid(row=2)
        remove_button = tk.Button(
            entry_frame,
            text='Remove packages',
            command=self.delete_from_listbox
        )
        remove_button.grid(row=2, column=1)

        # save preset
        save_preset_frame = tk.Frame(main_frame)
        save_preset_frame.grid()
        preset_name_label = tk.Label(
            save_preset_frame,
            text='Enter preset name: ')
        preset_name_label.grid(row=0, column=0)
        self.preset_name = tk.Entry(save_preset_frame)
        self.preset_name.grid(row=0, column=1)
        save_button = tk.Button(
            save_preset_frame,
            text='Save preset',
            command=self.save_preset
        )
        save_button.grid(row=1)

    def save_preset(self):
        preset_name = self.preset_name.get()
        if not preset_name:
            messagebox.showwarning(
                title='Warning', message='Preset name is required')
            return
        python_dir = self.dir_var.get()
        if not python_dir:
            messagebox.showwarning(
                title='Warning',
                message='Python directory is required')
            return
        python_exe = Path(python_dir + '/python.exe')
        if not python_exe.is_file():
            messagebox.showwarning(
                title='Warning',
                message='Invalid python directory\n python.exe is not found'
            )
            return
        pip_packages = self.package_list.get(0, 'end')
        preset_values: dict[str, Any] = {  # type: ignore
            f'{preset_name}': {
                'python_dir': python_dir,
                'pip_packages': pip_packages
            }
        }
        with open('presets/presets.json', 'a', encoding='UTF-8') as file:
            json.dump(preset_values, file, indent=2)

    def delete_from_listbox(self):
        selection = self.package_list.curselection()
        if not selection:
            return
        for selected_i in reversed(selection):
            self.package_list.delete(selected_i)

    def add_to_listbox(self, event=None):
        package_name = self.package_entry.get()
        if package_name:
            self.package_list.insert('end', package_name)
            self.package_entry.delete(0, 'end')

    def browse_folders(self) -> None:
        dir_path = filedialog.askdirectory(
            title='Select folder',
            initialdir='/'
        )
        if dir_path:
            self.dir_var.set(dir_path)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Setup Preset')
    root.geometry('600x600')
    root.resizable(False, False)
    app = SetupApp(root)
    root.mainloop()
