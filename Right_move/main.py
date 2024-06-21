import os 
import json 
import pathlib
import itertools

from api_clients.google_maps_client import GoogleMapsClient
from api_clients.google_sheets_client import GoogleSheetsClient
from utils.shelf_functions import *

def main(gsheets_on : bool, gmaps_on : bool, update_sheets : bool, remove_shelf : bool):


    #set base dir, maps and sheets keys
    base_dir= pathlib.Path.cwd()
    storage_dir = base_dir / 'local_storage' / 'house_data'
    google_maps_api_key = os.getenv('GOOGLE_API_KEY') 
    googe_sheets_id=os.getenv('SHEET_ID')

    if remove_shelf:
        clear_shelf(storage_dir)
        print("Clearing shelf, no other functions performed if this is true")
        return None 

    #get google sheets data and update shelf 
    if gsheets_on:
        gsheets_instance = GoogleSheetsClient(sheet_id=googe_sheets_id, path_to_json_cred="sheets_credentials.json")
        workbook = gsheets_instance.get_google_sheet()
        headers_links = gsheets_instance.get_workbook_info(workbook)
        headers= headers_links[0] #dictionary of headers and respective google sheets column to update 
        links = headers_links[1] #list of links
        all_data = headers_links[2] #keys are links, values are lists of data for each link 
        search_data = update_shelf(storage_dir, all_data)
        update_auxilliary_shelf(storage_dir,{"headers":headers})
        print(f"Data to search and add to sheets \n {search_data}")
    else:
        headers, links, all_data, search_data = None, None, None, None
        print(f"No data taken from googlesheets; current local shelf")
    
    search_data = get_shelf_data(storage_dir)
    #fill in shelf data and update google sheets
    if gmaps_on and search_data is not None:
        set_limit = 1
        for i in itertools.islice(search_data, set_limit):
                print(search_data[i])
                links = get_shelf_data(storage_dir, "auxilliary")['headers']

                gmaps_instance = GoogleMapsClient(api_key=google_maps_api_key)
                gmaps_instance.get_distance_matrix(location)

                #start setting these if empty with new data or update with old data
                location = search_data[i][links['Location']]
                print(i)
                print("\n")
        print(get_shelf_data(storage_dir, "auxilliary"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--gsheets','-gs',action='store_true', help='Enable Google Sheets')
    parser.add_argument('--gmaps','-gm',action='store_true', help='Enable Google Maps')
    parser.add_argument('--update_sheets','-us', action='store_true', help='Update Google Sheets')
    parser.add_argument('--remove_shelf','-rs', action='store_true', help='Clear Current Shelf')
    args = parser.parse_args()
    main(args.gsheets, args.gmaps, args.update_sheets, args.remove_shelf)

