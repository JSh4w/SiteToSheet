import os
from pathlib import Path
from dotenv import load_dotenv
import json

def get_config_dir():
    if os.name  == 'nt':
        return Path(os.getenv('LOCALAPPDATA')) / 'SiteToSheet'
    else:
        return Path.home() / '.config' / 'SiteToSheet'

CONFIG_DIR = get_config_dir()
ENV_FILE = CONFIG_DIR / '.env'
CREDENTIALS_FILE = CONFIG_DIR / 'sheets_credentials.json'

def create_template_env():
    template = """
# SiteToSheet config
#Google API key
GOOGLE_API_KEY="your_google_api_key"

#Google sheets ID- this can be taken from online  
SHEET_ID="your_sheet_id"

    """
    with open(ENV_FILE, 'w') as f:
        f.write(template.strip())

def create_template_credentials():
    template = {
        "type": "service_account",
        "project_id": "your_project_id",
        "private_key_id": "your_private_key_id",
        "private_key": "your_private_key",
        "client_email": "your_client_email",
        "client_id": "your_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "your_client_x509_cert_url",
        "universe_domain": "googleapis.com"
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(template, f, indent=2)

def load_configuration():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    
    if not ENV_FILE.exists():
        create_template_env()
        print(f"Created template .env file at {ENV_FILE}")
        print("Please edit this file and add your actual API keys and settings.")
    else:
        load_dotenv(ENV_FILE)
    
    if not CREDENTIALS_FILE.exists():
        create_template_credentials()
        print(f"Created template credentials file at {CREDENTIALS_FILE}")
        print("Please replace the placeholder values with your actual Google Sheets credentials.")
    
    # Verify that required environment variables are set
    required_vars = ['GOOGLE_API_KEY', 'SHEET_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: The following required environment variables are not set: {', '.join(missing_vars)}")
        print(f"Please edit the .env file at {ENV_FILE} and add these variables.")
    
    # You could return a configuration object here if needed
    return {var: os.getenv(var) for var in required_vars}
  
# Load the configuration when this module is imported
config = load_configuration()

# Export the configuration and other necessary items
__all__ = ['config', 'CONFIG_DIR', 'ENV_FILE', 'CREDENTIALS_FILE']