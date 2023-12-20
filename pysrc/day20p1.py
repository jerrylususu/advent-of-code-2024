import multiprocessing as mp
from functools import partial

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

initial_grid = [list(line.strip()) for line in lines]

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
    return [(row_idx + 1, col_idx), (row_idx - 1, col_idx), (row_idx, col_idx + 1), (row_idx, col_idx - 1)]

def is_valid_step(grid, next_pos):
    row_idx, col_idx = next_pos
    return 0 <= row_idx < N_ROW and 0 <= col_idx < N_COL and grid[row_idx][col_idx] != "#"

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
            if is_valid_step(grid, next_pos):
                queue.append((next_pos, cur_step + 1))
    return None

base_min_step = bfs_min_path(initial_grid, BEGIN_POS, END_POS)
print(base_min_step)

def get_hack_on_pos(grid, pos):
    if grid[pos[0]][pos[1]] != "#":
        return None

    hack_list = []
    next_pos_list = get_next_pos(pos)
    for next_pos in next_pos_list:
        if is_valid_step(grid, next_pos):
            hack_list.append((pos, next_pos))
    
    return hack_list

def get_all_possible_hacks():
    all_hack_set = set()

    for row_idx in range(N_ROW):
        for col_idx in range(N_COL):
            hacks = get_hack_on_pos(initial_grid, (row_idx, col_idx))
            if hacks is not None:
                all_hack_set.update(hacks)
    return all_hack_set

def copy_grid(grid):
    new_grid = []
    for row in grid:
        new_grid.append(row[:])
    return new_grid

def eval_hack(grid, hack):
    new_grid = copy_grid(grid)
    hack_entry = hack[0]
    # hack_exit = hack[1]
    new_grid[hack_entry[0]][hack_entry[1]] = "."
    min_step = bfs_min_path(new_grid, BEGIN_POS, END_POS)
    return min_step

def process_single_hack(hack_with_index):
    index, hack = hack_with_index
    print("workin on", index)
    
    min_step = eval_hack(initial_grid, hack)
    diff = min_step - base_min_step
    if diff == 0:
        return None
    return (hack, diff)

def process_all_hacks(all_hacks, initial_grid, base_min_step):
    # 获取CPU核心数
    num_cores = mp.cpu_count()
    
    # 创建进程池
    with mp.Pool(num_cores) as pool:
        # 给hack添加索引
        indexed_hacks = list(enumerate(all_hacks))
        
        # 并行处理所有hack
        results = list(pool.imap_unordered(process_single_hack, indexed_hacks))
        
        # 过滤掉None结果并返回有效的hack结果
        return [r for r in results if r is not None]

if __name__ == '__main__':
    all_hacks = get_all_possible_hacks()

    print("len hacks", len(all_hacks))

    hacks_to_eval = process_all_hacks(all_hacks, initial_grid, base_min_step)

    diff_to_count = {}

    for hack, diff in hacks_to_eval:
        diff_to_count[diff] = diff_to_count.get(diff, 0) + 1

    print(diff_to_count)

    # hack are counted by hack_enter, should divided by 2

    save_more_than_100_count = 0

    for diff, count in diff_to_count.items():
        if count > 100:
            save_more_than_100_count += count/2

    print(save_more_than_100_count)

def vis_grid(grid):
    for row in grid:
        print("".join(row))

def vis_hack(grid, hack):
    new_grid = copy_grid(grid)
    hack_entry = hack[0]
    hack_exit = hack[1]
    new_grid[hack_entry[0]][hack_entry[1]] = "1"
    new_grid[hack_exit[0]][hack_exit[1]] = "2"

    vis_grid(new_grid)
