import subprocess

from pathlib import Path
from .save_system import SaveSystem
from .path import get_base_path

save = SaveSystem()
temp_dir = get_base_path('temp/requirements.txt')
bat_dir = get_base_path('deploy.bat')


def get_preset(key: str) -> tuple[str, dict]:
    return key, save.get_required_key(key)


def make_temp_requirements_file(key_dict: tuple[str, dict]):
    key, data = key_dict
    packages: str = '\n'.join(data[key].get('pip_packages', []))
    if not packages:
        return
    with open(temp_dir, 'w', encoding='utf-8') as file:
        file.write(packages)


def run_bat(project_dir: str, key_dict: tuple[str, dict]):
    # TODO: error handling
    _, data = key_dict
    python_dir = data.get('python_dir', '')
    requirements_dir = temp_dir if Path(temp_dir).exists() else ''
    args: list[str] = [
        bat_dir, project_dir,
        python_dir, requirements_dir]
    config_files = data.get('config_files', {})
    if config_files:
        for k, v in config_files.items():
            args.extend([k, v])
    result = subprocess.run(
        args, capture_output=True,
        text=True,
        timeout=60
    )
    return result
