"""
config.py

This module provides functions for managing the configuration of the SiteToSheet application.
"""

import os
from pathlib import Path
import json
from dotenv import load_dotenv, set_key

def get_config_dir():
    """
    Returns the configuration directory for the SiteToSheet application.

    The configuration directory is determined based on the operating system.
    On Windows, it is located in the LOCALAPPDATA directory.
    On other operating systems, it is located in the .config directory in the user's home directory.

    Returns:
        Path: The configuration directory for the SiteToSheet application.
    """
    if os.name  == 'nt':
        return Path(os.getenv('LOCALAPPDATA')) / 'SiteToSheet'
    return Path.home() / '.config' / 'SiteToSheet'

CONFIG_DIR = get_config_dir()
ENV_FILE = CONFIG_DIR / '.env'
CREDENTIALS_FILE = CONFIG_DIR / 'sheets_credentials.json'

def create_template_env():
    """
    Creates a template environment file at the specified path.

    This function generates a template environment file with default values for 
    GOOGLE_API_KEY and SHEET_ID. The file is created at the path specified by 
    the ENV_FILE variable.

    Parameters:
    None

    Returns:
    None
    """
    template = """GOOGLE_API_KEY=SHEET_ID="""
    with open(ENV_FILE, 'w', encoding="UTF-8") as f:
        f.write(template.strip())

def update_env_config(path: Path, key: str, value: str):
    """
    Updates the environment configuration by setting a key-value pair in the environment file.

    Args:
        path (Path): The path to the environment file. If None,
        the default environment file is used.
        key (str): The key to be set in the environment file.
        value (str): The value associated with the key.

    Returns:
        None
    """
    set_key(dotenv_path=ENV_FILE or path, key_to_set=key, value_to_set=value)
    load_dotenv(ENV_FILE, override=True)

def create_template_credentials():
    """
    Creates a template for Google Sheets API credentials and saves it to the specified file.

    This function generates a JSON template for Google Sheets API
    credentials and saves it to the file specified by the `CREDENTIALS_FILE` constant.
    The template includes the following fields:
    - `type`: The type of credentials, set to "service_account".
    - `project_id`: The project ID associated with the credentials.
    - `private_key_id`: The private key ID.
    - `private_key`: The private key.
    - `client_email`: The client email.
    - `client_id`: The client ID.
    - `auth_uri`: The URI for OAuth 2.0 authorization.
    - `token_uri`: The URI for obtaining an access token.
    - `auth_provider_x509_cert_url`: URL for the X.509 certificate of the authentication provider.
    - `client_x509_cert_url`: The URL for the X.509 certificate of the client.
    - `universe_domain`: The universe domain.

    This function does not take any parameters and does not return anything.

    Example usage:
    ```python
    create_template_credentials()
    ```
    """
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
    with open(CREDENTIALS_FILE, 'w', encoding="UTF-8") as f:
        json.dump(template, f, indent=2)

def load_configuration():
    """
    Load the configuration for the application.

    This function checks if the CONFIG_DIR directory exists and creates it if it doesn't.
    It then checks if the ENV_FILE file exists and creates a template .env file if it doesn't.
    The template .env file is created with placeholders for API keys and settings.
    The user is prompted to edit the .env file and add their actual API keys and settings.

    If the CREDENTIALS_FILE file doesn't exist, a template credentials file is created.
    The template credentials file is created with placeholders for Google Sheets credentials.
    The user is prompted to replace the placeholders with their actual Google Sheets credentials.

    The function verifies that the required environment variables are set.
    The required environment variables are 'GOOGLE_API_KEY' and 'SHEET_ID'.
    If any of the required environment variables are missing, a warning is printed.
    The user is prompted to edit the .env file and add the missing variables.

    The function returns a dictionary containing the values of the required environment variables.

    Parameters:
    None

    Returns:
    dict: A dictionary containing the values of the required environment variables.
          The keys of the dictionary are the variable names 
          and the values are the corresponding variable values.
    """
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
        print(f"""Warning: The following required
            environment variables are not set: {', '.join(missing_vars)}""")
        print(f"Please edit the .env file at {ENV_FILE} and add these variables.")

    return {var: os.getenv(var) for var in required_vars}
