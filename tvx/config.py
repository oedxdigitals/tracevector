import json
import os

CONFIG_PATH = os.path.expanduser("~/.tracevector_config.json")


def _load():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def set_key(key: str, value: str):
    config = _load()
    config[key] = value
    _save(config)


def get_key(key: str, default=None):
    config = _load()
    return config.get(key, default)
