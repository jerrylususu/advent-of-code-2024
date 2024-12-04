with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

grid = []
for line in lines:
    chars = list(line.strip())
    grid.append(chars)


def is_xmas(list):
    if len(list) != 4:
        return False

    return list[0] == "X" and list[1] == "M" and list[2] == "A" and list[3] == "S"

def pos_in_grid(grid, x, y):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
        return False
    return True

# direction: x, y, diag1, diag2
# also need to consider the reverse direction

def count_xmas_whole_line(list):
    count = 0
    for i in range(len(list)):
        if is_xmas(list[i:i+4]):
            count += 1
    return count

def traverse_x(grid):
    results = []
    for line in grid:
        results.append(line)
    return results

def traverse_y(grid):
    results = []
    for i in range(len(grid[0])):
        results.append([line[i] for line in grid])
    return results

def traverse_diag1(grid):
    results = []
    n_rows = len(grid)
    n_cols = len(grid[0])
    
    left_and_up_edge_pos_list = []
    for i in range(n_rows - 1, 0, -1):
        left_and_up_edge_pos_list.append((i,0))
    for i in range(n_cols):
        left_and_up_edge_pos_list.append((0,i))

    for initial_pos in left_and_up_edge_pos_list:
        pos = initial_pos
        collected = []
        while pos_in_grid(grid, pos[0], pos[1]):
            collected.append(grid[pos[0]][pos[1]])
            pos = (pos[0] + 1, pos[1] + 1)
        results.append(collected)

    return results

def traverse_diag2(grid):
    results = []
    n_rows = len(grid)
    n_cols = len(grid[0])
    
    left_and_down_edge_pos_list = []
    for i in range(n_rows):
        left_and_down_edge_pos_list.append((i,0))
    for i in range(1, n_cols):
        left_and_down_edge_pos_list.append((n_rows-1,i))

    for initial_pos in left_and_down_edge_pos_list:
        pos = initial_pos
        collected = []
        while pos_in_grid(grid, pos[0], pos[1]):
            collected.append(grid[pos[0]][pos[1]])
            pos = (pos[0] - 1, pos[1] + 1)
        results.append(collected)

    return results

total = 0
possible_lines = traverse_x(grid) + traverse_y(grid) + traverse_diag1(grid) + traverse_diag2(grid)
for line in possible_lines:
    total += count_xmas_whole_line(line)
    total += count_xmas_whole_line(line[::-1])

print(total)