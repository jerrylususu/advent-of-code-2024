from enum import Enum
from itertools import product
from functools import cache


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class KeypadType(Enum):
    NUMERIC = 0
    DIRECTIONAL = 1

def key_to_direction(key: str) -> Direction:
    if key == '^':
        return Direction.UP
    elif key == 'v':
        return Direction.DOWN
    elif key == '<':
        return Direction.LEFT
    elif key == '>':
        return Direction.RIGHT


class NumericKeypad():

    grid = [['7','8','9'], ['4','5','6'], ['1','2','3'], [None, '0', 'A']]
    cursor_pos = (3, 2)
    pressed = []

    def __init__(self) -> None:
        self.pressed = []

    def move_cursor(self, direction: Direction) -> bool:
        row_idx, col_idx = self.cursor_pos
        if direction == Direction.UP:
            row_idx -= 1
        elif direction == Direction.DOWN:
            row_idx += 1
        elif direction == Direction.LEFT:
            col_idx -= 1
        elif direction == Direction.RIGHT:
            col_idx += 1

        if 0 <= row_idx < len(self.grid) and 0 <= col_idx < len(self.grid[row_idx]) and self.grid[row_idx][col_idx] is not None:
            self.cursor_pos = (row_idx, col_idx)
            return True
        else:
            return False
        

    def press_cursor(self):
        row_idx, col_idx = self.cursor_pos
        self.pressed.append(self.grid[row_idx][col_idx])

    @classmethod
    def get_pos_from_key(cls, key: str) -> tuple[int, int]:
        for row_idx, row in enumerate(cls.grid):
            for col_idx, value in enumerate(row):
                if value == key:
                    return (row_idx, col_idx)
        return None

class DirectionalKeypad():
    grid = [[None, '^', 'A'], ['<', 'v', '>']]
    cursor_pos = (0, 2)
    pressed = []
    connected_keypad = None

    def __init__(self, connected_keypad) -> None:
        self.pressed = []
        self.connected_keypad = connected_keypad

    def move_cursor(self, direction: Direction) -> bool:
        row_idx, col_idx = self.cursor_pos
        if direction == Direction.UP:
            row_idx -= 1
        elif direction == Direction.DOWN:
            row_idx += 1
        elif direction == Direction.LEFT:
            col_idx -= 1
        elif direction == Direction.RIGHT:
            col_idx += 1

        if 0 <= row_idx < len(self.grid) and 0 <= col_idx < len(self.grid[row_idx]) and self.grid[row_idx][col_idx] is not None:
            self.cursor_pos = (row_idx, col_idx)
            return True
        else:
            print("invalid curosr pos", self.cursor_pos)
            return False
    
    def press_cursor(self):
        row_idx, col_idx = self.cursor_pos
        self.pressed.append(self.grid[row_idx][col_idx])

        if self.grid[row_idx][col_idx] == 'A':
            self.connected_keypad.press_cursor()
        else:
            self.connected_keypad.move_cursor(key_to_direction(self.grid[row_idx][col_idx]))

    def process_input(self, input: str):
        for key in input:
            if key == 'A':
                self.press_cursor()
            else:
                self.move_cursor(key_to_direction(key))


    @classmethod
    def get_pos_from_key(cls, key: str) -> tuple[int, int]:
        for row_idx, row in enumerate(cls.grid):
            for col_idx, value in enumerate(row):
                if value == key:
                    return (row_idx, col_idx)
        return None

numeric_keypad = NumericKeypad()
directional_keypad = DirectionalKeypad(numeric_keypad)


def get_four_next_positions(position: tuple[int, int]) -> list[tuple[int, int]]:
    row_idx, col_idx = position
    return [(row_idx - 1, col_idx), (row_idx + 1, col_idx), (row_idx, col_idx - 1), (row_idx, col_idx + 1)]

def is_invalid_position(keypad_type: KeypadType, position: tuple[int, int]) -> bool:
    if keypad_type == KeypadType.NUMERIC:
        valid_pos = [(row_idx, col_idx) for row_idx in range(4) for col_idx in range(3) if numeric_keypad.grid[row_idx][col_idx] is not None]
    elif keypad_type == KeypadType.DIRECTIONAL:
        valid_pos = [(row_idx, col_idx) for row_idx in range(2) for col_idx in range(3) if directional_keypad.grid[row_idx][col_idx] is not None]
    return position not in valid_pos


@cache
def bfs_get_paths_between_two_positions(start: tuple[int, int], end: tuple[int, int], keypad_type: KeypadType) -> list[list[tuple[int, int]]]:
    queue = [(start, [start])]
    all_paths = []
    min_len = None

    while queue:
        current_position, path = queue.pop(0)
        if current_position == end:

            if min_len is None:
                min_len = len(path)
            
            if len(path) < min_len:
                raise Exception("should not happen")
            elif len(path) == min_len:
                all_paths.append(path)
            else:
                # not shortest path rejected
                continue
        else:
            for next_position in get_four_next_positions(current_position):
                if not is_invalid_position(keypad_type, next_position) and next_position not in path:
                    queue.append((next_position, path + [next_position]))
    return all_paths


