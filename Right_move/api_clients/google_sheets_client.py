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
        return None 
    
    def get_google_sheet(self):
        """Gets google sheet document and returns as self.workbook"""
        client = gspread.authorize(self.creds)
        workbook = client.open_by_key(self.sheet_id)

        return workbook

    def get_workbook_info(self, workbook) -> dict:
        """
        Retrieves the headers and links data from the provided workbook.

        Parameters:
            self: The object instance.
            workbook: The Google Sheets workbook to extract data from.

        Returns:
            dict: A dictionary containing the headers and links data.
        """
        sheet=workbook.worksheet("Listings")

        headings=sheet.row_values(1)
        headings_dict={}
        for i,j in enumerate(headings):
            headings_dict[str(j)]=i+1
        
        #google sheets headings
        self.google_sheets_heading=headings_dict
        #all values under links
        links=sheet.col_values(headings_dict["Link"])[1:]

        #create a dictionary of links associated with data
        links_data_dict={}
        for i,j in enumerate(links):
            data=sheet.row_values(i+2)
            links_data_dict[data[0]]=data[1:]
        #list of links
        self.google_links=links 

        return [headings_dict,links,links_data_dict]

