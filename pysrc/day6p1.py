from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]

n_row = len(grid)
n_col = len(grid[0])

def in_grid(pos):
    return 0 <= pos[0] < n_row and 0 <= pos[1] < n_col

# find initial position
pos = (0, 0)
current_direction = Direction.UP
for i in range(n_row):
    for j in range(n_col):
        if grid[i][j] == "^":
            pos = (i, j)
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

def is_blocked(pos):
    if not in_grid(pos):
        return False
    return grid[pos[0]][pos[1]] == "#"

def turn_right(direction):
    if direction == Direction.UP:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    elif direction == Direction.LEFT:
        return Direction.UP

def mark(pos):
    grid[pos[0]][pos[1]] = "X"

while True:
    if not in_grid(pos):
        break
    
    next_pos = get_next_pos(pos, current_direction)
    if is_blocked(next_pos):
        # turn right
        current_direction = turn_right(current_direction)
    else:
        mark(pos)
        pos = next_pos
        
total_marked = 0
for i in range(n_row):
    for j in range(n_col):
        if grid[i][j] == "X":
            total_marked += 1

print(total_marked)

