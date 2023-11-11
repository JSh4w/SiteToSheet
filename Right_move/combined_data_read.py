import pandas as pd
import numpy as np
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
            if row[2]=='Three Bedrooms' and type(row[4])==int and row[1]==y :
                i2+=1
                Property_score.append()
            if row[2]=='Three Bedrooms' and type(row[4])==int and row[1]==y2:
                i2+=1

print(i1,i2)



