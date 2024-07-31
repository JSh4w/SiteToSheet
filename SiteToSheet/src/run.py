#!/usr/bin/env python3

import argparse
import sys
import pathlib
from SiteToSheet.config import load_configuration, CREDENTIALS_FILE, update_env_config
#from SiteToSheet.main import site_to_sheet
from SiteToSheet.main import SiteToSheetProcessor
from SiteToSheet.utils.shelf_functions import clear_shelf, print_shelf_data
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps','-gm',action='store_true', help='Enable Google Maps')
    parser.add_argument('--remove_shelf','-rs', action='store_true', help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true', help='Print All Current Shelf')
    parser.add_argument('--gs_merge','-gs_m', action='store_true', help='Updates all links in the sheet')
    parser.add_argument('--update_config','-uc', action='store_true', help='Update config file')
    parser.add_argument('--update_sheet_id','-us', type=str, help='Update sheet id')

    # Add arguments for setting configuration values
    parser.add_argument("--set-google-api-key", type=str, help="Set Google API Key")
    parser.add_argument("--set-sheet-id", type=str, help="Set Google Sheet ID")
    return parser.parse_args()

def main():
    args = parse_arguments()

    config = load_configuration()

    if args.set_google_api_key:
        update_env_config(key="GOOGLE_API_KEY", value=args.set_google_api_key)
    if args.set_sheet_id:
        update_env_config(key="SHEET_ID", value=args.set_sheet_id)

    # Check for missing configuration
    #if not config.google_api_key or not config.sheet_id:
    #    print("Error: Missing configuration. Please set the following:")
    #    if not config.google_api_key:
    #        print("- Google API Key (use --set-google-api-key)")
    #    if not config.sheet_id:
    #        print("- Sheet ID (use --set-sheet-id)")
    #    return  # 

    #set current directory 
    base_dir= pathlib.Path.cwd()
    storage_dir = base_dir / 'local_storage' / 'link_data'

    if args.remove_shelf:
        clear_shelf(storage_dir)
        print("Clearing shelf, ending script")
        exit()
    if args.print_shelf:
        print_shelf_data(storage_dir, 'link_data')
        print('\n')
        print_shelf_data(storage_dir, 'auxilliary')   
        exit()  
    
    site_to_sheet = SiteToSheetProcessor(storage_directory=storage_dir, credentials_filepath=CREDENTIALS_FILE)
    site_to_sheet.initialize_clients()
    site_to_sheet.update_headers_and_destination_info(force_update=args.update_sheet_id)
    site_to_sheet.get_links()
    site_to_sheet.process_links_update_sheet(enable_google_maps=args.gmaps, force_link_process=args.gs_merge)

if __name__ == '__main__':
    main()
