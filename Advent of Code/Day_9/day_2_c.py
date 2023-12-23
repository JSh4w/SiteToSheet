def extrapolate(array):
    if all(x == 0 for x in array):
        return 0

    deltas = [y - x for x, y in zip(array, array[1:])]
    diff = extrapolate(deltas)
    return array[0] - diff

total = 0

for line in open("Advent of Code/Day_9/input.txt"):
    nums = list(map(int, line.split()))
    total += extrapolate(nums)

print(total)