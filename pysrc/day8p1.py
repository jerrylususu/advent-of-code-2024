from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class Pos:
    x: int
    y: int


with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]

n_row = len(grid)
n_col = len(grid[0])


antanna_map = {}

for i in range(n_row):
    for j in range(n_col):
        if grid[i][j] == ".":
            continue

        antanna_type = grid[i][j]
        if antanna_type not in antanna_map:
            antanna_map[antanna_type] = []
        
        antanna_map[antanna_type].append(Pos(i, j))


def in_grid(pos: Pos):
    return 0 <= pos.x < n_row and 0 <= pos.y < n_col


antinode_set = set()

for antanna_type, antanna_pos_list in antanna_map.items():
    for antanna_pos1, antanna_pos2 in combinations(antanna_pos_list, 2):
        dist_vector = Pos(antanna_pos2.x - antanna_pos1.x, antanna_pos2.y - antanna_pos1.y)
        antinode_2 = Pos(antanna_pos2.x + dist_vector.x, antanna_pos2.y + dist_vector.y)
        if in_grid(antinode_2):
            antinode_set.add(antinode_2)

        antinode_1 = Pos(antanna_pos1.x - dist_vector.x, antanna_pos1.y - dist_vector.y)
        if in_grid(antinode_1):
            antinode_set.add(antinode_1)

print(len(antinode_set))

