import numpy as np
input=open("Advent of Code/Day_5/input.txt","r").read().split("\n\n")
seeds,maps=input[0],input[1:]
seeds=list(map(int,seeds.split(":")[1].split()))
seed_2=[]

for i in range(0,len(seeds),2):
    seed_2.append((seeds[i], seeds[i]+seeds[i+1]))
for a in maps:
    ranges=[]
    for line in a.splitlines():
        if "map" not in line:
            ranges.append(list(map(int,line.split())))
    new=[]
    while len(seed_2)>0:
        s,e=seed_2.pop()
        for a,b,c in ranges:
            os=max(s,b)
            oe=min(e,b+c)
            if os<oe:
                new.append((os-b+a,oe-b+a))
                if os>s:
                    seed_2.append((s,os))
                if e>oe:
                    seed_2.append((oe,e))
                break
        else:
            new.append((s,e))
    seed_2=new
print(min(seed_2)[0])