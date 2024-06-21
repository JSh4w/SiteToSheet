############################
#
#The idea is to combine all python files together into a class
# We want to take CSV input , Link input and then output to command line and or CSV
#Functions: 
#Search through single link / list of links (set limit for API)
#Search through all listed properties in a certain borough and put all into excel
#Locate distances to wrok for selected locations 
#Locate nearest tube station and shops for selected location 
#Output info to CSV in specific column 
# 
###########################
#requests deals with extracting information from RightMove
import requests 

#all for API key
import os

#for using environment variables for GOOGLE API key 
from dotenv import load_dotenv
load_dotenv()

#duh
import csv

#Beautiful soup- https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)#:~:text=Beautiful%20Soup%20is%20a%20Python,is%20useful%20for%20web%20scraping.
# Parses HTML - taking code and extracting relevant information 
from bs4 import BeautifulSoup

#used for rests, regex
import re

#for GOOGLE api 
import googlemaps

#https://docs.google.com/spreadsheets/d/1QVGoFL_3m57_HcWLyxl83aMQKKWRBVSR44EmMXUQy4I/edit#gid=0

#for getting monday morning 9am
from datetime import datetime
from datetime import timedelta


#for sheet_hunter and filler:
import gspread
from google.oauth2.service_account import Credentials


#this is for storing all info so not multiple API calls
import shelve

class house_hunter:
    '''Takes txt input of links, csv input of current options and outputting to CSV or command-line'''
    def __init__(self,person_destination : dict ,LINK : str):
        '''Google API key, dictionary of people and destinations, path to text file with links'''
        self.output_dict={}
        self.journey_dict=person_destination
        self.link=open(LINK).readlines()
        self.time_dict={}
        #determines the web browser setup for Beautiful soup
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"
        }

    def get_google_sheet(self):
        """Gets google sheet document and returns as self.workbook"""
        scopes= [
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        creds  = Credentials.from_service_account_file("sheets_credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        sheet_id = os.getenv('SHEET_ID')
        self.workbook = client.open_by_key(sheet_id)
        return None 

    def sheet_hunter(self):
        """Returns a list containing: a dictionary of headers and their positions in the google sheets, a list of links taken from the document"""
        sheet=self.workbook.worksheet("Listings")

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

        #create a dictionary of links associated with data
        try:
            self.new_data={}
            with shelve.open('house_data', 'c', writeback=True) as shelf:
                retrieved_data = shelf.get("all_data", {})
                print("Data retrieved successfully:")
                for i in links_data_dict.keys():
                    if i not in retrieved_data.keys():
                        retrieved_data[i]=links_data_dict[i]
                        self.new_data[i]=links_data_dict[i]
                shelf["all_data"]=retrieved_data
                self.all_data=retrieved_data
                print(self.new_data)

            #still need to run search on all new entries 
        except IOError:
            print("Database error")
    
        return None
    
    def sheet_filler(self):
        sheet=self.workbook.worksheet("Listings")
        headings_dict=self.google_sheets_heading
        links=sheet.col_values(headings_dict["Link"])[1:]
        for i,j in enumerate(links):
            if i in self.new_data.keys:
                #need tuy update workbook row with corerct data in set format 
                pass 
        
       
        #need to worksheet.update_col 
        #or worksheet.update()
        #do this for all links base on position, maybe only do if new idk 

    def load_csv(self, csv_path: str):
        """loads_csv data currently present, if not present will create an excel sheet"""
        # Check if the file exists; if not, prepare to initialize it
        initialize_file = not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0
        if initialize_file:
            print("No file currently for path")

        template_data={"Link":'none', "Location":'none', "Price":'none', "Deposit":'none', "Local station": 'none', "Walking Distance":'none'}
        for i in self.journey_dict:
            template_data[i]=self.journey_dict[i]
        if initialize_file:
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file,fieldnames=template_data.keys())
                writer.writeheader()
                writer.writerow(template_data)
        else:
            data_list=[]
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_list.append(row)


    def single_read(self, gmaps_true,transport_mode):
        '''BOOL - using google maps, transport mode : transit, driving, walking, cycling '''
        res = requests.get(self.link[0], headers=self.headers)
        self.output_dict["Link"]=self.link[0]
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        just_text=soup.get_text()
        matches = [(match.group(), match.start()) for match in re.finditer(r'£\d{1,3},\d{3}', just_text)]
        Deposit = None
        Price = None
        location = [(match.group(), match.start()) for match in re.finditer("for rent in", just_text)]
        location_text=just_text[location[0][1]+11:location[0][1]+120].strip()
        for i in matches:
            index=i[1]
            min_range = index-30
            max_range = index+30
            search_text=just_text[min_range:max_range]
            if "Deposit" in search_text:
                Deposit=i[0]
            elif "Price" or "pcm" in search_text:
                Price=i[0]
        self.output_dict["Deposit"]=Deposit
        self.output_dict["Price"]=Price
        self.output_dict["Location"]=location_text
        #alternate method for extracting location 
        loc = soup.find(string=re.compile("for rent in"))
        if gmaps_true:
            my_key= os.getenv('GOOGLE_API_KEY')
            gmaps = googlemaps.Client(key=my_key)
            todayDate = datetime.today()
            nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
            nextMonday = nextMonday.replace(hour=9,minute=0,second=0,microsecond=0)
            geo_loc = gmaps.geocode(address=location_text)
            geo_loc_lat_long= geo_loc[0]['geometry']['location']
            nearest_station=gmaps.places_nearby(location=geo_loc_lat_long, radius=600,keyword="tube station")
            stations_list=nearest_station['results']
            stat_list=[]
            tube_list=open('tube_stops.txt').read().splitlines()
            for i in stations_list:
                if any(word in i['name'] for word in tube_list):
                    stat_list.append((i['name'],i['geometry']['location']))
            dist_stat= gmaps.distance_matrix(location_text,stat_list[0][1],mode="walking",arrival_time=nextMonday)
            #print(stat_list[0][0],dist_stat["rows"][0]["elements"][0]["duration"]["text"] )
            self.output_dict["Local Station"]=stat_list[0][0]
            for key in self.journey_dict:
                dist= gmaps.distance_matrix(location_text,self.journey_dict[key],mode=transport_mode,arrival_time=nextMonday)
                duration=dist["rows"][0]["elements"][0]["duration"]["text"] 
                self.time_dict[key]=duration
                self.output_dict["Work - "+key]=duration
        else:
            for key in self.journey_dict:
                self.time_dict[key]="Empty"

        with shelve.open('full_data', 'r') as shelf:
            retrieved_data = shelf[self.link[0]]
            print("Data retrieved successfully:")
            print(retrieved_data)

        
        return self.time_dict
        
    

    def journey_duration(self):
        '''Sanity check , returns journey dictionarys'''
        for key in self.journey_dict:
             print(key,self.journey_dict[key])

    def output(self):
        print(self.output_dict)


x=house_hunter({'Jonty':'Kings Langley','Taka':'Westminster','Jovan':'1 New St Square, London EC4A 3HQ '},'./link.txt')
x.get_google_sheet()
x.sheet_hunter()  