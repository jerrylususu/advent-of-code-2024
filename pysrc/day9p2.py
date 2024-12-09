from enum import Enum
from bisect import bisect_left
from dataclasses import dataclass

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
max_file_id = 0

@dataclass(frozen=True)
class FileInfo:
    file_id: int
    begin: int
    end: int
    length: int

file_id_to_file_info_map = {}

def set_value(value, begin, end):
    for i in range(begin, end):
        arr[i] = value

empty_spaces = []

@dataclass(frozen=True)
class EmptySpace:
    length: int
    begin: int

    def __lt__(self, other):
        return self.length < other.length or (self.length == other.length and self.begin < other.begin)

for idx, length in enumerate(files):
    if state == Entry.FILE:
        set_value(file_id, pos, pos + length)
        file_id_to_file_info_map[file_id] = FileInfo(file_id, pos, pos + length, length)
        max_file_id = max(max_file_id, file_id)
        pos += length
        state = Entry.EMPTY_SPACE
        file_id += 1
    else:
        empty_spaces.append(EmptySpace(length, pos))
        pos += length
        state = Entry.FILE

print("len", len(arr))

def save_to_file(arr, filename):
    with open(filename, "w", encoding="u8") as f:
        for i in range(len(arr)):
            f.write(f"{i:06d}: {arr[i]}\n")

# print(arr)
save_to_file(arr, "before.txt")

empty_spaces.sort()
# print(empty_spaces)
# print(file_id_to_file_info_map)

def do_range_swap(src_begin, target_begin, len):
    tmp = []
    for i in range(len):
        tmp.append(arr[target_begin + i])
    for i in range(len):
        arr[target_begin + i] = arr[src_begin + i]
    for i in range(len):
        arr[src_begin + i] = tmp[i]


def find_first_empty_space_having_enough_length(length):
    begin = 0
    current_empty_len = 0
    for i in range(len(arr)):
        if arr[i] is not None:
            begin = i + 1
            current_empty_len = 0
            continue

        current_empty_len += 1
        if current_empty_len >= length:
            return begin
    return None



    # for empty_space in empty_spaces:
    #     if empty_space.length >= length:
    #         return empty_space
    # return None

    # pos = bisect_left(empty_spaces, EmptySpace(length, 0))
    # if pos < len(empty_spaces):
    #     return pos, empty_spaces[pos]
    # return None, None

# do defrag
# for i in range(max_file_id, -1, -1):
#     file_info = file_id_to_file_info_map[i]
#     empty_pos, empty_space = find_first_empty_space_having_enough_length(file_info.length)
#     if empty_space is not None:
#         do_range_swap(file_info.begin, empty_space.begin, file_info.length)
#         empty_spaces.pop(empty_pos)
#         remaining_empty_space_length = empty_space.length - file_info.length
#         if remaining_empty_space_length > 0:
#             new_empty_begin = empty_space.begin + file_info.length
#             empty_spaces.append(EmptySpace(remaining_empty_space_length, new_empty_begin))
#             empty_spaces.sort()


for i in range(max_file_id, -1, -1):
    file_info = file_id_to_file_info_map[i]
    empty_space_begin = find_first_empty_space_having_enough_length(file_info.length)
    if empty_space_begin is not None and empty_space_begin < file_info.begin:
        do_range_swap(file_info.begin, empty_space_begin, file_info.length)

    # print(arr)
    print("working on file", i)


save_to_file(arr, "after.txt")


def calc_hash():
    total = 0
    for idx, value in enumerate(arr):
        if value is not None:
            total += value * idx
    return total

print(calc_hash())

