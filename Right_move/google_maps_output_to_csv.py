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

from dotenv import load_dotenv
load_dotenv()

#Beautiful soup- https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)#:~:text=Beautiful%20Soup%20is%20a%20Python,is%20useful%20for%20web%20scraping.
# Parses HTML - taking code and extracting relevant information 
from bs4 import BeautifulSoup

#used for rests
import re

#for GOOGLE api 
import googlemaps

#for getting monday morning 9am
from datetime import datetime
from datetime import timedelta


class house_hunter:
    def __init__(self,KEY,person_destination,LINK):
        self.key=KEY
        self.journey_dict=person_destination
        self.link=open(LINK).readlines()


    #determines the web browser setup for Beautiful soup
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
    def single_read(self,gmaps_true):
        res = requests.get(self.link[0], headers=self.headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        loc = soup.find(string=re.compile("for rent in"))
        location=loc.replace("4 bedroom apartment for rent in","")
        cost=soup.find(string=re.compile("Rent Amount"))
        description=soup.find(string=re.compile('"text":{"description":'))
        description=description.split("<b")
        des=[]
        for a in description:
            if len(str(a))>30 and (not any(char.isdigit() for char in a)):
                des.append(a)
        print(cost,loc)  

        if gmaps_true:
            my_key= os.getenv('GOOGLE_API_KEY')
            gmaps = googlemaps.Client(key=my_key)
            todayDate = datetime.today()
            nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
            nextMonday = nextMonday.replace(hour=9,minute=0,second=0,microsecond=0)

        #sets limits and data sets for google_maps_iterations
        x=0   
        google_maps_max_it=5
        final_loc = "Kings Langley"
        transport_mode="transit" 

        if gmaps_true:
            dist= gmaps.distance_matrix(location,final_loc,mode=transport_mode,arrival_time=nextMonday)
            duration_jonty=dist["rows"][0]["elements"][0]["duration"]["text"] 
            print(f"Jonty:{duration_jonty}")
            dist= gmaps.distance_matrix(location,"1 New St Square, London EC4A 3HQ ",mode=transport_mode,arrival_time=nextMonday)
            duration_jovan=dist["rows"][0]["elements"][0]["duration"]["text"] 
            print(f"Jovan:{duration_jovan}")


    def journey_duration(self):
        for key in self.journey_dict:
            print(key,self.journey_dict[key])

    
csv_1= house_hunter(12,{'Jonty':'Kings Langley','Taka':'Westminster','Jovan':'Deloitte'},'./link.txt')
csv_1.single_read(True)
csv_1.journey_duration()