def map_move_to_key(move_begin: tuple[int, int], move_end: tuple[int, int]) -> str:
    if move_begin[0] == move_end[0]:
        if move_begin[1] < move_end[1]:
            return ">"
        else:
            return "<"
    else:
        if move_begin[0] < move_end[0]:
            return "v"
        else:
            return "^"
        
@cache
def count_key_continous_range_for_seq(seq: str) -> int:
    count = 0
    for i in range(len(seq) - 1):
        if seq[i] != seq[i + 1]:
            count += 1
    return count


numeric_keys = [str(i) for i in range(10)] + ['A']
directional_keys = ['^', 'v', '<', '>'] + ['A']

numeric_key_map = {}
directional_key_map = {}

def find_key_pos_in_numeric_keypad(key: str) -> tuple[int, int]:
    for row_idx, row in enumerate(numeric_keypad.grid):
        for col_idx, value in enumerate(row):
            if value == key:
                return (row_idx, col_idx)
    return None

def find_key_pos_in_directional_keypad(key: str) -> tuple[int, int]:
    for row_idx, row in enumerate(directional_keypad.grid):
        for col_idx, value in enumerate(row):
            if value == key:
                return (row_idx, col_idx)
    return None


def get_min_range_key_press_seqs_from_all_seqs(all_seqs: list[str]) -> list[str]:
    min_range = None
    min_range_seqs = []
    for seq in all_seqs:
        range_count = count_key_continous_range_for_seq(seq)
        if min_range is None:
            min_range = range_count
            min_range_seqs.append(seq)
        elif range_count == min_range:
            min_range_seqs.append(seq)
        elif range_count < min_range:
            min_range = range_count
            min_range_seqs = [seq]
    return list(min_range_seqs)


def path_to_keys(path) -> str:
    keys = []
    for i in range(len(path) - 1):
        move_begin = path[i]
        move_end = path[i + 1]
        key = map_move_to_key(move_begin, move_end)
        keys.append(key)
    return "".join(keys)

for key1 in numeric_keys:
    key1_pos = find_key_pos_in_numeric_keypad(key1)
    if key1 not in numeric_key_map:
        numeric_key_map[key1] = {}
    for key2 in numeric_keys:

        if key2 not in numeric_key_map[key1]:
            numeric_key_map[key1][key2] = {}


        key2_pos = find_key_pos_in_numeric_keypad(key2)
        paths = bfs_get_paths_between_two_positions(key1_pos, key2_pos, KeypadType.NUMERIC)
        keys = [path_to_keys(path) for path in paths]        

        pruned_keys = get_min_range_key_press_seqs_from_all_seqs(keys)

        numeric_key_map[key1][key2] = pruned_keys


for key1 in directional_keys:
    key1_pos = find_key_pos_in_directional_keypad(key1)
    if key1 not in directional_key_map:
        directional_key_map[key1] = {}
    for key2 in directional_keys:
        if key2 not in directional_key_map[key1]:
            directional_key_map[key1][key2] = {}

        key2_pos = find_key_pos_in_directional_keypad(key2)
        paths = bfs_get_paths_between_two_positions(key1_pos, key2_pos, KeypadType.DIRECTIONAL)
        keys = [path_to_keys(path) for path in paths]

        pruned_keys = get_min_range_key_press_seqs_from_all_seqs(keys)

        directional_key_map[key1][key2] = pruned_keys

# print(directional_key_map)


def build_seq_for_numeric_input(input: str) -> list[str]:
    seqs = []
    for key1, key2 in zip(input, input[1:]):
        seqs.append([i + 'A' for i in numeric_key_map[key1][key2]])
    producted_seqs = product(*seqs)
    return [''.join(seq) for seq in producted_seqs]

# print(build_seq_for_numeric_input("029A"))


# youtube: https://www.youtube.com/watch?v=dqzAaj589cM
@cache
def get_best_length_for_input_at_layer(input: str, depth: int) -> int:
    if depth == 0:
        return len(input)

    min_len_sum = 0
    for key1, key2 in zip("A" + input, input):
        min_len = float("inf")
        for seq in directional_key_map[key1][key2]:
            min_len = min(min_len, get_best_length_for_input_at_layer(seq + "A", depth - 1))
        min_len_sum += min_len

    return min_len_sum

raw_inputs = ["540A", "839A", "682A", "826A", "974A"]

sum_of_complexity = 0

for raw_input in raw_inputs:

    code_num = int(raw_input[:-1])

    min_len = float("inf")
    raw_input = "A" + raw_input
    initial_seqs = build_seq_for_numeric_input(raw_input)

    for seq in initial_seqs:
        print(seq)
        min_len = min(min_len, get_best_length_for_input_at_layer(seq, 25))

    print(min_len)

    complexity = code_num * min_len
    sum_of_complexity += complexity

print(sum_of_complexity)

