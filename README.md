# PyAVPD (Python Auto Venv & Pip Deploy)

Automatically set up a virtual environment in your project, install all required packages, and configure necessary files

Set it up once and forget about repetitive environment configuration tasks!

## Features

- One‑click deployment: Deploy a complete Python environment with a single button press.
- Preset management: Create, edit, and reuse presets for different projects.
- Flexible Python version selection: Choose the exact Python interpreter for your project.
- Dependency control: Specify package names and versions.
- Custom config files: Add any configuration files (e.g., `.env`, `config.json`) directly in the preset.

## Quick-start

1. **Clone the repository:**
   ```git clone https://github.com/reviinthesky/PyAVPD.git```
2. **Navigate to the project folder**
    ```cd <cloned-repository-directory>```
3. **Run the application**
    ```python -m src.app.main```

## HOW TO USE
### Main Window
1. **Select Project Directory**
2. **Choose a preset** - pick from your presets or create/edit them in the preset editor. You also can edit .json file if you want to!
3. **Deploy** - click the deployment button and the tool will:
    - Create a venv
    - install packages
    - create config files

### Preset Editor
1. Select folder with exact python interpreter you need(it should contain python.exe)
2. Add pip packages one at a time(e.g flake8, Django==3.2.16)
3. Config files:
    - Enter name
    - Paste the full config file
    - Press save
    - You can edit it right there if you remembered something
4. Choose a preset name
5. Save preset
