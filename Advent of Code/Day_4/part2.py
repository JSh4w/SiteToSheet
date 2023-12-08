import numpy as np
input=open("Advent of Code/Day_4/input.txt","r").read().splitlines()
total=0

def num_of_wins(line):
    game,number=line.split("|")
    game_numbers=game.split(":")[1].split(" ")
    wins=0
    for a in game_numbers:
        if a.strip()=="":
            continue
        for b in number.split(" "):
            if a==b:
                wins+=1
    return wins

m={}
for x,y in enumerate(input):
    if x not in m:
        m[x]=1
    j=num_of_wins(y)

    for n in range(x+1,x+j+1):
        #iterating through, add number of x to these values. Then as go through it multiplies the values 
        m[n]=m.get(n,1)+m[x]

print(sum(m.values()))






     
