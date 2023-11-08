import googlemaps
from datetime import datetime
from datetime import timedelta

i=0
my_key='AIzaSyBrMB9s8ZahiX3g6H5iVVvgJxCRQ21Zijg'
gmaps = googlemaps.Client(key=my_key)
todayDate = datetime.today()
nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
nextMonday = nextMonday.replace(hour=9,minute=0,second=0,microsecond=0)
print(nextMonday)

start_loc = "1 lamb's passage London"
final_loc = "Waterloo Station London"
transport_mode="bicycling"    #driving, walking, bicycling,transit , can also set transit_mode = rail,tram,train,subway,bus
if i==0:
    dist= gmaps.distance_matrix(start_loc,final_loc,mode=transport_mode,arrival_time=nextMonday)
    duration=dist["rows"][0]["elements"][0]["duration"]["text"] 
    i+=1
i=1
#print(f'all data= {dist}')
print(f'duration = {duration}')