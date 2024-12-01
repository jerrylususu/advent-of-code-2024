with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

lefts = []
rights = []

for line in lines:
    left, right = line.split()
    lefts.append(int(left))
    rights.append(int(right))


lefts.sort()
rights.sort()

total = 0

for l, r in zip(lefts, rights):
    total += abs(r - l)

print(total)
