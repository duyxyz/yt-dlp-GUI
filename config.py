import os, json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".yt_downloader_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return CONFIG_PATH, data.get("last_folder", os.path.join(os.path.expanduser("~"), "Downloads"))
        except:
            pass
    return CONFIG_PATH, os.path.join(os.path.expanduser("~"), "Downloads")

def save_config(folder):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"last_folder": folder}, f, ensure_ascii=False, indent=2)
    except:
        pass
