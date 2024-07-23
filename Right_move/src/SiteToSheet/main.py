import os 
import pathlib
import itertools

from .api_clients.google_maps_client import GoogleMapsClient
from .api_clients.google_sheets_client import GoogleSheetsClient
from .scrapers.web_scraping import WebDataHunter
from .utils.shelf_functions import *

def SiteToSheet(
    gmaps_on : bool,
    gs_merge : bool,
    storage_dir : pathlib.Path,
    credentials_file : pathlib.Path
    ):

    #get and set api, keys 
    #get maps api key
    google_maps_api_key = os.getenv('GOOGLE_API_KEY') 
    #get google sheets ids
    google_sheets_id=os.getenv('SHEET_ID')

    #cerate gsheets instance
    gsheets_instance = GoogleSheetsClient(sheet_id=google_sheets_id, path_to_json_cred=credentials_file)
    #this gets the workbook and makes the API call
    gsheets_instance.retrieve_google_sheet()

    try:
        gsheets_instance.gs_headers = get_shelf_data(storage_dir, "auxilliary")['headers']
        gsheets_instance.destination_info = get_shelf_data(storage_dir, "auxilliary")['Info']
    #if gs_headers and  not set, KeyError will be raised as they will not be found 
    except KeyError:
        gsheets_instance.gs_headers = gsheets_instance.extract_headers()
        gsheets_instance.destination_info = gsheets_instance.extract_destination_info()
        update_auxilliary_shelf(storage_dir,{"headers":gsheets_instance.gs_headers})
        update_auxilliary_shelf(storage_dir,{"Info":gsheets_instance.destination_info})

    #get links to search
    print(list(gsheets_instance.gs_headers.keys())[0])
    links_to_search, previous_links = check_links_shelf(storage_dir, gsheets_instance.extract_links())
    print(f"Data to search and add to sheets \n {links_to_search}")

    #### Now all updated info is in the shelf or in links_to_search ####
    
    #fill in shelf data and update google sheets
    if gmaps_on and links_to_search is not None:
        #set limit for data to search to not overload API's requests
        ### ADD OVERRIDE / EXPONENTIAL BACKOFF ### 
        set_limit = 10
        #start class instance
        gmaps_instance = GoogleMapsClient(api_key=str(google_maps_api_key))
        headers = get_shelf_data(storage_dir, "auxilliary")['headers']
        destination_info = get_shelf_data(storage_dir, "auxilliary")['Info']

        #if deleted info / can check if searched before or not 
        ### NOT FULLY TESTED ### 
        if gs_merge:
            all_shelfed_data = get_shelf_data(storage_dir)
            for i in itertools.islice(previous_links, set_limit):
                if i in all_shelfed_data:
                    gs_update_info = all_shelfed_data[i]
                gsheets_instance.update_links_info(gs_update_info)

        for i in itertools.islice(links_to_search, set_limit):
                web_instance = WebDataHunter()
                link = i
                #compares with googlesheets to only search if destination info in the headers

                matches=[]
                destination_matches=[]
                for i in list(headers.keys()):
                    for j in destination_info:
                        if str(j).strip()!=str(i).strip():
                            matches.append(i)
                        else:
                            destination_matches.append(i)
                
                #try:
                web_info = web_instance.link_info(link, matches)
                #except Exception as e:
                #    print(e)
                #    print("link not found, backed out of data search")
                #    continue 
                start = web_info['Location']
                gmaps_instance.set_start(start)
                #compares with googlesheets to only search if tenant info in the headers
                for i in destination_matches:
                    destination = destination_info[i]
                    print(destination)
                    time_to_destination = gmaps_instance.time_to_destination(destination)
                    web_info[i] = time_to_destination
                gsheets_instance.update_links_info(web_info)
                update_shelf(storage_dir, {link: web_info})


