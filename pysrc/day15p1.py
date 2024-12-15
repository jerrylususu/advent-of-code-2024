with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

grid = []

operations = []

for line in lines:
    line = line.strip()
    if line.startswith("#") and line.endswith("#"):
        grid.append(list(line[1:-1]))
    elif line == "":
        continue
    else:
        ops = [i for i in line]
        operations += ops

grid = grid[1:-1]
print(grid)

print(operations)

N_ROW = len(grid)
N_COL = len(grid[0])

robot_pos = (0, 0)
for row in range(N_ROW):
    for col in range(N_COL):
        if grid[row][col] == "@":
            robot_pos = (row, col)
            break

print(robot_pos)


def get_next_pos(row, col, operation):
    if operation == "v":
        return row + 1, col
    elif operation == "^":
        return row - 1, col
    elif operation == ">":
        return row, col + 1
    elif operation == "<":
        return row, col - 1

def in_grid(row, col):
    return 0 <= row < N_ROW and 0 <= col < N_COL

def not_occupied(row, col):
    return grid[row][col] == "."

def get_pos_list_until_wall(row, col, operation):
    pos_list = []
    while in_grid(row, col) and grid[row][col] != "#":
        pos_list.append((row, col))
        row, col = get_next_pos(row, col, operation)
    return pos_list

def move_robot_to_pos(old_pos, new_pos):
    grid[old_pos[0]][old_pos[1]] = "."
    grid[new_pos[0]][new_pos[1]] = "@"

def try_push_at(row, col, operation):
    # print(f"try_push_at {row}, {col}, {operation}")
    next_row, next_col = get_next_pos(row, col, operation)

    # is there any space?
    pos_list = get_pos_list_until_wall(row, col, operation)
    # print(f"pos_list: {pos_list}")
    some_empty_space = False
    first_empty_space_idx = None
    for idx, pos in enumerate(pos_list):
        if not_occupied(pos[0], pos[1]):
            some_empty_space = True
            first_empty_space_idx = idx
            break
    # print(f"some_empty_space: {some_empty_space}, first_empty_space_idx: {first_empty_space_idx}")
    if some_empty_space:
        # can actually push
        for idx in range(first_empty_space_idx + 1):
            pos = pos_list[idx]
            grid[pos[0]][pos[1]] = "O"
        grid[next_row][next_col] = "."
        # move_robot_to_pos((row, col), (next_row, next_col))
        return True
    else:
        return False



def step(robot_pos, operation):
    row, col = robot_pos
    next_row, next_col = get_next_pos(row, col, operation)

    if not in_grid(next_row, next_col):
        return row, col

    if not_occupied(next_row, next_col):
        move_robot_to_pos((row, col), (next_row, next_col))
        return next_row, next_col
    
    can_be_pushed = try_push_at(row, col, operation)
    if can_be_pushed:
        move_robot_to_pos((row, col), (next_row, next_col))
        return next_row, next_col
    else:
        return row, col


def visualize_grid():
    for row in grid:
        print("".join(row))

for i in range(len(operations)):
    print(f"Step {i}")
    # visualize_grid()
    robot_pos = step(robot_pos, operations[i])

visualize_grid()

def count_pos_value(row, col):
    return (row+1)*100 + (col+1)

sum_pos_value = 0
for row in range(N_ROW):
    for col in range(N_COL):
        if grid[row][col] == "O":
            sum_pos_value += count_pos_value(row, col)

print(sum_pos_value)

