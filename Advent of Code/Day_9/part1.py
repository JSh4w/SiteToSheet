import numpy as np
input=open("Advent of Code/Day_9/input.txt","r").read()

seq=input.split("\n")


def next_num(input):
    #i is a list of values
    diffs=[input[-1]]
    layer=0
    x="a"
    while x!=0:
        d=[input[i+1]-input[i] for i in range(len(input)-1)]
        layer+=1
        if all(a==0 for a in d):
            x=0
        else:
            diffs.append(d[-1])
        input=d
    result=sum(diffs)
    return(result)


answer=0
for x in seq:    
    answer+=(next_num(list(map(int,x.split(" ")))))
    #print(next_num(list(map(int,x.split(" ")))))
print(answer)



