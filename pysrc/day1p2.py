from collections import Counter

with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

lefts = []
rights = []

for line in lines:
    left, right = line.split()
    lefts.append(int(left))
    rights.append(int(right))

cnt = dict(Counter(rights))

total = 0
for l in lefts:
    if l in cnt:
        total += l * cnt[l]

print(total)
