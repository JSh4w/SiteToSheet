import pandas as pd
import numpy as np
rent_stats= 'Right_move/londonrentalstatisticsq22023.xlsx'
dat1 = pd.read_excel(rent_stats,sheet_name="Table 1.3", header=12,nrows=1974)
#print(dat1)
x=np.array(dat1['Postcode District'])
x=np.unique(x)


y=np.array(dat1["Bedroom Category"])

data_new=np.array(dat1)
i=0
i_2=0


for row in data_new:
    if row[2]=='Three Bedrooms':
       i_2+=1        
    if row[2]=='Three Bedrooms' and type(row[4])==int  :
       print(row[1])
       i+=1
