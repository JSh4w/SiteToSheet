import numpy as np
input=open("Advent of Code/Day_5/input.txt","r").read().split("\n\n")
from tqdm import tqdm
seeds,maps=input[0],input[1:]
seeds=list(map(int,seeds.split(":")[1].split()))
seed_2=[]

for i in range(0,len(seeds),2):
    seed_2.append((seeds[i], seeds[i]+seeds[i+1]))

for a in tqdm(maps):
    ranges=[]
    for line in a.splitlines():
        if "map" not in line:
            ranges.append(list(map(int,line.split())))
    new=[]
    for b in tqdm(seed_2):
        if type(b)==tuple:
            for x in range(b[0],b[1]):
                for d,s,r in ranges:
                    if s <= x < s+r:
                        new.append(x-s+d)
                        break
            else:
                new.append(x)
        elif type(b)==int:
            for d,s,r in ranges:
                if s <= x < s+r:
                    new.append(x-s+d)
                    break
            else:
                new.append(x)
    seed_2=new
print(min(seed_2))