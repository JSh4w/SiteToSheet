import os
import pathlib
import itertools

from .api_clients.google_maps_client import GoogleMapsClient
from .api_clients.google_sheets_client import GoogleSheetsClient
from .scrapers.web_scraping import WebDataHunter
from .utils.shelf_functions import *

class SiteToSheetProcessor:
    def __init__(self, storage_directory: pathlib.Path, credentials_filepath: pathlib.Path):
        """
        Initializes a new instance of the SiteToSheetProcessor class.

        Args:
            storage_directory (pathlib.Path): The directory where data will be stored.
            credentials_filepath (pathlib.Path): The file path to the credentials file.

        Raises:
            AssertionError: If the GOOGLE_API_KEY environment variable is not set.
            AssertionError: If the SHEET_ID environment variable is not set.
        """
        self.storage_directory = storage_directory
        self.credentials_filepath = credentials_filepath
        self.gsheets_instance = None
        self.gmaps_instance = None
        self.google_maps_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_sheets_id = os.getenv('SHEET_ID')
        assert self.google_maps_api_key is not None, "Please set the GOOGLE_API_KEY environment variable"
        assert self.google_sheets_id is not None, "Please set the SHEET_ID environment variable"
        self.all_links = None
        self.links_to_search = None
        self.stored_links = None

    def initialize_clients(self, sheet_id = None , path_to_json_cred = None):
        if sheet_id is None:
            sheet_id = self.google_sheets_id
        if path_to_json_cred is None:
            path_to_json_cred = self.credentials_filepath
        self.gsheets_instance =\
            GoogleSheetsClient(sheet_id=sheet_id, path_to_json_cred=path_to_json_cred)
        self.gsheets_instance.retrieve_google_sheet()
        return None 

    def update_headers_and_destination_info(self, force_update: bool):
        if force_update:
            self.gsheets_instance.gs_headers = self.gsheets_instance.extract_headers()
            self.gsheets_instance.destination_info =\
                self.gsheets_instance.extract_destination_info()
        else:
            try:
                self.gsheets_instance.gs_headers =\
                    get_shelf_data(self.storage_directory, "auxilliary")['Headers']
                self.gsheets_instance.destination_info =\
                    get_shelf_data(self.storage_directory, "auxilliary")['Info']
            except KeyError:
                self.gsheets_instance.gs_headers = self.gsheets_instance.extract_headers()
                self.gsheets_instance.destination_info =\
                    self.gsheets_instance.extract_destination_info()
        update_auxilliary_shelf(self.storage_directory,{"Headers":self.gsheets_instance.gs_headers})
        update_auxilliary_shelf(self.storage_directory,{"Info":self.gsheets_instance.destination_info})
        return None

    def get_links(self):
        self.all_links = self.gsheets_instance.extract_links()
        self.links_to_search, self.stored_links = check_links_shelf(self.storage_directory, self.all_links)

    def process_links_update_sheet(self, enable_google_maps: bool, force_link_process: bool):
        if enable_google_maps and ((self.links_to_search is not None) or force_link_process):
            self.gmaps_instance = GoogleMapsClient(api_key=self.google_maps_api_key)
            headers = get_shelf_data(self.storage_directory, "auxilliary")['Headers']
            destination_info = get_shelf_data(self.storage_directory, "auxilliary")['Info']

            for i in self.links_to_search:
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

                #Rate limiting applied to obtain_all_link_info method
                web_info = web_instance.obtain_all_link_info(link, matches)

                start = web_info['Location']
                self.gmaps_instance.set_start(start)

                #compares with googlesheets to only search if tenant info in the headers
                print(f"Adding time to destination from {start} to {destination_matches}")
                for i in destination_matches:
                    destination = destination_info[i]
                    time_to_destination = self.gmaps_instance.time_to_destination(destination)
                    web_info[i] = time_to_destination

                self.gsheets_instance.update_links_info(web_info)  
                update_shelf(self.storage_directory, {link: web_info})


    def sync_sheets_with_local_data(self, sync_local_data: bool):
        if sync_local_data:
            #Limit of 50 sync sheets to prevent overloading google sheets
            set_limit = 50
            all_shelfed_data = get_shelf_data(self.storage_directory)
            for i in itertools.islice(self.stored_links, set_limit):
                if i in all_shelfed_data:
                    gs_update_info = all_shelfed_data[i]
                self.gsheets_instance.update_links_info(gs_update_info)
