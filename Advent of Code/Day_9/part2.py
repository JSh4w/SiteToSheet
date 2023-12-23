import numpy as np
input=open("Advent of Code/Day_9/input.txt","r").read()

seq=input.split("\n")


def next_num(input):
    diffs=[input[0]]
    layer=0
    x="a"
    while x!=0:
        d=[input[i+1]-input[i] for i in range(len(input)-1)]
        layer+=1
        if all(a==0 for a in d):
            x=0
        else:
            diffs.append(d[0])
        input=d
    result=0
    sign=1
    for x in diffs:
        sign=-sign
        result+=-sign*x
    return(result)


answer=0
for x in seq:    
    answer+=(next_num(list(map(int,x.split(" ")))))
    #print(next_num(list(map(int,x.split(" ")))))
print(answer)



