import numpy as np
input=open("Advent of Code/Day_4/input.txt","r").read().splitlines()

mapping={}
#dictionary of games and total numbers

for i,x in enumerate(input):
    if i not in mapping:
        mapping[i]=1

    x=x.split(":")[1].strip()

    a,b=[list(map(int,k.split())) for k in x.split("|")]

    j = sum(f in a for f in b)

    #going through from card 1 to card 1 plus total wins
    for n in range(i+1,i+j+1):
            mapping[n]=mapping.get(n,1) + mapping[i]
    # i = 1, j=4 hence n is 2,3,4,5
    #then mapping[2]=2
    #then mapping[3]=2 
    #mapping[3]=2
    #mapping [5]=2
    # then mapping[2]
    #i=2 j=3 
    #mapping[3]= 2+2 
    # mapping of n where is a vlaue 

print(sum(mapping.values()))       