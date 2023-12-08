import numpy as np
input=open("Advent of Code/Day_5/input.txt","r").read().split("\n\n")

seeds,maps=input[0],input[1:]
seeds=list(map(int,seeds.split(":")[1].split()))
for a in maps:
    range=[]
    for line in a.splitlines():
        if "map" not in line:
            range.append(list(map(int,line.split())))
    new=[]
    for a in seeds:
        for d,s,r in range:
            if s <= a < s+r:
                new.append(a-s+d)
                break
        else:
            new.append(a)
    seeds=new

print(min(seeds))