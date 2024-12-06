from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

orig_grid = [list(line.strip()) for line in lines]

n_row = len(orig_grid)
n_col = len(orig_grid[0])

def copy_grid(grid):
    return [row[:] for row in grid]

def in_grid(pos):
    return 0 <= pos[0] < n_row and 0 <= pos[1] < n_col

# find initial position
initial_pos = (0, 0)
for i in range(n_row):
    for j in range(n_col):
        if orig_grid[i][j] == "^":
            initial_pos = (i, j)
            break

def get_next_pos(pos, direction):
    if direction == Direction.UP:
        return (pos[0] - 1, pos[1])
    elif direction == Direction.DOWN:
        return (pos[0] + 1, pos[1])
    elif direction == Direction.LEFT:
        return (pos[0], pos[1] - 1)
    elif direction == Direction.RIGHT:
        return (pos[0], pos[1] + 1) 

def is_blocked(mut_grid, pos):
    if not in_grid(pos):
        return False
    return mut_grid[pos[0]][pos[1]] == "#"

def turn_right(direction):
    if direction == Direction.UP:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    elif direction == Direction.LEFT:
        return Direction.UP

def path_is_circle(mut_grid):
    pos = initial_pos
    current_direction = Direction.UP

    # stores (pos, direction)
    visited_pos_and_direction = set()

    while True:
        pd = (pos, current_direction)
        if pd in visited_pos_and_direction:
            return True
        
        visited_pos_and_direction.add(pd)

        if not in_grid(pos):
            return False
        
        next_pos = get_next_pos(pos, current_direction)
        if is_blocked(mut_grid, next_pos):
            # turn right
            current_direction = turn_right(current_direction)
        else:
            pos = next_pos


total_placement = 0
for i in range(n_row):
    for j in range(n_col):
        print(i,j)
        mut_grid = copy_grid(orig_grid)

        # try place
        mut_grid[i][j] = "#"
        if path_is_circle(mut_grid):
            total_placement += 1
        
print(total_placement)
