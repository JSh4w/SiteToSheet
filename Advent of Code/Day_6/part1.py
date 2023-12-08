import numpy as np
import math
input=open("Advent of Code/Day_6/input.txt","r").readlines()

times=list(map(int,input[0].split(":")[1].split()))
distances=list(map(int,input[1].split(":")[1].split()))

ranges=[]
answer=1
for a,i in enumerate(times):
    win_by=0.001
    distances[a]=distances[a]+win_by
    min=math.ceil(((-i+np.sqrt(i**2-4*distances[a]))/-2))
    max=math.floor(((-i-np.sqrt(i**2-4*distances[a]))/-2))
    diff=max-min+1
    answer=answer*diff
    ranges.append((min,max))
print(answer)
#here c=-distance 
#a=-1
#b=time

#x=-b+-sqrt(b^2-4ac)/2a
    #formula is x*i-x^2 =9 

