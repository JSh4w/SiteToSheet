input=open("Advent of Code/Day_7/input.txt","r").read().split("\n")

nums=["1","2","3","4","5","6","7","8","9","T","J","Q","K","A"]

letter_map = {"T": "A", "J": ".", "Q": "C", "K": "D", "A": "E"}

def score(hand_1):
    t_r=0
    t1=[]
    for i in nums:
        t1.append(hand_1.count(str(i)))
    if t1.count(2)==0 and t1.count(3)==0 and t1.count(4)==0 and t1.count(5)==0:
        t_r=0
    elif t1.count(2) == 1 and t1.count(3)==0:
        t_r=1
    elif t1.count(2)==2:
        t_r=2
    elif t1.count(3)==1: 
        if t1.count(2)==1:
            t_r=4
        else:
            t_r=3
    elif t1.count(4)==1:
        t_r=5
    elif t1.count(5)==1:
        t_r=6
    else:
        pass
    return t_r

def replacements(hand):
    if hand == "":
        return [""]

    return [
        x + y
        for x in ("23456789TQKA" if hand[0] == "J" else hand[0])
        for y in replacements(hand[1:])
    ]


def classify(hand):
    return max(map(score, replacements(hand)))


def strength(hand):
    return (classify(hand), [letter_map.get(card, card) for card in hand])


plays = []

for line in input:
    hand, bid = line.split()
    plays.append((hand, int(bid)))

plays.sort(key=lambda play: strength(play[0]))
total = 0

for rank, (hand, bid) in enumerate(plays, 1):
    total += rank * bid

print(total)