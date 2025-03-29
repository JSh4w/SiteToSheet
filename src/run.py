#!/usr/bin/env python3
"""
This module provides a command-line interface for the SiteToSheet application.
It allows users to interact with the application by specifying various command-line arguments.
"""
import sys
import argparse
import pathlib
import logging
from SiteToSheet.config import load_configuration, CREDENTIALS_FILE, ENV_FILE, update_env_config
from SiteToSheet.main import SiteToSheetProcessor
from SiteToSheet.utils.shelf_functions import clear_shelf, print_shelf_data
from SiteToSheet.utils.logging import setup_logger
from SiteToSheet.cli import parse_arguments

logger = logging.getlogger(__name__)


def main():
    """
    The main function of the application, responsible for parsing command line
    arguments and executing the main workflow.

    It first parses the command line arguments using the parse_arguments
    function. Then, it checks for specific flags such as --remove_shelf,
    --print_shelf, and updates the configuration file if necessary.

    The function then initializes the SiteToSheetProcessor with the provided
    storage directory and credentials file. It updates the headers and destination
    information, gets links, and processes the links to update the sheet.

    The function does not return any value.
    """
    # Set base directory and storage directory
    base_dir= pathlib.Path.cwd()
    storage_dir = base_dir / 'local_storage' / 'link_data'
    # Parse arguments from Command line - see parse_arguments()
    args = parse_arguments()
    # Setup logging config
    log_level = getattr(logging, args.log_level)
    setup_logger(name="SiteToSheet", level=log_level, log_file=args.log_file)
    # Clear shelf if --remove_shelf is provided, see utils/shelf_functions.py
    # This is done first as it exits the script
    if args.remove_shelf:
        clear_shelf(storage_dir)
        print("Cleared shelf, ending script")
        sys.exit(0)
    if args.print_shelf:
        print_shelf_data(storage_dir, 'link_data')
        print('\n')
        print_shelf_data(storage_dir, 'auxilliary')
        print("Printing shelf, ending script")
        sys.exit(0)
    # Load configuration file and update environment variables, taken from config.py
    load_configuration()
    # Update environment variables if --set-google-api-key or --set-sheet-id is provided
    if args.set_google_api_key:
        update_env_config(path= ENV_FILE, key="GOOGLE_API_KEY", value=args.set_google_api_key)
    if args.set_sheet_id:
        update_env_config(path= ENV_FILE, key="SHEET_ID", value=args.set_sheet_id)


    site_to_sheet = SiteToSheetProcessor(storage_directory=storage_dir,
                                          credentials_filepath=CREDENTIALS_FILE)
    site_to_sheet.initialize_clients()
    site_to_sheet.update_headers_and_destination_info(force_update=args.update_sheet_id)
    site_to_sheet.get_links()
    #Main function that handles NLP, and distance processing
    site_to_sheet.process_links_update_sheet(
        enable_google_maps=args.gmaps,
        force_link_process=args.gs_merge
        )

if __name__ == '__main__':
    main()
