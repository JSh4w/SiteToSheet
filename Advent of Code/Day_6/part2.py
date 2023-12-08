import numpy as np
import math
input=open("Advent of Code/Day_6/input.txt","r").readlines()

time=float(str(input[0].split(":")[1].strip()).replace(" ",""))
distance=float(str(int(str(input[1].split(":")[1].strip()).replace(" ",""))+0.001))
print(time,distance)


min=math.ceil(((-time+np.sqrt(time**2-4*distance))/-2))
max=math.floor(((-time-np.sqrt(time**2-4*distance))/-2))
diff=max-min+1
print(diff)