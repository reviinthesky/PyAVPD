import json
from src.app.path import get_base_path
from pathlib import Path


def save_json(new_preset: dict[str, dict]) -> None:
    try:
        preset_name, = new_preset.keys()
    except Exception as e:
        print(e)
        return
    with open(
            get_base_path(f'presets/{preset_name}.json'), 'w',
            encoding='utf-8') as file:
        json.dump(new_preset, file, indent=2)


def get_json_data(preset_name: str) -> dict:
    try:
        with open(
                get_base_path(f'presets/{preset_name}.json'),
                'r', encoding='utf-8') as file:
            result_data = json.load(file)
    except FileNotFoundError:
        print(f'{preset_name} not found')
        result_data = {}

    return result_data


def get_all_preset_keys() -> list[str]:
    folder_path = Path(get_base_path('presets/'))
    return [file.name.replace('.json', '') for file in folder_path.glob('*.json')]
