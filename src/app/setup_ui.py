import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import Any
from pathlib import Path


class SetupApp():
    def __init__(self, root: tk.Tk) -> None:
        self.colors = {
            'bg_main': '#0E0E0E',
            'bg_frame': '#1A1A1A',
            'bg_entry': '#2D2D2D',
            'text_primary': '#E0E0E0',
            'text_secondary': '#A0A0A0',
            'accent': '#5D8BF4',
            'button_normal': '#3A3A3A',
            'button_hover': '#4A4A4A',
            'listbox_bg': '#252525',
            'entry_hl': '#404040'
        }
        self.config_files_presets: dict[str, str] = {}
        self.root = root
        self.root.configure(bg=self.colors['bg_main'])
        main_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=1, pady=20, padx=20)

        # ________find python folder________
        find_dir_frame = tk.Frame(
            main_frame,
            bg=self.colors['bg_frame'],
            bd=1, relief='solid'
        )
        find_dir_frame.grid(row=0, sticky='ew', pady=(0, 20))
        find_dir_frame.columnconfigure(0, weight=1)

        self.dir_var = tk.StringVar(value='Python folder not selected')
        dir_label = tk.Label(
            find_dir_frame,
            textvariable=self.dir_var,
            justify='left',
            fg=self.colors['text_primary'],
            bg=self.colors['bg_entry'],
            padx=10,
            pady=8,
            font=('Arial', 10))

        dir_label.grid(
            column=0, row=0,
            sticky='ew', padx=10, pady=10)

        browse_button = self.create_styled_button(
            find_dir_frame,
            text='Select python folder',
            command=self.browse_folders)
        browse_button.grid(
            row=0,
            column=1,
            padx=(5, 10))

        # ________make pip list________
        entry_frame = tk.Frame(
            main_frame, bg=self.colors['bg_frame'], bd=1, relief='solid')
        entry_frame.grid(row=1, sticky='ew', pady=(0, 20))
        entry_frame.columnconfigure(0, weight=1)

        self.package_entry = tk.Entry(
            entry_frame,
            bg=self.colors['bg_entry'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            width=30,
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.colors['entry_hl'])
        self.package_entry.grid(
            row=0, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.package_entry.bind('<Return>', self.add_to_listbox)

        add_button = self.create_styled_button(
            entry_frame,
            text='Add package',
            command=self.add_to_listbox
        )
        add_button.grid(row=0, column=1, padx=(5, 10))

        self.package_list = tk.Listbox(
            entry_frame,
            selectmode='multiple',
            bg=self.colors['listbox_bg'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            font=('Arial', 10),
            relief='flat',
            highlightthickness=0,
            height=8)
        self.package_list.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

        remove_button = self.create_styled_button(
            entry_frame,
            text='Remove packages',
            command=self.delete_from_listbox
        )
        remove_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # ________config files________
        config_files_frame = tk.Frame(
            main_frame, bg=self.colors['bg_frame'], bd=1, relief='solid'
        )
        config_files_frame.grid(row=2, sticky='ew', pady=(0, 20))
        config_files_frame.columnconfigure(1, weight=1)

        config_file_name_label = tk.Label(
            config_files_frame,
            text='Enter config file name:',
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_frame'],
            font=('Arial', 10))
        config_file_name_label.grid(
            row=0, column=0, padx=(10, 5), pady=10, sticky='w')

        self.config_file_name_entry = tk.Entry(
            config_files_frame,
            bg=self.colors['bg_entry'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.colors['entry_hl']
        )
        self.config_file_name_entry.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky='ew'
        )

        config_file_content_label = tk.Label(
            config_files_frame,
            text='Enter config file content:',
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_frame'],
            font=('Arial', 10))
        config_file_content_label.grid(
            row=1, column=0, padx=(10, 5), pady=(0, 5), sticky='nw')

        self.config_file_content_entry = tk.Text(
            config_files_frame,
            bg=self.colors['bg_entry'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            font=('Arial', 10),
            relief='flat',
            highlightthickness=1,
            highlightbackground='#404040',
            wrap='word',
            height=6)
        self.config_file_content_entry.grid(
            row=1, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')

        config_files_listbox_label = tk.Label(
            config_files_frame,
            text='Config files list:',
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_frame'],
            font=('Arial', 10)
        )
        config_files_listbox_label.grid(
            row=0, column=2, padx=(20, 10), pady=(10, 5), sticky='w'
        )

        self.config_files_listbox = tk.Listbox(
            config_files_frame,
            bg=self.colors['listbox_bg'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
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
        save_config_button = self.create_styled_button(
            config_files_frame,
            text='Save config file',
            command=self.save_config_file
        )
        save_config_button.grid(
            row=2, column=0, columnspan=2, pady=(0, 10))

        # ________save preset________
        save_preset_frame = tk.Frame(
            main_frame, bg=self.colors['bg_frame'], bd=1, relief='solid')
        save_preset_frame.grid(row=3, sticky='ew')
        save_preset_frame.columnconfigure(1, weight=1)
        preset_name_label = tk.Label(
            save_preset_frame,
            text='Enter preset name:',
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_frame'],
            font=('Arial', 10))
        preset_name_label.grid(
            row=0, column=0, padx=(10, 5), pady=10, sticky='w')

        self.preset_name = tk.Entry(
            save_preset_frame,
            bg=self.colors['bg_entry'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            font=('Arial', 11),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.colors['entry_hl']
        )
        self.preset_name.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky='ew')

        save_button = self.create_styled_button(
            save_preset_frame,
            text='Save preset',
            command=self.save_preset
        )
        save_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))

    def choose_config_file_content(self, event=None) -> None:
        file_name: str = self.config_files_listbox.get('anchor')
        file_content: str = self.config_files_presets[file_name]
        self.config_file_content_entry.delete(1.0, 'end')
        self.config_file_content_entry.insert(1.0, file_content)
        self.config_file_name_entry.delete(0, 'end')
        self.config_file_name_entry.insert(0, file_name)

    def create_styled_button(
            self, parent: tk.Frame, text: str,
            command) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors['button_normal'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['button_hover'],
            activeforeground=self.colors['text_primary'],
            relief='flat',
            padx=15,
            pady=8,
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        # Эффект наведения
        btn.bind('<Enter>', lambda e: btn.config(
            bg=self.colors['button_hover']))
        btn.bind('<Leave>', lambda e: btn.config(
            bg=self.colors['button_normal']))

        return btn

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
            }
        }
        with open('presets/presets.json', 'a', encoding='UTF-8') as file:
            json.dump(preset_values, file, indent=2)

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
    root.geometry('1080x900')
    root.resizable(False, False)
    app = SetupApp(root)
    root.mainloop()
