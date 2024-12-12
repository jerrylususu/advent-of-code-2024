with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]

n_row = len(grid)
n_col = len(grid[0])

def in_grid(x, y):
    return 0 <= x < n_row and 0 <= y < n_col

# key: (type, id)
# value: list[(x, y)]
type_with_id_to_points_map = {}

# key: type
# value: count
type_to_type_count_map = {}

visited = [[False] * n_col for _ in range(n_row)]

def get_neighbours(x, y):
    neighbours = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if in_grid(nx, ny):
            neighbours.append((nx, ny))
    return neighbours

def get_neighbours_without_border_check(x, y):
    neighbours = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        neighbours.append((nx, ny))
    return neighbours

def flood_from(x, y):
    current_type = grid[x][y]
    if current_type not in type_to_type_count_map:
        type_to_type_count_map[current_type] = 0
    type_to_type_count_map[current_type] += 1
    type_with_id = (current_type, type_to_type_count_map[current_type])

    points = []
    queue = []
    queue.append((x, y))

    while queue:
        cx, cy = queue.pop(0)
        if visited[cx][cy]:
            continue
        visited[cx][cy] = True
        points.append((cx, cy))

        for nx, ny in get_neighbours(cx, cy):
            if not visited[nx][ny] and grid[nx][ny] == current_type:
                queue.append((nx, ny))

    type_with_id_to_points_map[type_with_id] = points


for x in range(n_row):
    for y in range(n_col):
        if not visited[x][y]:
            flood_from(x, y)

# print(type_with_id_to_points_map)

# key: (type, id)
# value: perimeter
type_with_id_to_perimeter_map = {}

for type_with_id, points in type_with_id_to_points_map.items():
    perimeter = 0
    for x, y in points:
        for nx, ny in get_neighbours_without_border_check(x, y):
            if not in_grid(nx, ny):
                perimeter += 1
                continue

            if grid[nx][ny] != type_with_id[0]:
                perimeter += 1
                continue

    type_with_id_to_perimeter_map[type_with_id] = perimeter

# print(type_with_id_to_perimeter_map)

total_cost = 0
for type_with_id in type_with_id_to_points_map.keys():

    area = len(type_with_id_to_points_map[type_with_id])
    perimeter = type_with_id_to_perimeter_map[type_with_id]
    cost = perimeter * area

    total_cost += cost

print(total_cost)
