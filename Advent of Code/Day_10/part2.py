import numpy as np
import os
input=open("Advent of Code/Day_10/input.txt","r").read()
#print(input.split("\n"))
a=[row for row in input.split("\n")]
  
#padding of a
x="."*(len(a[0])+2)
for s in range(0,len(a)):
    a[s]="."+a[s]+"."
a.insert(0,x)
a.insert(len(a)+1,x)
#print(a)

def start_point(a):
    for b,c in enumerate(a):
        for d,e in enumerate(c):
            if e=="S":
                return([b,d])
            
def next_point(c,p):
    if a[c[0]][c[1]]=="S":
        #top
        if a[c[0]-1][c[1]]=="|" or a[c[0]-1][c[1]]=="7" or a[c[0]-1][c[1]]=="F":
            return([c[0]-1,c[1]])
        #right
        elif a[c[0]][c[1]+1]=="-" or a[c[0]][c[1]+1]=="J" or a[c[0]][c[1]+1]=="7":
            return([c[0],c[1]+1])
        #bottom
        elif a[c[0]+1][c[1]]=="|" or a[c[0]+1][c[1]]=="L" or a[c[0]+1][c[1]]=="J":
            return([c[0]+1,c[1]])
        #left
        elif a[c[0]][c[1]-1]=="-" or a[c[0]][c[1]-1]=="L" or a[c[0]][c[1]-1]=="F":
            return([c[0],c[1]-1])
        #error 
        else:
            return("no near s")
    elif a[c[0]][c[1]]=="|":
        if c[0]<p[0]:
            return([c[0]-1,c[1]])
        elif c[0]>p[0]:
            return([c[0]+1,c[1]])
    
    elif a[c[0]][c[1]]=="-":
        if c[1]>p[1]:
            return([c[0],c[1]+1])
        elif c[1]<p[1]:
            return([c[0],c[1]-1])
    elif a[c[0]][c[1]]=="L":
        if c[0]>p[0]:
            return([c[0],c[1]+1])
        if c[1]<p[1]:
            return([c[0]-1,c[1]])
    elif a[c[0]][c[1]]=="J":
        if c[1]>p[1]:
            return([c[0]-1,c[1]])
        if c[0]>p[0]:
            return([c[0],c[1]-1])
    elif a[c[0]][c[1]]=="7":
        if c[1]>p[1]:
            return([c[0]+1,c[1]])
        if c[0]<p[0]:
            return([c[0],c[1]-1])
    elif a[c[0]][c[1]]=="F":
        if c[0]<p[0]:
            return([c[0],c[1]+1])
        if c[1]<p[1]:
            return([c[0]+1,c[1]])
    else:
        print("S is found")


nip=""
sp=start_point(a)
prev=sp
nep=[0,0]

s=0
s2="S"
new_a=[[char for char in string] for string in a]
while nip!="S":
    s+=1
    nip=str(a[nep[0]][nep[1]])
    nep=next_point(sp,prev)
    prev=sp
    sp=nep
    new_a[nep[0]][nep[1]]="S"

new_a_join=["".join(b) for b in new_a]
f= open("Advent of Code/Day_10/new_a.txt","w+")

for b in new_a_join:
    f.write(str(b)+"\n")
#print(new_a_join)

    
#print(a)