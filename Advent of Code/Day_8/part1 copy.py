import numpy as np
import math
from tqdm import tqdm
input=open("Advent of Code/Day_8/test_input.txt","r").read()
instructions,node_data=input.split("\n\n")


dic={}

    #name=a.split("=")[0].strip()
for a in node_data.split("\n"):
    name=a.split("=")[0].strip()
    left=a.split("=")[1].split(",")[0][2:].strip()
    right=a.split("=")[1].split(",")[1][:-1].strip()
    dic[name]=(left,right)

cn="AAA"
sc=0
while cn != "ZZZ":
    sc+= 1
    cn=dic[cn][0 if instructions[0]=="L" else 1]
    instructions=instructions[1:]+instructions[0]
print(sc)
