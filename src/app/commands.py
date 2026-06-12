import subprocess

from pathlib import Path
from typing import Any
from .path import get_base_path
temp_dir = get_base_path('temp\\requirements.txt')
bat_dir = Path('src/app/deploy.bat')


def make_temp_requirements_file(data: dict[str, Any]):
    packages: str = '\n'.join(data.get('pip_packages', []))
    if not packages:
        return
    with open(temp_dir, 'w', encoding='utf-8') as file:
        file.write(packages)


def run_bat(project_dir: str, preset_data: dict[str, dict]):
    try:
        data: dict[str, Any] = next(iter(preset_data.values()))
    except StopIteration:
        print(preset_data)
        print(preset_data.values())
        raise Exception
    make_temp_requirements_file(data)
    python_dir = data.get('python_dir', '')
    requirements_dir = temp_dir if Path(temp_dir).exists() else ''
    args: list[str] = [
        str(bat_dir), project_dir,
        python_dir, requirements_dir]
    subprocess.Popen(
        args, text=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE)

    configs_data = data.get('config_files', {})
    if configs_data:
        for file_name, file_content in configs_data.items():
            path = Path(project_dir) / file_name
            with open(path, 'w', encoding='utf-8') as file:
                file.write(file_content)
