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



link= "https://www.rightmove.co.uk/properties/146078252#/?channel=RES_LET"

#link = links[8]
rightmove=link
#headers = {
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
#}
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}

res = requests.get(rightmove, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")
description=soup.find('title').getText()
loc = soup.find(string=re.compile("for rent in"))
location=loc.replace("4 bedroom apartment for rent in","")
description=soup.find(string=re.compile('"text":{"description":'))
cost=[str(description)[i:i+5] for i in range(0,len(str(description))) if (str(description)[i+2:i+5].isdigit() and str(description)[i+1]=="," and str(description)[i].isdigit())]
for i in cost:
    for j in cost:
        if j==i and j!="0,000":
            cost=j
#print(cost)
#setting up google maps api and datetime offset
gmaps=True
if gmaps:
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

if gmaps:
    dist= gmaps.distance_matrix(location,final_loc,mode=transport_mode,arrival_time=nextMonday)
    duration_jonty=dist["rows"][0]["elements"][0]["duration"]["text"] 
    print(f"Jonty:{duration_jonty}")
    dist= gmaps.distance_matrix(location,"BPP University London Holborn",mode=transport_mode,arrival_time=nextMonday)
    duration_tom=dist["rows"][0]["elements"][0]["duration"]["text"] 
    print(f"Tom:{duration_tom}")
    dist= gmaps.distance_matrix(location,"1 New St Square, London EC4A 3HQ ",mode=transport_mode,arrival_time=nextMonday)
    duration_jovan=dist["rows"][0]["elements"][0]["duration"]["text"] 
    print(f"Jovan:{duration_jovan}")

