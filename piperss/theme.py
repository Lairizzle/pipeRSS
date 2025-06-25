import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.config/piperss/theme.conf")


def get_style(key, default):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get("theme", key, fallback=default)


theme_title = get_style("title", "dark_orange")
theme_header = get_style("header", "light_goldenrod3")
theme_accent = get_style("accent", "yellow3")
theme_border = get_style("border", "grey37")
theme_error = get_style("error", "indian_red")
