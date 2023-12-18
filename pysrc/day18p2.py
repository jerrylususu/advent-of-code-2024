with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

SIDE_LEN = 71

grid = [['.' for _ in range(SIDE_LEN)] for _ in range(SIDE_LEN)]


def visualize_grid():
    for row in grid:
        print("".join(row))


pos_list = []
for line in lines:
    col, row = map(int, line.split(","))
    pos_list.append((col, row))

START_POS = (0, 0)
END_POS = (SIDE_LEN - 1, SIDE_LEN - 1)

def get_next_pos(pos):
    col, row = pos
    return [(col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)]

def is_vaild_pos(pos):
    col, row = pos
    if not (0 <= col < SIDE_LEN and 0 <= row < SIDE_LEN):
        return False
    if grid[row][col] == "#":
        return False
    return True

def bfs(start_pos, end_pos):
    queue = [(start_pos, [start_pos])]
    visited = set()

    while len(queue) > 0:
        pos, path = queue.pop(0)

        if pos in visited:
            continue
        visited.add(pos)
        
        if pos == end_pos:
            return path
        
        for next_pos in get_next_pos(pos):
            if is_vaild_pos(next_pos):
                queue.append((next_pos, path + [next_pos]))
    return None


# for i in range(len(pos_list)):
#     print("at", i)
#     col, row = pos_list[i]
#     grid[row][col] = "#"

#     path = bfs(START_POS, END_POS)
#     if path is None:
#         # print(f"No path found for {i}", pos_list[i])
#         print(",".join(map(str, pos_list[i])))
#         break


def check_path_exists_at_index(index):
    for i in range(SIDE_LEN):
        for j in range(SIDE_LEN):
            grid[i][j] = '.'
            
    # 放置前index个障碍
    for i in range(index + 1):
        col, row = pos_list[i]
        grid[row][col] = '#'
    
    return bfs(START_POS, END_POS) is not None

left, right = 0, len(pos_list) - 1
result = -1

while left <= right:
    mid = (left + right) // 2
    if check_path_exists_at_index(mid):
        left = mid + 1
    else:
        result = mid
        right = mid - 1

if result != -1:
    print(",".join(map(str, pos_list[result])))