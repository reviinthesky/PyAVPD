import tkinter as tk
from tkinter import messagebox
from .ui_custom import *
from .save_system import get_json_data, get_all_preset_keys
from .setup_ui import SetupApp


class MainWindow(ParentUI):
    def __init__(self, root: tk.Tk):
        self.default_message = 'Select project directory'
        super().__init__(root, self.default_message)
        # ______ preset browser _____
        presets_list = get_all_preset_keys()
        preset_browser_frame = make_frame(
            self.main_frame,
            row=1, column=0, rowspan=3, sticky='ns', padx=(0, 20), pady=0)
        preset_browser_frame.rowconfigure(1, weight=1)

        preset_browser_label = make_label(
            preset_browser_frame,
            text='Select preset',
            padx=10, pady=8, row=1, column=0, sticky='ew')

        setup_button = make_button(
            preset_browser_frame,
            text='Create preset',
            command=self.open_setup_window,
            row=0, column=0, padx=10, sticky='ew', pady=10)
        edit_button = make_button(
            preset_browser_frame,
            text='Edit preset',
            command=self.edit_selected_preset,
            row=0, column=1, padx=10, sticky='ew', pady=10)

        self.presets_listbox = tk.Listbox(
            preset_browser_frame,
            bg=COLORS['listbox_bg'],
            fg=COLORS['text_primary'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            font=('Arial', 10),
            relief='flat',
            highlightthickness=0,
            width=25,
            height=15,
            selectmode='single')
        self.presets_listbox.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        for preset in presets_list:
            self.presets_listbox.insert('end', preset)

        # ______ big setup button ______
        setup_frame = make_frame(self.main_frame, row=4, pady=40)
        setup_frame.columnconfigure(0, weight=1)
        self.setup_button = tk.Button(
            setup_frame,
            text='START DEPLOYMENT',
            command=self.deploy,
            bg=COLORS['accent'],
            fg='white',
            font=('Arial', 14, 'bold'),
            relief='flat',
            padx=40,
            pady=20,
            cursor='hand2'
        )
        self.setup_button.grid(row=0, column=0, sticky='ew')
        self.setup_button.bind(
            '<Enter>', lambda e: self.setup_button.config(bg='#4A7BF3'))
        self.setup_button.bind(
            '<Leave>', lambda e: self.setup_button.config(bg=COLORS['accent']))

    def edit_selected_preset(self) -> None:
        preset_name = self.presets_listbox.get('active')
        if not preset_name:
            return
        preset_data = get_json_data(preset_name)
        self.open_setup_window(preset_data)

    def open_setup_window(self, preset_data: dict[str, dict] | None = None) -> None:
        setup_root = tk.Toplevel(self.root)
        setup_root.title('Setup Preset')
        setup_root.geometry('980x820')
        setup_root.resizable(False, False)

        setup_app = SetupApp(setup_root, preset_data)
        setup_app.run()

    def run(self) -> None:
        self.root.mainloop()

    def deploy(self) -> None:
        preset_name = self.presets_listbox.get('active')
        if not preset_name:
            messagebox.showwarning('Warning', 'Please select preset')
            return  # type: ignore
        if self.dir_var.get() == self.default_message or not self.dir_var.get():
            messagebox.showwarning('Warning', 'Please select project directory')
            return
        preset_data = get_json_data(preset_name)
        self.preset_data = preset_data

        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('PyAVPD')
    root.geometry('480x680')
    root.resizable(False, False)
    app = MainWindow(root)
    root.mainloop()
