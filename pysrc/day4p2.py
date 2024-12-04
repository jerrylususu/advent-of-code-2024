with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

grid = []
for line in lines:
    chars = list(line.strip())
    grid.append(chars)

def pos_in_grid(grid, x, y):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
        return False
    return True

def check_pos(grid, x, y):
    # x, y as left and up corner

    edge_len = 2
    # all in boundary
    for i in range(edge_len + 1):
        for j in range(edge_len + 1):
            if not pos_in_grid(grid, x+i, y+j):
                return False

    # check center
    if grid[x+1][y+1] != "A":
        return False
    
    # check corner
    valid_configs = ["MMSS", "MSMS", "SSMM", "SMSM"]
    for config in valid_configs:
        if (grid[x][y] == config[0]
            and grid[x+edge_len][y] == config[1] 
            and grid[x][y+edge_len] == config[2] 
            and grid[x+edge_len][y+edge_len] == config[3]):
            return True
    return False


n_rows = len(grid)
n_cols = len(grid[0])

total = 0
for i in range(n_rows):
    for j in range(n_cols):
        if check_pos(grid, i, j):
            total += 1
print(total)