
from dataclasses import dataclass

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()


@dataclass
class Robot:
    pos_row: int
    pos_col: int
    vel_row: int
    vel_col: int

def parse_line_to_robot(line: str) -> Robot:
    p_str, v_str = line.split(" ")
    p_x, p_y = p_str.split("=")[1].split(",")
    v_x, v_y = v_str.split("=")[1].split(",")
    return Robot(int(p_y), int(p_x), int(v_y), int(v_x))

robots = []

for line in lines:
    robots.append(parse_line_to_robot(line))

print(robots)

TOTAL_STEPS = 100
N_ROW = 103
N_COL = 101

def visualize_grid(robots):
    grid = [["." for _ in range(N_COL)] for _ in range(N_ROW)]
    for r in robots:
        grid[r.pos_row][r.pos_col] = "#"
    for row in grid:
        print("".join(row))


# def in_grid(pos_row, pos_col):
#     return 0 <= pos_row < N_ROW and 0 <= pos_col < N_COL

# def wrap_out_of_grid_pos(pos_row, pos_col):
#     if pos_row < 0:
#         while pos_row < 0:
#             pos_row += N_ROW
#     elif pos_row >= N_ROW:
#         while pos_row >= N_ROW:
#             pos_row -= N_ROW
#     if pos_col < 0:
#         while pos_col < 0:
#             pos_col += N_COL
#     elif pos_col >= N_COL:
#         while pos_col >= N_COL:
#             pos_col -= N_COL
#     return pos_row, pos_col

def get_quadrant_of_pos(pos_row, pos_col):
    middle_row = N_ROW // 2
    middle_col = N_COL // 2

    # 0 | 1
    # -----
    # 2 | 3
    
    if pos_row < middle_row and pos_col < middle_col:
        return 0
    elif pos_row < middle_row and pos_col > middle_col:
        return 1
    elif pos_row > middle_row and pos_col < middle_col:
        return 2
    elif pos_row > middle_row and pos_col > middle_col:
        return 3
    else:
        return None

for i in range(TOTAL_STEPS):
    for robot in robots:
        robot.pos_row = (robot.pos_row + robot.vel_row) % N_ROW
        robot.pos_col = (robot.pos_col + robot.vel_col) % N_COL

visualize_grid(robots)


quad_count_map = {0: 0, 1: 0, 2: 0, 3: 0}

for r in robots:
    print(r)

    quad = get_quadrant_of_pos(r.pos_row, r.pos_col)
    if quad is None:
        continue
    quad_count_map[quad] += 1

print(quad_count_map)

result = quad_count_map[0] * quad_count_map[1] * quad_count_map[2] * quad_count_map[3]
print(result)


