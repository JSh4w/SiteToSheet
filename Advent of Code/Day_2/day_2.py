input=open("Advent of Code/Day_2/input.txt","r").readlines()
total_valid=0
part_2=0
for a in input:
    games =a.split(":")[1]
    game_ID=a.split(":")[0].split(" ")[1]
    Dict={'red':0,'green':0,'blue':0}
    for b in games.split(";"):
        for c in b.split(", "):
            value=int(c.strip().split(" ")[0])
            colour=str(c.strip().split(" ")[1])
            if value >Dict.get(colour):
                Dict.update({colour:value})
    part_2+=Dict.get("green")*Dict.get("blue")*Dict.get("red")
    if Dict.get("red") <= 12 and Dict.get("green") <= 13 and Dict.get("blue") <= 14:
        total_valid+=int(game_ID)     
print(total_valid, part_2)
        
