import tkinter as tk
from tkinter import messagebox
from typing import Any
from pathlib import Path
from src.app.ui_custom import *
from src.app.save_system import save_json


class SetupApp(ParentUI):
    def __init__(
            self, root: tk.Tk | tk.Toplevel,
            preset_data: dict[str, Any] | None = None) -> None:
        super().__init__(root, 'Select Python directory')
        self.config_files_presets: dict[str, str] = {}
        self.preset_data = preset_data

        # ________ pip list ________
        entry_frame = make_frame(self.main_frame, row=1)
        entry_frame.columnconfigure(0, weight=1)

        self.package_entry = tk.Entry(
            entry_frame,
            bg=COLORS['bg_entry'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            width=30,
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=COLORS['entry_hl'])
        self.package_entry.grid(
            row=0, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.package_entry.bind('<Return>', self.add_to_listbox)

        add_button = make_button(
            entry_frame,
            text='Add package',
            command=self.add_to_listbox,
            row=0, column=1, padx=(5, 10))

        self.package_list = tk.Listbox(
            entry_frame,
            selectmode='multiple',
            bg=COLORS['listbox_bg'],
            fg=COLORS['text_primary'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            font=('Arial', 10),
            relief='flat',
            highlightthickness=0,
            height=8)
        self.package_list.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

        remove_button = make_button(
            entry_frame,
            text='Remove packages',
            command=self.delete_from_listbox,
            row=3, column=0, columnspan=2, pady=(0, 10))

        # ________config files________
        config_files_frame = make_frame(self.main_frame, row=2)
        config_files_frame.columnconfigure(1, weight=1)

        config_file_name_label = make_label(
            config_files_frame,
            text='Enter config file name:',
            row=0, column=0, padx=(10, 5), pady=10, sticky='w')
        config_file_name_label.grid(
        )

        self.config_file_name_entry = tk.Entry(
            config_files_frame,
            bg=COLORS['bg_entry'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=COLORS['entry_hl']
        )
        self.config_file_name_entry.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky='ew'
        )

        config_file_content_label = make_label(
            config_files_frame,
            text='Enter config file content:',
            row=1, column=0, padx=(10, 5), pady=(0, 5), sticky='nw')

        self.config_file_content_entry = tk.Text(
            config_files_frame,
            bg=COLORS['bg_entry'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            font=('Arial', 10),
            relief='flat',
            highlightthickness=1,
            highlightbackground='#404040',
            wrap='word',
            height=6)
        self.config_file_content_entry.grid(
            row=1, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')

        config_files_listbox_label = make_label(
            config_files_frame,
            text='Config files list:',
            row=0, column=2, padx=(20, 10), pady=(10, 5), sticky='w'
        )

        self.config_files_listbox = tk.Listbox(
            config_files_frame,
            bg=COLORS['listbox_bg'],
            fg=COLORS['text_primary'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            font=('Arial', 10),
            relief='flat',
            highlightthickness=0,
            height=12,
            width=25,
            selectmode='single')
        self.config_files_listbox.grid(
            row=1, column=2, rowspan=2, padx=(20, 10), pady=10, sticky='ns'
        )
        self.config_files_listbox.bind(
            '<<ListboxSelect>>', self.choose_config_file_content)
        save_config_button = make_button(
            config_files_frame,
            text='Save config file',
            command=self.save_config_file,
            row=2, column=0, columnspan=2, pady=(0, 10))

        # ________save preset________
        save_preset_frame = make_frame(self.main_frame, row=3)
        save_preset_frame.columnconfigure(1, weight=1)
        preset_name_label = make_label(
            save_preset_frame,
            text='Enter preset name:',
            row=0, column=0, padx=(10, 5), pady=10, sticky='w')

        self.preset_name = tk.Entry(
            save_preset_frame,
            bg=COLORS['bg_entry'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=COLORS['entry_hl']
        )
        self.preset_name.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky='ew')

        save_button = make_button(
            save_preset_frame,
            text='Save preset',
            command=self.save_preset,
            row=1, column=0, columnspan=2, pady=(0, 10))

        self.load_preset_data()

    def load_preset_data(self) -> None:
        if self.preset_data is None:
            return

        preset_name, preset_values = next(iter(self.preset_data.items()))

        self.dir_var.set(preset_values['python_dir'])
        if preset_values['pip_packages']:
            self.package_list.delete(0, 'end')
            for package in preset_values['pip_packages']:
                self.package_list.insert('end', package)

        if preset_values['config_files']:
            self.config_files_presets = preset_values['config_files'].copy()
            self.config_files_listbox.delete(0, 'end')
            for file_name in self.config_files_presets.keys():
                self.config_files_listbox.insert('end', file_name)

        self.preset_name.delete(0, 'end')
        self.preset_name.insert(0, preset_name)

    def choose_config_file_content(self, event=None) -> None:
        file_name: str = self.config_files_listbox.get('anchor')
        file_content: str = self.config_files_presets[file_name]
        self.config_file_content_entry.delete(1.0, 'end')
        self.config_file_content_entry.insert(1.0, file_content)
        self.config_file_name_entry.delete(0, 'end')
        self.config_file_name_entry.insert(0, file_name)

    def save_config_file(self) -> None:
        config_file_name = self.config_file_name_entry.get()
        if not config_file_name:
            messagebox.showwarning(
                'Warning',
                'Config file name is required')
            return
        config_content = self.config_file_content_entry.get(1.0, 'end-1c')
        self.config_files_presets[config_file_name] = config_content
        self.config_files_listbox.insert('end', config_file_name)
        self.config_file_name_entry.delete(0, 'end')
        self.config_file_content_entry.delete(1.0, 'end')

    def save_preset(self) -> None:
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
                'pip_packages': pip_packages,
                'config_files': self.config_files_presets
            }}
        save_json(preset_values)
        self.root.destroy()

    def delete_from_listbox(self) -> None:
        selection = self.package_list.curselection()
        if not selection:
            return
        for selected_i in reversed(selection):
            self.package_list.delete(selected_i)

    def add_to_listbox(self, event=None) -> None:
        package_name = self.package_entry.get()
        if package_name:
            self.package_list.insert('end', package_name)
            self.package_entry.delete(0, 'end')

    def run(self) -> None:
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Setup Preset')
    root.geometry('1080x900')
    root.resizable(False, False)
    app = SetupApp(root)
    root.mainloop()
