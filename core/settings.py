from data.settings_manager import load_settings

_settings = load_settings()

def get_settings(key, default = None):
    return _settings.get(key, default)

def reload_settings():
    global _settings

    _settings = load_settings()

    return _settings