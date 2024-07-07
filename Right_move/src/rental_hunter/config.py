import os
from pathlib import Path
from dotenv import load_dotenv

def get_config_dir():
    if os.name  == 'nt':
        return Path(os.getenv('LOCALAPPDATA')) / 'rental_hunter'
    else:
        return Path.home() / '.config' / 'rental_hunter'

CONFIG_DIR = get_config_dir()
ENV_FILE = CONFIG_DIR / '.env'
CREDENTIALS_FILE = CONFIG_DIR / 'sheet_credentials.json'

def load_configuration():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    

    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
    else:
        print(f"Warn ing: .env file not found at {ENV_FILE}")

    if not CREDENTIALS_FILE.exists():
        print(f"Warning: sheet_credentials.json not found at {CREDENTIALS_FILE}")

# Call this function when your package initializes

## add this in later
#load_configuration()