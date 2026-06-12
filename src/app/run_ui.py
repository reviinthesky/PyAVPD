import tkinter as tk
from tkinter import filedialog
from .setup_ui import COLORS, SetupApp


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        main_frame = tk.Frame(
            self.root,
            bg=COLORS['bg_main'])
        main_frame.pack(fill='both', expand=1, pady=20, padx=20)

        # ______ tabs ______

        tabs_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        tabs_frame.grid(row=0, sticky='ew', pady=(0, 40))
        tabs_frame.columnconfigure(0, weight=1)
        tabs_frame.columnconfigure(1, weight=1)

        # button for this window
        self.deploy_button = self.create_tab_button(
            tabs_frame,
            text='Deploy',
            command=self.show_deploy_tab,
            is_active=True
        )
        self.deploy_button.grid(row=0, column=0, padx=(0, 10), sticky='ew')

        # button for add/edit window setup_ui.py
        self.setup_button = self.create_tab_button(
            tabs_frame,
            text='Setup',
            command=self.open_setup_window
        )
        self.setup_button.grid(row=0, column=1, padx=(10, 0), sticky='ew')

        #  ______ find project folder  ______

        find_dir_frame = tk.Frame(
            main_frame, bg=COLORS['bg_frame'], bd=1, relief='solid')
        find_dir_frame.grid(row=1, sticky='ew', pady=30)
        find_dir_frame.columnconfigure(0, weight=3)
        find_dir_frame.columnconfigure(1, weight=1)

        self.dir_var = tk.StringVar(value='Project folder not selected')
        dir_label = tk.Label(
            find_dir_frame,
            textvariable=self.dir_var,
            fg=COLORS['text_primary'],
            bg=COLORS['bg_entry'],
            justify='left',
            padx=15,
            pady=12,
            font=('Arial', 11),
            anchor='w')
        dir_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky='ew')

        browse_button = SetupApp.create_styled_button(
            find_dir_frame,
            text='Select project folder',
            command=self.browse_folders)
        browse_button.grid(row=0, column=1, padx=(0, 15), pady=10)

        # ______ big setup button ______
        setup_frame = tk.Frame(
            main_frame, bg=COLORS['bg_main']
        )
        setup_frame.grid(row=2, pady=40)
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

    def create_tab_button(
            self, parent: tk.Frame, text: str,
            command, is_active: bool = False) -> tk.Button:
        bg_color = COLORS['accent'] if is_active else COLORS['button_normal']
        fg_color = 'white' if is_active else COLORS['text_primary']

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            activebackground=(
                '#4A7BF3' if is_active
                else COLORS['button_hover']),
            activeforeground='white' if is_active else COLORS['text_primary'],
            relief='flat',
            padx=25,
            pady=15,
            font=('Arial', 12, 'bold'),
            cursor='hand2'
        )

        btn.bind('<Enter>', lambda e: btn.config(
            bg='#4A7BF3' if is_active else COLORS['button_hover'],
            fg='white' if is_active else COLORS['text_primary']
        ))
        btn.bind('<Leave>', lambda e: btn.config(
            bg=bg_color,
            fg=fg_color
        ))

        return btn

    def open_setup_window(self):
        setup_root = tk.Toplevel(self.root)
        setup_root.title('Setup Configuration')
        setup_root.geometry('600x600')
        setup_root.resizable(False, False)

        setup_app = SetupApp(setup_root)
        setup_app.run()

        self.setup_button.config(
            bg=COLORS['accent'],
            fg='white'
        )
        self.deploy_button.config(
            bg=COLORS['button_normal'],
            fg=COLORS['text_primary']
        )

    def browse_folders(self) -> None:
        dir_path = filedialog.askdirectory(
            title='Select folder',
            initialdir='/'
        )
        if dir_path:
            self.dir_var.set(dir_path)

    def show_deploy_tab(self) -> None:
        # Активируем вкладку Deploy
        self.deploy_button.config(
            bg=COLORS['accent'],
            fg='white'
        )
        self.setup_button.config(
            bg=COLORS['button_normal'],
            fg=COLORS['text_primary']
        )

    def run(self) -> None:
        self.root.mainloop()

    def deploy(self) -> None:
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Setup Preset')
    root.geometry('1080x900')
    root.resizable(False, False)
    app = MainWindow(root)
    root.mainloop()
