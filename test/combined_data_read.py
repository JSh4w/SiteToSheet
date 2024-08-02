import pandas as pd
import numpy as np
import re
import json 
import googlemaps
from datetime import datetime
from datetime import timedelta

#set paths for rental_stats and rightmove/online data
rent_by_postcode_path= 'Right_move/londonrentalstatisticsq22023.xlsx'
rent_data_path="Right_move/sales_data.csv"

#still have to set number of bedrooms to match data for now
bedroom_no=3
if bedroom_no==0:
    bed_str='Studio'
elif bedroom_no==1:
    bed_str='One Bedroom'
elif bedroom_no==2:
    bed_str='Two Bedrooms'
elif bedroom_no==3:
    bed_str='Three Bedrooms'
elif bedroom_no==4:
    bed_str='Four or More Bedrooms'

#read data of files and extract postcodes
postcode_data = pd.read_excel(rent_by_postcode_path,sheet_name="Table 1.3", header=12,nrows=1974)
postcodes_list=np.unique(np.array(postcode_data['Postcode District']))
rent_data= pd.read_csv(rent_data_path)

#setting up google maps api and datetime offset
my_key='AIzaSyBrMB9s8ZahiX3g6H5iVVvgJxCRQ21Zijg'
gmaps = googlemaps.Client(key=my_key)
todayDate = datetime.today()
nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
nextMonday = nextMonday.replace(hour=9,minute=0,second=0,microsecond=0)

#sets limits and data sets for google_maps_iterations
x=0   
google_maps_max_it=5
final_loc = "Kings Langley"
transport_mode="transit"    #driving, walking, bicycling,transit , can also set transit_mode = rail,tram,train,subway,bus

#seteup list of classes for later
property_list=[]
class Property:
    def __init__(self, link, location, price, mean_price, distance,borough_score):
        self.link= link
        self.location= location
        self.price = price
        self.mean_price = mean_price
        self.distance = distance
        self.borough_score = borough_score
    def __str__(self):
        return f"Link: {self.link}, Location: {self.location}, Price: {self.price}, Mean price:{self.mean_price}, Distance: {self.distance}"


#making arrays
postcode_data_array=np.array(postcode_data)
rent_data_array=np.array(rent_data)


#iterate through rent_data and extract postcode (some are two parters hence postcode is split)
for i in rent_data_array:
    postcode_1=str(i[1]).split()[-1]
    postcode_2=str(i[1]).split()[-2]

    if len(postcode_1)>3:
        pass
    #this is for when postcode rather than 'london', there may be a better way
    if len(postcode_1)<=3:
        for row in postcode_data_array:
            #if three bed
            if row[2]==bed_str and type(row[4])==int and (row[1]==postcode_1 or row[1]==postcode_2) :

                #price=re.findall('[0-9]+',i[3].replace(",",""))
                if x<=google_maps_max_it:
                    start_loc=i[1]
                    dist= gmaps.distance_matrix(start_loc,final_loc,mode=transport_mode,arrival_time=nextMonday)
                    duration=dist["rows"][0]["elements"][0]["duration"]["text"] 
                    x+=1
                if x>google_maps_max_it:
                    duration=None
                price_int=int(''.join(filter(str.isdigit,i[3].replace(",",""))))
                property_list.append(Property(i[0],i[1],price_int,row[4],duration,None))


for Property in property_list:
    print(Property)


with open('Right_move/items.json', 'w') as file:
    json.dump([item.__dict__ for item in property_list], file)