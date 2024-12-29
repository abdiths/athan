import json
from pathlib import Path

class SettingsManager:
    def load_config(self, location_entry):
        config_path = Path.home() / '.config' / 'athan-app' / 'config.json'
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                location_entry.set_text(config.get('location', ''))
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump({'location': ''}, f)
    
    def save_config(self, city):
        config_path = Path.home() / '.config' / 'athan-app' / 'config.json'
        with open(config_path, 'w') as f:
            json.dump({'location': city}, f)
