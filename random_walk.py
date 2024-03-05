import random
x=0
num_steps_list=[]
while x<1e7:
    x+=1
    co_ord=[0,0]
    num_steps=0
    while abs(co_ord[0])<20 and abs(co_ord[1])<20:
        step=random.choice([[0,10],[0,-10],[10,0],[-10,0]])
        co_ord[0]=co_ord[0]+int(step[0])
        co_ord[1]=co_ord[1]+int(step[1])
        num_steps+=1
    num_steps_list.append(num_steps)
print(sum(num_steps_list)/len(num_steps_list))