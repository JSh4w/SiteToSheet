import pandas as pd

data= pd.read_csv("Right_move/sales_data.csv")
for i in data['Address']:
    x=str(i)
    y=x.split()[-1]
    if len(y)>3:
        print("location not name")
    else:
        print(y)

    