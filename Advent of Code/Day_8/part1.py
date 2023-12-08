import numpy as np
import math
from tqdm import tqdm
input=open("Advent of Code/Day_8/input.txt","r").read()
instructions,node_data=input.split("\n\n")
class daynames:
    def __init__(self, name,left,right):
        self.name = name
        self.left = left
        self.right=right
node_tree=[]

    #name=a.split("=")[0].strip()
for a in node_data.split("\n"):
    name=a.split("=")[0].strip()
    left=a.split("=")[1].split(",")[0][2:].strip()
    right=a.split("=")[1].split(",")[1][:-1].strip()
    x=daynames(name,left,right)
    node_tree.append(x)
for a in node_tree:
    if a.name=="AAA":
        current_node=a
step_count=0
ns=0
while current_node.name!="ZZZ":
    for b in instructions:
        ns+=1
        if b=='R':
            next_node=current_node.right
        if b=='L':
            next_node=current_node.left
        for n in node_tree:
            if next_node==n.name:
                current_node=n
print(ns)
