import os
import json

CONFIG_DIR = os.path.expanduser("~/.tvx")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def ensure_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)


def load_config():
    ensure_config()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    ensure_config()
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def set_key(key, value):
    config = load_config()
    config[key] = value
    save_config(config)


def get_key(key):
    config = load_config()
    return config.get(key)
