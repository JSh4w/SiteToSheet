#for sheet_hunter and filler:
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsClient:
    def __init__(self, sheet_id, path_to_json_cred):
        """
        Initializes the GoogleSheetsClient with the provided sheet_id and path_to_json_cred.

        Parameters:
            sheet_id: str - The ID of the Google Sheets.
            path_to_json_cred: str - The path to the JSON credentials file.

        Returns:
            None
        """
        self.sheet_id = sheet_id 
        self.sheet_idscopes= [
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        self.creds  = Credentials.from_service_account_file(path_to_json_cred, scopes=self.sheet_idscopes)


        self._gs_headers = None
        self._tenant_info = None
        self.gs_headers = None 
        self.tenant_info = None 
        return None 
    
    def retrieve_google_sheet(self):
        """Gets google sheet document and returns as self.workbook"""
        client = gspread.authorize(self.creds)
        workbook = client.open_by_key(self.sheet_id)
        self.listing_sheet= workbook.worksheet("Listings")

        return workbook
    @property
    def gs_headers(self):
        return self._gs_headers
    
    @gs_headers.setter
    def gs_headers(self, gs_headers):
        self._gs_headers=gs_headers 
    
    @property
    def tenant_info(self):
        return self._tenant_info
    
    @tenant_info.setter
    def tenant_info(self, tenant_info):
        self._tenant_info=tenant_info
    
    def extract_headers(self) -> dict:
        """
        Retrieves the headers from the provided workbook.

        Parameters:
            self: The object instance.
            workbook: The Google Sheets workbook to extract data from.

        Returns:
            dict: A dictionary containing the headers data.
        """
        sheet=self.listing_sheet
        headings=sheet.row_values(1)
        headings_dict={}
        for i,j in enumerate(headings):
            headings_dict[str(j)]=i+1
        self.gs_headers=headings_dict
        return headings_dict

    def extract_tenant_info(self, workbook = None) -> dict:
        """
    
        """
        if workbook is None:
            client = gspread.authorize(self.creds)
            workbook = client.open_by_key(self.sheet_id)
        sheet=workbook.worksheet("Info")
        names = sheet.col_values(1)[1:]
        location = sheet.col_values(2)[1:]
        address = sheet.col_values(3)[1:]
        tenant_info = {}
        for i in names:
            tenant_info[i] = [location[names.index(i)], address[names.index(i)]]
        self.tenant_info = tenant_info

        return self.tenant_info
    
    def extract_links(self) -> dict:
        """
        Retrieves the headers and links data from the provided workbook.

        Parameters:
            self: The object instance.
            workbook: The Google Sheets workbook to extract data from.

        Returns:
            dict: A dictionary containing the headers and links data.
        """
        sheet= self.listing_sheet
        #all values under links
        links=sheet.col_values(self.gs_headers["Link"])[1:]
        return links

    def get_listings_info(self) -> dict:
        """
        Retrieves the headers and links data from the provided workbook.

        Parameters:
            self: The object instance.
            workbook: The Google Sheets workbook to extract data from.

        Returns:
            dict: A dictionary containing the headers and links data.
        """
        sheet= self.listing_sheet
        #all values under links
        links=sheet.col_values(self.gs_headers["Link"])[1:]

        #create a dictionary of links associated with data
        links_data_dict={}
        for i,j in enumerate(links):
            data=sheet.row_values(i+2)[0:len(self.gs_headers)]
            link_dictionary={}
            for x in data:
                link_dictionary[self.gs_headers[data.index(x)]] = x
            links_data_dict[data[0]]=link_dictionary
        #list of links
        self.google_links=links 

        return [links,links_data_dict]

    def update_listing_info(self, web_info) -> None:
        """
        Updates the listing info in the provided workbook.

        Parameters:
            self: The object instance.
            workbook: The Google Sheets workbook to update.

        Returns:
            None
        """
        sheet=self.listing_sheet
        links= sheet.col_values(self.gs_headers["Link"])[1:]
        if web_info["Link"] in links:
            index = links.index(web_info["Link"])
            for i in web_info:
                sheet.update_cell(index+2, self.gs_headers[i], web_info[i])



