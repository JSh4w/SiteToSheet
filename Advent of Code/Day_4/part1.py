import numpy as np
input=open("Advent of Code/Day_4/input.txt","r").read().splitlines()
total=0
for x, line in enumerate(input):
    game,numbers=line.split("|")
    game_numbers=game.split(":")[1].split(" ")
    hits=0

    for a in game_numbers:
        a.strip()
        if a=="":
            continue
        for b in numbers.split(" "):
            b.strip()
            if a==b:
                if hits==0:
                    hits+=1
                else:
                    hits=hits*2
    total+=hits
print(total)
    
