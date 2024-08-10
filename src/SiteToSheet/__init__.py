"""
This is the main module of the SiteToSheet project.
It imports and exports various functions and classes used throughout the project.
"""

from .config import load_configuration, update_env_config, CONFIG_DIR, ENV_FILE, CREDENTIALS_FILE
from .main import SiteToSheetProcessor
from .scrapers.web_scraping import WebDataHunter
from .utils.shelf_functions import (
    make_data_shelf,
    get_shelf_data,
    print_shelf_data,
    check_links_shelf,
    update_shelf,
    clear_shelf,
    update_auxilliary_shelf
)
from .api_clients.google_maps_client import GoogleMapsClient
from .api_clients.google_sheets_client import GoogleSheetsClient

# Export all functions you might want to use
__all__ = [
    'load_configuration',
    'update_env_config',
    'CONFIG_DIR',
    'ENV_FILE',
    'CREDENTIALS_FILE',
    'SiteToSheetProcessor',
    'WebDataHunter',
    'make_data_shelf',
    'get_shelf_data',
    'print_shelf_data',
    'check_links_shelf',
    'update_shelf',
    'clear_shelf',
    'update_auxilliary_shelf',
    'GoogleMapsClient',
    'GoogleSheetsClient'
]
