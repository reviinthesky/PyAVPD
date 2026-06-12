import json
from .path import get_base_path

SAVE_PATH = get_base_path('presets/presets.json')


class SaveSystem:
    def save_json(self, new_preset: dict[str, dict]) -> None:
        try:
            preset_name, = new_preset.keys()
        except Exception as e:
            print(e)
            return
        data = self.get_json_data()
        data[preset_name] = new_preset[preset_name]
        with open(
                SAVE_PATH,
                'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

    def get_json_data(self) -> dict:
        try:
            with open(
                    SAVE_PATH,
                    'r', encoding='utf-8') as file:
                result_data = json.load(file)
        except FileNotFoundError:
            result_data = {}

        return result_data

    def get_required_key(self, key) -> dict:
        data = self.get_json_data()
        return data.get(key, {})
