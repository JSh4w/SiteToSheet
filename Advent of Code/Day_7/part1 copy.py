import numpy as np
import math
input=open("Advent of Code/Day_7/input.txt","r").read().split("\n")
new_input=[]
for a in input:
    new_input.append(a)
numbers=["1","2","3","4","5","6","7","8","9","T","J","Q","K"]

def type_order(hand_1):
    t_r=0
    t1=[]
    for i in numbers:
        t1.append(hand_1.count(i))
    if t1.count(2)==0 and t1.count(3)==0 and t1.count(4)==0:
        #print("ha ha trash_hand")
        t_r=0
    elif t1.count(2) == 1 and t1.count(3)==0:
        t_r=1
    elif t1.count(2)==2:
        t_r=2
    elif t1.count(3)==1 and t1.count(2)==0:
        t_r=3
    elif t1.count(2)==1 and t1.count(3)==1:
        t_r=4
    elif t1.count(4)==1:
        t_r=5
    elif t1.count(5)==1:
        t_r=6
    else:
        #print("no type")
        pass
    return t_r

def higher(h1,h2):
    for b in range(0,4):
        val_1=0
        val_2=0
        if not h1[b].isdigit():
            if h1[b]=="T":
                val_1=10
            if h1[b]=="J":
                val_1=11
            if h1[b]=="Q":
                val_1==12
            if h1[b]=="K":
                val_1==13
            if h1[b]=="A":
                val_1==14
        else: 
            val_1=int(h1[b])
        if not h2[b].isdigit():
            if h2[b]=="T":
                val_2=10
            if h2[b]=="J":
                val_2=11
            if h2[b]=="Q":
                val_2==12
            if h2[b]=="K":
                val_2==13
            if h2[b]=="A":
                val_2==14
        else:
            val_2=int(h2[b])
        #print(val_1,val_2)
        if val_1==val_2:
            continue
        elif val_1>val_2:
            return 1
        elif val_1<val_2:
            return 0
        

#for x in range(0,len(new_input)-1):

#for a in range(0,len(new_input)-1):
#    score_1=type_order(new_input[a].split()[0])
#    score_2=type_order(new_input[a+1].split()[0])
#    temp_1=new_input[a]
#    temp_2=new_input[a+1]
#    print(score_1,temp_1)


for a in    
    
print(new_input)
#x=True 
#print(len(new_input))
#switches=1
#for x in range(0,len(new_input)-1):
#    new=new_input
#    switches=0
#    for a in range(0,len(new_input)-1):
#        hand_1=new_input[a].split()[0]
#        hand_2=new_input[a+1].split()[0]
#        print(hand_1)
#        if type_order(hand_2)>type_order(hand_1):
#            new[a]=new_input[a+1]
#            new[a+1]=new_input[a]
#        else:
#            new[a]=new_input[a]
#            new[a+1]=new_input[a+1]
#    new_input=new

