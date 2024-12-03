import re

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

PATTERN = re.compile(r"mul\((\d+),(\d+)\)")

total = 0

for line in lines:
    matches = PATTERN.findall(line)

    for match in matches:
        a, b = match
        a, b = int(a), int(b)
        total += a * b

print(total)


