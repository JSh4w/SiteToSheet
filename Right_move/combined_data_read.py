import pandas as pd
import numpy as np
import re
import json 
rent_stats= 'Right_move/londonrentalstatisticsq22023.xlsx'
dat1 = pd.read_excel(rent_stats,sheet_name="Table 1.3", header=12,nrows=1974)
#print(dat1)
x=np.array(dat1['Postcode District'])
x=np.unique(x)


Property_score=[]

y=np.array(dat1["Bedroom Category"])

data_new=np.array(dat1)
data= pd.read_csv("Right_move/sales_data.csv")
data=np.array(data)

i1=0
i2=0


class Property:
    def __init__(self, link, location, price, mean_price, distance):
        self.link= link
        self.location= location
        self.price = price
        self.mean_price = mean_price
        self.distance = distance
    def __str__(self):
        return f"Link: {self.link}, Location: {self.location}, Price: {self.price}, Mean price:{self.mean_price}, Distance: {self.distance}"

property_list=[]
# data structure link, location , house , price
for i in data:
    x=str(i[1])
    y=x.split()[-1]
    y2=x.split()[-2]
    if len(y)>3:
        #print("location not name")
        pass
    if len(y)<=3:
        i1+=1
        for row in data_new:
            if row[2]=='Three Bedrooms' and type(row[4])==int and (row[1]==y or row[1]==y2) :
                i2+=1
                #price=re.findall('[0-9]+',i[3].replace(",",""))
                price_2=int(''.join(filter(str.isdigit,i[3].replace(",",""))))
                property_list.append(Property(i[0],i[1],price_2,row[4],None))
print(i1,i2)
for Property in property_list:
    print(Property)


with open('Right_move/items.json', 'w') as file:
    json.dump([item.__dict__ for item in property_list], file)