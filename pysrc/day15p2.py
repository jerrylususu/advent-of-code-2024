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

def transform_grid():
    NEW_N_ROW = N_ROW
    NEW_N_COL = N_COL * 2
    new_grid = [['.' for _ in range(NEW_N_COL)] for _ in range(NEW_N_ROW)]
    for row in range(N_ROW):
        for col in range(N_COL):
            if grid[row][col] == "@":
                new_grid[row][col * 2] = "@"
            elif grid[row][col] == "#":
                new_grid[row][col * 2] = "#"
                new_grid[row][col * 2 + 1] = "#"
            elif grid[row][col] == "O":
                new_grid[row][col * 2] = "["
                new_grid[row][col * 2 + 1] = "]"

    return new_grid



grid = transform_grid()
N_ROW = len(grid)
N_COL = len(grid[0])

robot_pos = (0, 0)
for row in range(N_ROW):
    for col in range(N_COL):
        if grid[row][col] == "@":
            robot_pos = (row, col)
            break

print(robot_pos)



def visualize_grid():
    for row in grid:
        print("".join(row))

visualize_grid()

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

# def get_pos_list_until_wall_axis_row(row, col, operation):
#     pos_list = []
#     while in_grid(row, col) and grid[row][col] != "#":
#         pos_list.append((row, col))
#         row, col = get_next_pos(row, col, operation)
#     return pos_list

def get_another_box_pos(row, col):
    if grid[row][col] == "[":
        return row, col + 1
    elif grid[row][col] == "]":
        return row, col - 1
    else:
        raise Exception(f"invalid box: {row}, {col}")

def bfs_find_all_connected_boxes_incl_robot(robot_row, robot_col, direction):
    boxes = []

    queue = []
    queue.append((robot_row, robot_col))
    visited = set()
    while queue:
        cur_row, cur_col = queue.pop(0)
        if (cur_row, cur_col) in visited:
            continue

        visited.add((cur_row, cur_col))
        if grid[cur_row][cur_col] in ["[", "]"]:
            boxes.append((cur_row, cur_col))

        if direction == "^":
            next_row, next_col = cur_row - 1, cur_col
            if in_grid(next_row, next_col) and grid[next_row][next_col] in ["[", "]"]:
                queue.append((next_row, next_col))
                another_box_pos = get_another_box_pos(next_row, next_col)
                queue.append(another_box_pos)
        elif direction == "v":
            next_row, next_col = cur_row + 1, cur_col
            if in_grid(next_row, next_col) and grid[next_row][next_col] in ["[", "]"]:
                queue.append((next_row, next_col))
                another_box_pos = get_another_box_pos(next_row, next_col)
                queue.append(another_box_pos)
        elif direction == ">":
            next_row, next_col = cur_row, cur_col + 1
            if in_grid(next_row, next_col) and grid[next_row][next_col] in ["[", "]"]:
                queue.append((next_row, next_col))
                another_box_pos = get_another_box_pos(next_row, next_col)
                queue.append(another_box_pos)
        elif direction == "<":
            next_row, next_col = cur_row, cur_col - 1
            if in_grid(next_row, next_col) and grid[next_row][next_col] in ["[", "]"]:
                queue.append((next_row, next_col))
                another_box_pos = get_another_box_pos(next_row, next_col)
                queue.append(another_box_pos)

    return visited




# print(bfs_find_all_connected_boxes_incl_robot(robot_pos[0], robot_pos[1], "<"))

def move_pos_list_by_direction(pos_list, direction):
    return [get_next_pos(pos[0], pos[1], direction) for pos in pos_list]


def check_pos_list_available(pos_list):
    for pos in pos_list:
        if not in_grid(pos[0], pos[1]):
            return False
        if grid[pos[0]][pos[1]] == "#":
            return False
    return True

def make_grid_copy():
    copy_grid = [row[:] for row in grid]
    return copy_grid

def do_move_pos_list_by_direction(pos_list, direction):
    copy_grid = make_grid_copy()
    
    next_pos_set = set()
    all_pos_set = set([pos for pos in pos_list])
    
    for pos in pos_list:
        next_pos = get_next_pos(pos[0], pos[1], direction)
        next_pos_set.add(next_pos)
        grid[next_pos[0]][next_pos[1]] = copy_grid[pos[0]][pos[1]]

    # clear up
    for pos in all_pos_set:
        if pos not in next_pos_set:
            grid[pos[0]][pos[1]] = "."



def move_robot_to_pos(old_pos, new_pos):
    grid[old_pos[0]][old_pos[1]] = "."
    grid[new_pos[0]][new_pos[1]] = "@"


def try_push_at(row, col, operation):
    all_connected_boxes = bfs_find_all_connected_boxes_incl_robot(row, col, operation)
    after_move_boxes = move_pos_list_by_direction(all_connected_boxes, operation)
    if check_pos_list_available(after_move_boxes):
        do_move_pos_list_by_direction(all_connected_boxes, operation)
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
        # robot is already moved
        return next_row, next_col
    else:
        return row, col




for i in range(len(operations)):
    print(f"Step {i}")
    # visualize_grid()
    robot_pos = step(robot_pos, operations[i])

visualize_grid()

def count_pos_value(row, col):
    return (row+1)*100 + (col+2)

sum_pos_value = 0
for row in range(N_ROW):
    for col in range(N_COL):
        if grid[row][col] == "[":
            sum_pos_value += count_pos_value(row, col)


print(sum_pos_value)

