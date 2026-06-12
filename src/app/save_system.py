import json
from .path import get_base_path


def save_json(new_preset: dict[str, dict]) -> None:
    try:
        preset_name, = new_preset.keys()
    except Exception as e:
        print(e)
        return
    with open(
            get_base_path(f'presets/{preset_name}'), 'w',
            encoding='utf-8') as file:
        json.dump(new_preset, file)


def get_json_data(preset_name: str) -> dict:
    try:
        with open(
                get_base_path(f'presets/{preset_name}'),
                'r', encoding='utf-8') as file:
            result_data = json.load(file)
    except FileNotFoundError:
        result_data = {}

    return result_data
