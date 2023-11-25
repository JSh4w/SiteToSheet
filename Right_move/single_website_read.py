#requests deals with extracting information from RightMove
import requests 

#Beautiful soup- https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)#:~:text=Beautiful%20Soup%20is%20a%20Python,is%20useful%20for%20web%20scraping.
# Parses HTML - taking code and extracting relevant information 
from bs4 import BeautifulSoup

#used for rests
import re

#for converting to csv
import pandas as pd
import numpy as np
import re
import googlemaps
from datetime import datetime
from datetime import timedelta

link = "https://www.rightmove.co.uk/properties/140546135#/?channel=RES_LET"
rightmove=link
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

res = requests.get(rightmove, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")
loc = soup.find(string=re.compile("for rent in"))
location=loc.replace("3 bedroom apartment for rent in","")


#setting up google maps api and datetime offset
gmaps=False
if gmaps:
    my_key='AIzaSyBrMB9s8ZahiX3g6H5iVVvgJxCRQ21Zijg'
    gmaps = googlemaps.Client(key=my_key)
todayDate = datetime.today()
nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
nextMonday = nextMonday.replace(hour=9,minute=0,second=0,microsecond=0)

#sets limits and data sets for google_maps_iterations
x=0   
google_maps_max_it=5
final_loc = "Kings Langley"
transport_mode="transit" 

if gmaps:
    dist= gmaps.distance_matrix(location,final_loc,mode=transport_mode,arrival_time=nextMonday)
    duration=dist["rows"][0]["elements"][0]["duration"]["text"] 
    print(duration)


headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    # Add more headers as needed
}


"""
search_loc=location.split()[:4]
search_loc= " ".join(search_loc)
search_loc=search_loc.replace(" ","+")
search_loc=search_loc.replace(",","")
print(search_loc)
location_search=(f"https://streets.homeviews.com/search/?location={search_loc}")
resource = requests.get(location_search, headers=headers)
resource.raise_for_status()
soup = BeautifulSoup(resource.text, "html.parser")
print(soup)"""
#loc = soup.find(string=re.compile("for rent in"))
#location=loc.replace("3 bedroom apartment for rent in","")