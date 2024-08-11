#!/usr/bin/env python3
"""
This module provides a command-line interface for the SiteToSheet application.
It allows users to interact with the application by specifying various command-line arguments.
"""
import sys
import argparse
import pathlib
from SiteToSheet.config import load_configuration, CREDENTIALS_FILE, ENV_FILE, update_env_config
from SiteToSheet.main import SiteToSheetProcessor
from SiteToSheet.utils.shelf_functions import clear_shelf, print_shelf_data
def parse_arguments():
    """
    Parses the command line arguments and returns the parsed arguments.

    This function uses the argparse module to define and parse command line arguments.
    It supports the following arguments:

    - --gmaps or -gm: Enable Google Maps.
    - --remove_shelf or -rs: Clear the current shelf.
    - --print_shelf or -ps: Print all current shelf data.
    - --gs_merge or -gs_m: Updates all links in the sheet.
    - --update_config or -uc: Update the configuration file.
    - --update_sheet_id or -us: Update the sheet ID.
    - --set-google-api-key: Set the Google API Key.
    - --set-sheet-id: Set the Google Sheet ID.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps','-gm',action='store_true',
                        help='Enable Google Maps')
    parser.add_argument('--remove_shelf','-rs', action='store_true',
                        help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true',
                        help='Print All Current Shelf')
    parser.add_argument('--gs_merge','-gs_m', action='store_true',
                        help='Updates all links in the sheet')
    parser.add_argument('--update_config','-uc', action='store_true',
                        help='Update config file')
    parser.add_argument('--update_sheet_id','-us', type=str,
                        help='Update sheet id')

    # Add arguments for setting configuration values
    parser.add_argument("--set-google-api-key", type=str, help="Set Google API Key")
    parser.add_argument("--set-sheet-id", type=str, help="Set Google Sheet ID")
    return parser.parse_args()

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
