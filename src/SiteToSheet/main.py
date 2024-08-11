"""
SiteToSheet Main Processor

This module serves as the main entry point for the SiteToSheet application.
It orchestrates the web scraping, natural language processing, and Google API integration
to extract data from websites and store it in Google Sheets.

Classes:
    SiteToSheetProcessor: The main processor class that coordinates the data extraction and storage.

Functions:
    None

Variables:
    None

Notes:
    This module relies on the following external dependencies:
        - Google Maps API
        - Google Sheets API
        - spaCy for natural language processing
        - BeautifulSoup for web scraping

    The application configuration is loaded from the `config` module.
"""
import os
import pathlib
import itertools

from .api_clients.google_maps_client import GoogleMapsClient
from .api_clients.google_sheets_client import GoogleSheetsClient
from .scrapers.web_scraping import WebDataHunter
from .utils.shelf_functions import (
    get_shelf_data,
    check_links_shelf,
    update_shelf,
    update_auxilliary_shelf
)

class SiteToSheetProcessor:
    """
    SiteToSheetProcessor class orchestrates the data extraction and storage process for the SiteToSheet application.

    Attributes:
        storage_directory (pathlib.Path): The directory where data will be stored.
        credentials_filepath (pathlib.Path): The file path to the credentials file.

    Methods:
        __init__(self, storage_directory: pathlib.Path, credentials_filepath: pathlib.Path): 
            Initializes a new instance of the SiteToSheetProcessor class.
            Raises:
                AssertionError: If the GOOGLE_API_KEY environment variable is not set.
    """
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
        self.all_links = None
        self.links_to_search = None
        self.stored_links = None
        assert self.google_maps_api_key is not None, "Set the GOOGLE_API_KEY env var"
        assert self.google_sheets_id is not None, "Please set the SHEET_ID environment variable"

    def initialize_clients(self, sheet_id = None , path_to_json_cred = None):
        """
        Initializes the GoogleSheetsClient and retrieves the Google Sheet.

        Args:
            sheet_id (str, optional): ID of the Google Sheets. Defaults to None.
            path_to_json_cred (str, optional): Path to the JSON credentials file. Defaults to None.

        Returns:
            None
        """
        if sheet_id is None:
            sheet_id = self.google_sheets_id
        if path_to_json_cred is None:
            path_to_json_cred = self.credentials_filepath
        self.gsheets_instance =\
            GoogleSheetsClient(sheet_id=sheet_id, path_to_json_cred=path_to_json_cred)
        self.gsheets_instance.retrieve_google_sheet()

    def update_headers_and_destination_info(self, force_update: bool):
        """
        Updates the headers and destination information of the Google Sheets instance.

        Args:
            force_update (bool): A flag indicating whether to 
                                force the update of headers and destination information.
                If True: 
                   The information is extracted from the Google Sheets instance.
                If False: 
                   The information is retrieved from the auxilliary shelf data.
                If the auxilliary shelf data is not available,
                The information is from the Google Sheets instance.

        Returns:
            None
        """
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
        update_auxilliary_shelf(
            self.storage_directory,
            {"Headers":self.gsheets_instance.gs_headers}
            )
        update_auxilliary_shelf(
            self.storage_directory,
            {"Info":self.gsheets_instance.destination_info}
            )

    def get_links(self):
        """
        Retrieves all links from the Google Sheets instance 
        and updates the links_to_search and stored_links attributes.
        
        Args:
            None
        
        Returns:
            None
        """
        self.all_links = self.gsheets_instance.extract_links()
        self.links_to_search, self.stored_links =\
            check_links_shelf(self.storage_directory, self.all_links)

    def process_links_update_sheet(self, enable_google_maps: bool, force_link_process: bool):
        """
        Updates Google Sheets with link information, including time to destination.

        Parameters:
            enable_google_maps (bool): Whether to use Google Maps API.
            force_link_process (bool): Whether to force link processing.

        Returns:
            None
        """
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
        """
        Synchronizes the data in Google Sheets with the local data.

        Args:
            sync_local_data (bool): A boolean indicating whether to sync the local data.

        Returns:
            None
        """
        if sync_local_data:
            #Limit of 50 sync sheets to prevent overloading google sheets
            set_limit = 50
            all_shelfed_data = get_shelf_data(self.storage_directory)
            for i in itertools.islice(self.stored_links, set_limit):
                if i in all_shelfed_data:
                    gs_update_info = all_shelfed_data[i]
                self.gsheets_instance.update_links_info(gs_update_info)
