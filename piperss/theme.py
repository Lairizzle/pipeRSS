import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.config/piperss/theme.conf")


def get_style(key, default):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get("theme", key, fallback=default)
