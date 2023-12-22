from enum import Enum
from itertools import product


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
directional_keypad_2 = DirectionalKeypad(directional_keypad)

# sequence = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
# directional_keypad_2.process_input(sequence)

# print("".join(numeric_keypad.pressed))
# print("".join(directional_keypad.pressed))
# print("".join(directional_keypad_2.pressed))



# ---------


def get_four_next_positions(position: tuple[int, int]) -> list[tuple[int, int]]:
    row_idx, col_idx = position
    return [(row_idx - 1, col_idx), (row_idx + 1, col_idx), (row_idx, col_idx - 1), (row_idx, col_idx + 1)]

def is_invalid_position(keypad_type: KeypadType, position: tuple[int, int]) -> bool:
    if keypad_type == KeypadType.NUMERIC:
        valid_pos = [(row_idx, col_idx) for row_idx in range(4) for col_idx in range(3) if numeric_keypad.grid[row_idx][col_idx] is not None]
    elif keypad_type == KeypadType.DIRECTIONAL:
        valid_pos = [(row_idx, col_idx) for row_idx in range(2) for col_idx in range(3) if directional_keypad.grid[row_idx][col_idx] is not None]
    return position not in valid_pos

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


def calc_product_of_all_paths(steps_and_keys) -> list[str]:
    steps = []
    key_strs = []
    for step_and_keys in steps_and_keys:
        step_start, step_end, paths_keys = step_and_keys
        steps.append((step_start, step_end))
        step_key_strs = []
        for keys in paths_keys:
            step_key_strs.append("".join(keys + ['A']))
        key_strs.append(step_key_strs)
    
    
    products = product(*key_strs)
    final_key_presses = []
    for product_result in products:
        final_key_presses.append("".join(product_result))
    
    return final_key_presses
    


def reverse_seq_for_keypad(input: str, keypad_type: KeypadType) -> list[str]:
    input = "A" + input  # add initial position

    steps = []
    for i in range(len(input) - 1):
        steps.append((input[i], input[i + 1]))
    
    steps_and_paths = []

    for step in steps:
        step_start, step_end = step

        if keypad_type == KeypadType.NUMERIC:
            path = bfs_get_paths_between_two_positions(NumericKeypad.get_pos_from_key(step_start), NumericKeypad.get_pos_from_key(step_end), KeypadType.NUMERIC)
        elif keypad_type == KeypadType.DIRECTIONAL:
            path = bfs_get_paths_between_two_positions(DirectionalKeypad.get_pos_from_key(step_start), DirectionalKeypad.get_pos_from_key(step_end), KeypadType.DIRECTIONAL)
        # print(step_start, step_end, path)
        steps_and_paths.append((step_start, step_end, path))

    steps_and_keys = []

    for step_and_paths in steps_and_paths:
        step_start, step_end, paths = step_and_paths
        paths_key = []
        for path in paths:
            keys = []
            for i in range(len(path) - 1):
                move_begin = path[i]
                move_end = path[i + 1]
                key = map_move_to_key(move_begin, move_end)
                keys.append(key)
            paths_key.append(keys)
        steps_and_keys.append((step_start, step_end, paths_key))

    final_key_presses = calc_product_of_all_paths(steps_and_keys)
    return final_key_presses



# print(len(reverse_seq_for_keypad("029A", KeypadType.NUMERIC)))

# print(len(reverse_seq_for_keypad("<A^A^^>AvvvA", KeypadType.DIRECTIONAL)))

# print(len(reverse_seq_for_keypad("v<<A>^>A<A>A<AAv>A^Av<AAA^>A", KeypadType.DIRECTIONAL)))


def get_min_len_key_press_seqs_from_all_seqs(all_seqs: list[str]) -> list[str]:
    min_len = None
    min_len_seqs = []
    for seq in all_seqs:
        if min_len is None:
            min_len = len(seq)
            min_len_seqs.append(seq)
        elif len(seq) < min_len:
            min_len = len(seq)
            min_len_seqs = [seq]
    return min_len_seqs


with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

codes = [line.strip() for line in lines]

sum_of_complexity = 0

for code in codes:

    code_num = int(code[:-1])

    shortest_seq_len = None
    layer_1_seq = reverse_seq_for_keypad(code, KeypadType.NUMERIC)
    layer_2_seq = []
    for seq in layer_1_seq:
        layer_2_seq.extend(reverse_seq_for_keypad(seq, KeypadType.DIRECTIONAL))
    layer_3_seq = []
    for seq in layer_2_seq:
        layer_3_seq.extend(reverse_seq_for_keypad(seq, KeypadType.DIRECTIONAL))
    

    for seq in layer_3_seq:
        if shortest_seq_len is None:
            shortest_seq_len = len(seq)
        elif len(seq) < shortest_seq_len:
            shortest_seq_len = len(seq)

    print(code, shortest_seq_len)

    complexity = code_num * shortest_seq_len
    sum_of_complexity += complexity

print(sum_of_complexity)


