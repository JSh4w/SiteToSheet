import pandas as pd
import re 
data= pd.read_csv("Right_move/sales_data.csv")
pattern = r"[A-Z]{1,2}\d[\dA-Z]? ?[\dA-Z]{0,3}"
[print(str(i).split()[-1]) for i in data['Address'] if re.search(pattern, str(i).split()[-1])]


    