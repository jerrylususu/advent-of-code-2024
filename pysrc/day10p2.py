with open("input.txt", "r", encoding="utf-8") as f:
    data = f.readlines()

grid = []
for line in data:
    row = []
    for i in list(line.strip()):
        if '0' <= i <= '9':
            row.append(int(i))
        else:
            row.append(None)
    grid.append(row)

n_row = len(grid)
n_col = len(grid[0])

def in_grid(x, y):
    return 0 <= x < n_row and 0 <= y < n_col

# find all start points
start_points = []
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == 0:
            start_points.append((i, j))

print(start_points)

def get_next_positions(x, y):
    current = grid[x][y]
    next_positions = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if in_grid(nx, ny) and grid[nx][ny] == current + 1:
            next_positions.append((nx, ny))
    return next_positions

def build_path(cur_x, cur_y, current_path, all_paths):
    if grid[cur_x][cur_y] == 9:
        # print(current_path)
        all_paths.append(current_path)
        return
    next_positions = get_next_positions(cur_x, cur_y)
    for next_position in next_positions:
        build_path(next_position[0], next_position[1], current_path + [next_position], all_paths)


# for a given start point, find paths starting from it
def find_paths(grid, start_point):
    all_paths = []
    build_path(start_point[0], start_point[1], [start_point], all_paths)
    return all_paths

total_path_count = 0
for start_point in start_points:
    paths = find_paths(grid, start_point)
    total_path_count += len(paths)
    print(start_point, len(paths))

print(total_path_count)


