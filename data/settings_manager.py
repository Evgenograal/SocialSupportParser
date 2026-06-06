import json
import os
import shutil

Settings_file = "data/settings.json"

def load_settings():
    with open(Settings_file, "r", encoding = "utf-8") as f:
        return json.load(f)
    
    if not os.path.exists(Settings_file):
        shutil.copy("data/default_settings.json", Settings_file)
    
def save_settings(data):
    with open(Settings_file, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def get_settings(key, default = None):
    data = load_settings()
    return data.get(key, default)