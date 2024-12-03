import re
from dataclasses import dataclass


@dataclass
class MutItem:
    left: int
    right: int
    begin_index: int
    end_index: int

@dataclass
class StatusItem:
    enabled: bool
    begin_index: int
    end_index: int


with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

line = "".join([i.strip() for i in lines])

MUT_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")
DO_PATTERN = re.compile(r"do\(\)")
DONT_PATTERN = re.compile(r"don't\(\)")


total = 0

items = []

for match in MUT_PATTERN.finditer(line):
    mut_item = MutItem(
        left=int(match.group(1)),
        right=int(match.group(2)),
        begin_index=match.start(),
        end_index=match.end(),
    )
    items.append(mut_item)

for match in DO_PATTERN.finditer(line):
    status_item = StatusItem(
        enabled=True,
        begin_index=match.start(),
        end_index=match.end(),
    )
    items.append(status_item)

for match in DONT_PATTERN.finditer(line):
    status_item = StatusItem(
        enabled=False,
        begin_index=match.start(),
        end_index=match.end(),
    )
    items.append(status_item)

items.sort(key=lambda x: x.begin_index)

total = 0
mut_enabled = True
for item in items:
    if isinstance(item, MutItem):
        if mut_enabled:
            total += item.left * item.right
    elif isinstance(item, StatusItem):
        mut_enabled = item.enabled

print(total)
