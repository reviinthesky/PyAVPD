import tkinter as tk
from tkinter import filedialog

COLORS = {
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


def make_frame(
        master: tk.Frame | tk.Tk,
        sticky='ew',
        pady=(0, 20),
        **kwargs) -> tk.Frame:
    frame = tk.Frame(
        master, bd=1, relief='solid',
        bg=COLORS['bg_frame'])
    frame.grid(sticky=sticky, pady=pady, **kwargs)
    return frame


def make_button(
        master: tk.Frame, text: str, command,
        **kwargs) -> tk.Button:
    btn = tk.Button(
        master,
        text=text,
        command=command,
        bg=COLORS['button_normal'],
        fg=COLORS['text_primary'],
        activebackground=COLORS['button_hover'],
        activeforeground=COLORS['text_primary'],
        relief='flat',
        padx=15,
        pady=8,
        font=('Arial', 10, 'bold'),
        cursor='hand2'
    )

    btn.bind('<Enter>', lambda e: btn.config(
        bg=COLORS['button_hover']))
    btn.bind('<Leave>', lambda e: btn.config(
        bg=COLORS['button_normal']))

    btn.grid(**kwargs)
    return btn


def make_label(master: tk.Frame, text: str, **kwargs) -> tk.Label:
    label = tk.Label(
        master,
        fg=COLORS['text_secondary'],
        bg=COLORS['bg_frame'],
        font=('Arial', 10),
    )
    label.grid(**kwargs)
    return label


class ParentUI:
    def __init__(
            self, root: tk.Tk | tk.Toplevel, dir_var_text: str,
            browse_button_text: str = 'Browse folders') -> None:
        self.root = root
        self.root.configure(bg=COLORS['bg_main'])
        self.main_frame = tk.Frame(self.root, bg=COLORS['bg_main'])
        self.main_frame.pack(fill='both', expand=1, pady=20, padx=20)

        self.find_dir_frame = make_frame(self.main_frame, row=0)
        self.find_dir_frame.columnconfigure(0, weight=1)

        self.dir_var = tk.StringVar(value=dir_var_text)
        dir_label = tk.Label(
            self.find_dir_frame,
            textvariable=self.dir_var,
            justify='left',
            fg=COLORS['text_primary'],
            bg=COLORS['bg_entry'],
            padx=10,
            pady=8,
            font=('Arial', 10))

        dir_label.grid(
            column=0, row=0,
            sticky='ew', padx=10, pady=10)
        browse_button = make_button(
            self.find_dir_frame,
            text=browse_button_text,
            command=self.browse_folders,
            row=0,
            column=1,
            padx=(5, 10))

    def browse_folders(self) -> None:
        dir_path = filedialog.askdirectory(
            title='Select folder',
            initialdir='/'
        )
        if dir_path:
            self.dir_var.set(dir_path)
