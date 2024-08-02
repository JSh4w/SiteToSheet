import gspread
from google.oauth2.service_account import Credentials


def sheet_hunter():
    """Returns a list containing: a dictionary of headers and their positions in the google sheets, a list of links taken from the document"""
    scopes= [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds  = Credentials.from_service_account_file("sheets_credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id= "1QVGoFL_3m57_HcWLyxl83aMQKKWRBVSR44EmMXUQy4I"
    workbook = client.open_by_key(sheet_id)

    sheet= workbook.worksheet("Listings")

    headings=sheet.row_values(1)
    headings_dict={}
    for i,j in enumerate(headings):
        headings_dict[str(j)]=i+1
    links=sheet.col_values(headings_dict["Link"])[1:]

    return [headings_dict,links]

def sheet_filler():
    """Fills in the same google sheets document with all found info"""
