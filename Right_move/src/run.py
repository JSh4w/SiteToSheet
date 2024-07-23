#!/usr/bin/env python3

import argparse
import sys
import pathlib
from SiteToSheet.config import config, load_configuration, CREDENTIALS_FILE
from SiteToSheet.main import SiteToSheet
from SiteToSheet.utils.shelf_functions import clear_shelf, print_shelf_data
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps','-gm',action='store_true', help='Enable Google Maps')
    parser.add_argument('--remove_shelf','-rs', action='store_true', help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true', help='Print All Current Shelf')
    parser.add_argument('--gs_merge','-gs_m', action='store_true', help='Updates all links in the sheet')
    parser.add_argument('--update_config','-uc', action='store_true', help='Update config file')
    parser.add_argument('--update_sheet_id','-us', type=str, help='Update sheet id')
    return parser.parse_args()

def update_config():
    print("Updating config...")
    config = load_configuration()
    print(f"Config updated: {config}")

def main():
    args = parse_arguments()

    if args.update_config:
        update_config()
        exit()
    if args.update_sheet_id:
        #TODO create function to update config 
        config['SHEET_ID'] = args.update_sheet_id
        update_config()
        exit()

    #set current directory 
    base_dir= pathlib.Path.cwd()
    #set storage directry for local data
    #TODO update to more local area for running package 
    storage_dir = base_dir / 'src' / 'SiteToSheet' / 'local_storage' / 'link_data'

    if args.remove_shelf:
        clear_shelf(storage_dir)
        print("Clearing shelf, ending script")
        exit()
    if args.print_shelf:
        print_shelf_data(storage_dir, 'link_data')
        print('\n')
        print_shelf_data(storage_dir, 'auxilliary')   
        exit()  
    
    #try:
    SiteToSheet(args.gmaps, args.gs_merge, storage_dir=storage_dir, credentials_file=CREDENTIALS_FILE)
    #except Exception as e:
    #    print(f"An error occurred: {e}", file=sys.stderr)
    #    sys.exit(1)

if __name__ == '__main__':
    main()
