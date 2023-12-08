input = open("Advent of Code/Day_3/input.txt","r").read().splitlines()
number_set=set()

for a,row in enumerate(input):
    #a is row index
    for b, ch in enumerate(row):
        #b is column index
        if ch.isdigit() or ch ==".":
            continue
        for current_row in [a-1,a,a+1]:
            for current_column in [b-1,b,b+1]:
                if current_row<0 or current_row>= len(input) or current_column<0 or current_column>= len(input) or not input[current_row][current_column].isdigit():
                    continue 
                while current_column>0 and input[current_row][current_column-1].isdigit():
                    current_column -=1
                number_set.add((current_row,current_column))

ns=[]
for r, c in number_set:
    s=""
    while c< len(input[r]) and input[r][c].isdigit():
        s += input[r][c]
        c +=1
    ns.append(int(s))

answer=sum(ns)
print(answer)