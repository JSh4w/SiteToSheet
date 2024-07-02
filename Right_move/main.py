import os 
import pathlib
import itertools

from api_clients.google_maps_client import GoogleMapsClient
from api_clients.google_sheets_client import GoogleSheetsClient
from scrapers.web_scraping import WebDataHunter
from utils.shelf_functions import *


def main(
    gmaps_on : bool,
    gs_merge : bool,
    storage_dir : pathlib.Path
    ):

    #get maps api key
    google_maps_api_key = os.getenv('GOOGLE_API_KEY') 
    #get google sheets id
    googe_sheets_id=os.getenv('SHEET_ID')

    #cerate gsheets instance
    gsheets_instance = GoogleSheetsClient(sheet_id=googe_sheets_id, path_to_json_cred="sheets_credentials.json")
    #this gets the workbook and makes the API call
    gsheets_instance.retrieve_google_sheet()
    #set headers and tenant info
    try:
        gsheets_instance.gs_headers = get_shelf_data(storage_dir, "auxilliary")['headers']
        gsheets_instance.tenant_info = get_shelf_data(storage_dir, "auxilliary")['tenant_info']
    #if gs_headers and tenant info not set, KeyError will be raised as they will not be found 
    except KeyError:
        gsheets_instance.gs_headers = gsheets_instance.extract_headers()
        gsheets_instance.tenant_info = gsheets_instance.extract_tenant_info()
        update_auxilliary_shelf(storage_dir,{"headers":gsheets_instance.gs_headers})
        update_auxilliary_shelf(storage_dir,{"tenant_info":gsheets_instance.tenant_info})

    #get links to search
    links_to_search, previous_links = check_links_shelf(storage_dir, gsheets_instance.extract_links())
    print(f"Data to search and add to sheets \n {links_to_search}")

    #### Now all updated info is in the shelf or in links_to_search ####
    
    #fill in shelf data and update google sheets
    if gmaps_on and links_to_search is not None:
        #set limit for data to search to not overload API's requests
        ### ADD OVERRIDE / EXPONENTIAL BACKOFF ### 
        set_limit = 10
        #start class instance
        gmaps_instance = GoogleMapsClient(api_key=google_maps_api_key)
        headers = get_shelf_data(storage_dir, "auxilliary")['headers']
        tenant_info = get_shelf_data(storage_dir, "auxilliary")['tenant_info']

        #if deleted info / can check if searched before or not 
        ### NOT FULLY TESTED ### 
        if gs_merge:
            all_shelfed_data = get_shelf_data(storage_dir)
            for i in itertools.islice(previous_links, set_limit):
                if i in all_shelfed_data:
                    gs_update_info = all_shelfed_data[i]
                gsheets_instance.update_listing_info(gs_update_info)

        for i in itertools.islice(links_to_search, set_limit):
                web_instance = WebDataHunter()
                link = i
                try:
                    web_info = web_instance.link_info(link)
                except Exception as e:
                    print(e)
                    print("link not found, backed out of data search")
                    continue 
                start = web_info['Location']
                gmaps_instance.set_start(start)
                #compares with googlesheets to only search if tenant info in the headers
                for i in headers:
                    for j in tenant_info:
                        if (j in i) and (tenant_info[j][0] in i):
                            name = j 
                            destination = tenant_info[name][1]
                            time_to_destination = gmaps_instance.time_to_destination(destination)
                            web_info[i] = time_to_destination
                gsheets_instance.update_listing_info(web_info)
                update_shelf(storage_dir, {link: web_info})

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps','-gm',action='store_true', help='Enable Google Maps')
    parser.add_argument('--remove_shelf','-rs', action='store_true', help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true', help='Print All Current Shelf')
    parser.add_argument('--gs_merge','-gs_m', action='store_true', help='Updates all links in the sheet')
    args = parser.parse_args()

    #set current directory 
    base_dir= pathlib.Path.cwd()
    #set storage directry for local data
    storage_dir = base_dir / 'local_storage' / 'house_data'

    #deal with shelf clearing/ printing seperatey 
    if args.remove_shelf:
        clear_shelf(storage_dir)
        print("Clearing shelf, ending script")
        exit()
    if args.print_shelf:
        print_shelf_data(storage_dir, 'house_data')
        print('\n')
        print_shelf_data(storage_dir, 'auxilliary')   
        exit()  

    main(args.gmaps, args.gs_merge, storage_dir=storage_dir)

