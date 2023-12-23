import itertools as iter
import numpy as np
input=open("Advent of Code/Day_12/input.txt","r").read().split("\n")

dicto={}
for a in input:
    dicto.update({a.split(" ")[0]:a.split(" ")[1]})
for a in dicto:
    #print(dicto.get(a),a)
    pass

example=["?##??##???.??.?#?", [3,4,1,2,2]]
length=len(example[0])
question_marks=example[0].count("?")
missing_hash=sum(example[1])-example[0].count("#")
missing_dots=question_marks-missing_hash
new_string=("#"*missing_hash)+("."*missing_dots)
x=iter.permutations(new_string,len(new_string))
new=list(i for i in example[0])
#print(new)
length_new=len(new)
s=0
for i in x:
    stri=i
    trial=[]
    for x in example[0]:
        if x=="?":
            trial.append(stri[0])
            stri=stri[1:]
        else:
            trial.append(x)
    


# sort an ordered list of highest to lowest:
#determine possible nunmber of positions for largest, then reduce problem 