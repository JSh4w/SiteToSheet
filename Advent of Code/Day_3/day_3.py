import numpy as np
input=open("Advent of Code/Day_3/input.txt","r").read().splitlines()
col=0
row=0
matrix=[[],[]]
#for y in input:
#    for x in y:
#input=open("Advent of Code/Day_3/input.txt","r").read()
Matrix=np.array([[x for x in y] for y in input])
symbols=np.array(np.where((Matrix=="$") | (Matrix=="*")| (Matrix=="-")| (Matrix=="=")| (Matrix=="#")| (Matrix=="@")| (Matrix=="/")))
symbols=symbols.transpose()
numbers="0,1,2,3,4,5,6,7,8,9"
print(np.shape(Matrix))
def number_hunt(Matrix,a0,a1,):
    if str(Matrix[a0][a1]).isnumeric():
            number=f"{Matrix[a0][a1]}"
            if a1>0 and a1<140:
                if str(Matrix[a0][a1-1]).isnumeric():
                    number=f"{Matrix[a0][a1-1]}{Matrix[a0][a1]}"
                    if a1>1:
                        if str(Matrix[a0][a1-2]).isnumeric():
                            number=f"{Matrix[a0][a1-2]}{Matrix[a0][a1-1]}{Matrix[a0][a1]}"

                elif str(Matrix[a0][a1+1]).isnumeric():
                    number=f"{Matrix[a0][a1+1]}"

            if a1>1:
                if str(Matrix[a0][a1-2]).isnumeric():
                    number=f"{Matrix[a0][a1-2]}{Matrix[a0][a1-1]}"
                    if a1>2:
                        if str(Matrix[a0][a1-3]).isnumeric():
                            number=f"{Matrix[a0][a1-3]}{Matrix[a0][a1-2]}{Matrix[a0][a1-1]}"
    return number

def better_number_hunt(Matrix,a0,a1,):
    number=[]
    for a in Matrix[a0][max(a1-2,0):min(a1+2,140)]:
        if a.isdigit():
            number.append(a)
    num=""
    for i in number:
        num=num+str(i)

    #print(num)
    return int(num)


numbers=[]
for a in symbols:
    if a[1]>0: #left
        if str(Matrix[a[0]][a[1]-1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0],a[1]-1))
    if a[1]<140: #right
        if str(Matrix[a[0]][a[1]+1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0],a[1]+1))
    if a[0]>0: #up 
        if str(Matrix[a[0]-1][a[1]]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]-1,a[1]))
    if a[0]<140: #down 
        if str(Matrix[a[0]+1][a[1]]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]+1,a[1]))
    if a[1]>0 and a[0]>0 : #topleft
        if str(Matrix[a[0]-1][a[1]-1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]-1,a[1]-1))
    if a[1]<140 and a[0]>0 : #topright
        if str(Matrix[a[0]-1][a[1]+1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]-1,a[1]+1))
    if a[1]>0 and a[0]<140 : #bottomleft
        if str(Matrix[a[0]+1][a[1]-1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]+1,a[1]-1))
    if a[1]<140 and a[0]<140 : #bottomright
        if str(Matrix[a[0]+1][a[1]+1]).isnumeric():
            numbers.append(better_number_hunt(Matrix,a[0]+1,a[1]+1))
print(numbers)
print(np.sum(numbers))

    
##columns then rows 

#for y in Matrix:
#    for x in y:
#        if x=='$' or x=='*':

