with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

SIDE_LEN = 71
STOP_AT = 1024

grid = [['.' for _ in range(SIDE_LEN)] for _ in range(SIDE_LEN)]


def visualize_grid():
    for row in grid:
        print("".join(row))


pos_list = []
for line in lines:
    col, row = map(int, line.split(","))
    pos_list.append((col, row))

for i in range(STOP_AT):
    col, row = pos_list[i]
    grid[row][col] = "#"



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

    while True:
        pos, path = queue.pop(0)

        if pos in visited:
            continue
        visited.add(pos)
        
        if pos == end_pos:
            return path
        
        for next_pos in get_next_pos(pos):
            if is_vaild_pos(next_pos):
                queue.append((next_pos, path + [next_pos]))
            

path = bfs(START_POS, END_POS)

# print(path)
print(len(path) - 1)
