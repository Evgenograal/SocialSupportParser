import json

Settings_file = "data/settings.json"

def load_settings():
    with open(Settings_file, "r", encoding = "utf-8") as f:
        return json.load(f)
    
def save_settings(data):
    with open(Settings_file, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def get_settings(key, default = None):
    data = load_settings()
    return data.get(key, default)