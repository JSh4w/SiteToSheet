import os 
import json 
import pathlib
import itertools

from api_clients.google_maps_client import GoogleMapsClient
from api_clients.google_sheets_client import GoogleSheetsClient
from scrapers.web_scraping import WebDataHunter
from utils.shelf_functions import *


def main(gsheets_on : bool, gmaps_on : bool, update_sheets : bool, remove_shelf : bool, print_shelf : bool):

    #set base dir, maps and sheets keys
    base_dir= pathlib.Path.cwd()
    storage_dir = base_dir / 'local_storage' / 'house_data'
    google_maps_api_key = os.getenv('GOOGLE_API_KEY') 
    googe_sheets_id=os.getenv('SHEET_ID')

    if remove_shelf:
        clear_shelf(storage_dir)
        print("Clearing shelf, no other functions performed if this is true")
        return None 
    if print_shelf:
        print_shelf_data(storage_dir, 'house_data')
        print('\n')
        print_shelf_data(storage_dir, 'auxilliary')        

    #get google sheets data and update shelf 
    if gsheets_on:
        gsheets_instance = GoogleSheetsClient(sheet_id=googe_sheets_id, path_to_json_cred="sheets_credentials.json")
        workbook = gsheets_instance.get_google_sheet()
        listing_headers = gsheets_instance.get_listings_info(workbook)
        tenant_info = gsheets_instance.get_tenant_info(workbook)
        headers= listing_headers[0] #dictionary of headers and respective google sheets column to update 
        links = listing_headers[1] #list of links
        all_data = listing_headers[2] #keys are links, values are lists of data for each link
        search_data = update_shelf(storage_dir, all_data)
        update_auxilliary_shelf(storage_dir,{"headers":headers})
        update_auxilliary_shelf(storage_dir,tenant_info)

        print(f"Data to search and add to sheets \n {search_data}")
    else:
        headers, links, all_data, search_data, tenant_info = None, None, None, None, None 
        print(f"No data taken from googlesheets; current local shelf")
    
    #fill in shelf data and update google sheets
    if gmaps_on and search_data is not None:
        set_limit = 1
        for i in itertools.islice(search_data, set_limit):
                headers = get_shelf_data(storage_dir, "auxilliary")['headers']
                web_instance = WebDataHunter()
                link = str(i)
                try:
                    web_info = web_instance.link_info(link)
                except Exception as e:
                    print(e)
                    print("link not found, backed out of data search")
                    continue
                start = web_info['Location']
                gmaps_instance = GoogleMapsClient(api_key=google_maps_api_key)
                gmaps_instance.set_start(start)
    
                for i in headers:
                    for j in tenant_info:
                        if (j in i) and (tenant_info[j][0] in i):
                            column = headers[i]
                            name = j 
                            end = tenant_info[j][1]
                            time_to_destination = gmaps_instance.time_to_destination(end)
                            web_info[i] = time_to_destination
                gsheets_instance.update_listing_info(workbook, web_info)
                update_shelf(storage_dir, {link: web_info})
                print("\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--gsheets','-gs',action='store_true', help='Enable Google Sheets')
    parser.add_argument('--gmaps','-gm',action='store_true', help='Enable Google Maps')
    parser.add_argument('--update_sheets','-us', action='store_true', help='Update Google Sheets')
    parser.add_argument('--remove_shelf','-rs', action='store_true', help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true', help='Print All Current Shelf')
    args = parser.parse_args()
    main(args.gsheets, args.gmaps, args.update_sheets, args.remove_shelf, args.print_shelf)

