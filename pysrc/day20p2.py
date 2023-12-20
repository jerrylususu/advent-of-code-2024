with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

initial_grid = [list(line.strip()) for line in lines]

# initial_grid = [row[1:-1] for row in initial_grid[1:-1]]

N_ROW = len(initial_grid)
N_COL = len(initial_grid[0])

BEGIN_POS = (0, 0)
END_POS = (0, 0)

for row_idx in range(N_ROW):
    for col_idx in range(N_COL):
        if initial_grid[row_idx][col_idx] == "S":
            BEGIN_POS = (row_idx, col_idx)
        elif initial_grid[row_idx][col_idx] == "E":
            END_POS = (row_idx, col_idx)

def get_next_pos(cur_pos):
    row_idx, col_idx = cur_pos
    base_list = [(row_idx + 1, col_idx), (row_idx - 1, col_idx), (row_idx, col_idx + 1), (row_idx, col_idx - 1)]
    return base_list

def is_valid_next_step(cur_pos):
    row_idx, col_idx = cur_pos
    if 0 <= row_idx < N_ROW and 0 <= col_idx < N_COL and initial_grid[row_idx][col_idx] != "#":
        return True
    return False



def bfs_min_path(grid, begin_pos, end_pos):
    queue = [(begin_pos, 0)]
    visited = set()

    while queue:
        cur_pos, cur_step = queue.pop(0)

        if cur_pos == end_pos:
            return cur_step

        if cur_pos in visited:
            continue

        visited.add(cur_pos)

        for next_pos in get_next_pos(cur_pos):
            if is_valid_next_step(next_pos):
                queue.append((next_pos, cur_step + 1))
    return None

def bfs_reverse_from_end(grid, end_pos):
    queue = [(end_pos, 0)]
    visited = set()
    pos_to_end_path_len = {}


    while queue:
        cur_pos, cur_step = queue.pop(0)

        if cur_pos in visited:
            continue

        visited.add(cur_pos)

        pos_to_end_path_len[cur_pos] = cur_step

        for next_pos in get_next_pos(cur_pos):
            if is_valid_next_step(next_pos):
                queue.append((next_pos, cur_step + 1))

    return pos_to_end_path_len

from_end = bfs_reverse_from_end(initial_grid, END_POS)
from_start = bfs_reverse_from_end(initial_grid, BEGIN_POS)

base_min_step = from_end[BEGIN_POS]
print(base_min_step)

def get_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# for row_idx in range(N_ROW):
#     for col_idx in range(N_COL):
#         print("working on", row_idx, col_idx)

#         if initial_grid[row_idx][col_idx] == "#":
#             continue

#         path_len = bfs_min_path(initial_grid, (row_idx, col_idx), END_POS)
#         pos_to_end_path_len[(row_idx, col_idx)] = path_len

# print(pos_to_end_path_len)

MAX_DIST = 20
RECORD_THRESHOLD = 100

save_to_hacks = {}

for row_idx in range(N_ROW):
    for col_idx in range(N_COL):
        if initial_grid[row_idx][col_idx] == "#":
            continue

        print("working on", row_idx, col_idx)

        for row_offset in range(-MAX_DIST, MAX_DIST + 1):
            for col_offset in range(-MAX_DIST, MAX_DIST + 1):
                hack_enter = (row_idx, col_idx)
                hack_exit = (row_idx + row_offset, col_idx + col_offset)

                if hack_exit not in from_end:
                    continue

                hack_enter_to_hack_exit = get_dist(hack_enter, hack_exit)
                if hack_enter_to_hack_exit > MAX_DIST:
                    continue

                start_to_hack_enter = from_start[hack_enter]
                hack_exit_to_end = from_end[hack_exit]

                total = start_to_hack_enter + hack_enter_to_hack_exit + hack_exit_to_end
                save = base_min_step - total
                if save >= RECORD_THRESHOLD:
                    if save not in save_to_hacks:
                        save_to_hacks[save] = set()
                    save_to_hacks[save].add((hack_enter, hack_exit))


total = 0

for save, hacks in save_to_hacks.items():
    # print(save, len(hacks), hacks)
    total += len(hacks)

print(total)
