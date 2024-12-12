from enum import Enum
from dataclasses import dataclass

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

type_with_id_grid = [[None] * n_col for _ in range(n_row)]

def get_neighbours(x, y):
    neighbours = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if in_grid(nx, ny):
            neighbours.append((nx, ny))
    return neighbours

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

def get_neighbours_and_direction_without_border_check(row, col):
    neighbours = []
    for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
        if direction == Direction.LEFT:
            neighbours.append((row, col - 1, direction))
        elif direction == Direction.RIGHT:
            neighbours.append((row, col + 1, direction))
        elif direction == Direction.UP:
            neighbours.append((row - 1, col, direction))
        elif direction == Direction.DOWN:
            neighbours.append((row + 1, col, direction))
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
        type_with_id_grid[cx][cy] = type_with_id
        points.append((cx, cy))

        for nx, ny in get_neighbours(cx, cy):
            if not visited[nx][ny] and grid[nx][ny] == current_type:
                queue.append((nx, ny))

    type_with_id_to_points_map[type_with_id] = points


for row in range(n_row):
    for col in range(n_col):
        if not visited[row][col]:
            flood_from(row, col)

# print(type_with_id_to_points_map)

@dataclass(frozen=True)
class Side:
    direction: Direction
    # crossing at
    row_or_col_1: int
    row_or_col_2: int
    # located at
    locate_col_or_row: int

def build_side(direction: Direction, row_or_col_1: int, row_or_col_2: int, locate_col_or_row: int):
    lesser = min(row_or_col_1, row_or_col_2)
    greater = max(row_or_col_1, row_or_col_2)
    return Side(direction, lesser, greater, locate_col_or_row)

# key: (type, id)
# value: set(side)
    # side: (direction, row/col1, row/col2, locate_col_or_row)
type_with_id_to_side_set_map = {}

for type_with_id, points in type_with_id_to_points_map.items():
    side_set = set()
    for row, col in points:
        for i_row, i_col, direction in get_neighbours_and_direction_without_border_check(row, col):

            if in_grid(i_row, i_col) and grid[i_row][i_col] == type_with_id[0]:
                continue

            # print(f"({row}, {col})[{grid[row][col]}] -> ({i_row}, {i_col})[{'ng' if not in_grid(i_row, i_col) else grid[i_row][i_col]}]")
            if direction == Direction.LEFT:
                side = build_side(direction, col, i_col, row)
            elif direction == Direction.RIGHT:
                side = build_side(direction, col, i_col, row)
            elif direction == Direction.UP:
                side = build_side(direction, row, i_row, col)
            elif direction == Direction.DOWN:
                side = build_side(direction, row, i_row, col)
            # print(side)

            side_set.add(side)

    type_with_id_to_side_set_map[type_with_id] = side_set

def count_continuous_ranges(nums):
    if not nums:
        return 0
        
    count = 1
    
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1] + 1:
            count += 1
            
    return count

# try to merge...
def merge_sides(side_set: set[Side]):
    side_map = {}
    for side in side_set:
        key = (side.direction, side.row_or_col_1, side.row_or_col_2)
        if key not in side_map:
            side_map[key] = []
        side_map[key].append(side.locate_col_or_row)

    result_side_to_range_map = {}
    for key, values in side_map.items():
        values.sort()
        result_side_to_range_map[key] = count_continuous_ranges(values)

    return result_side_to_range_map

# for i in type_with_id_to_side_set_map[('C', 1)]:
#     print(i)

# print(merge_sides(type_with_id_to_side_set_map[('C', 1)]))
# print(type_with_id_to_side_set_map)

total_cost = 0
for type_with_id in type_with_id_to_points_map.keys():

    area = len(type_with_id_to_points_map[type_with_id])
    raw_sides = type_with_id_to_side_set_map[type_with_id]
    merged_sides = merge_sides(raw_sides)
    side_count = sum(merged_sides.values())
    print(f"{type_with_id}: {area} * {side_count} = {area * side_count}")
    cost = side_count * area

    total_cost += cost

print(total_cost)
