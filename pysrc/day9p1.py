from enum import Enum

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

line = "".join(lines).strip()

class Entry(Enum):
    EMPTY_SPACE = 0
    FILE = 1

files = [int(c) for c in line]

state = Entry.FILE
arr = [None] * sum(files)
pos = 0
file_id = 0

def set_value(value, begin, end):
    for i in range(begin, end):
        arr[i] = value

for idx, length in enumerate(files):
    if state == Entry.FILE:
        set_value(file_id, pos, pos + length)
        pos += length
        state = Entry.EMPTY_SPACE
        file_id += 1
    else:
        pos += length
        state = Entry.FILE

print("len", len(arr))

# print(arr)

# do defrag
def find_first_empty_idx(last_value=None):
    begin = last_value if last_value is not None else 0
    for i in range(len(arr)):
        if arr[i] is None:
            return i
    return None

def find_last_occupied_idx(last_value=None):
    begin = last_value if last_value is not None else len(arr) - 1
    for i in range(begin, -1, -1):
        if arr[i] is not None:
            return i
    return None

def do_swap(a, b):
    arr[a], arr[b] = arr[b], arr[a]

last_first_empty_idx = None
last_last_occupied_idx = None

while True:
    first_empty_idx = find_first_empty_idx(last_first_empty_idx)
    last_occupied_idx = find_last_occupied_idx(last_last_occupied_idx)

    if first_empty_idx is None or last_occupied_idx is None:
        break

    if first_empty_idx > last_occupied_idx:
        break

    do_swap(first_empty_idx, last_occupied_idx)
    print("swap", first_empty_idx, last_last_occupied_idx)
    # print(arr)

    last_first_empty_idx = first_empty_idx
    last_last_occupied_idx = last_occupied_idx


def calc_hash():
    total = 0
    for idx, value in enumerate(arr):
        if value is not None:
            total += value * idx
    return total

print(calc_hash())

