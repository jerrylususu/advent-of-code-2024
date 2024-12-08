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

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


antinode_set = set()

for antanna_type, antanna_pos_list in antanna_map.items():
    for antanna_pos1, antanna_pos2 in combinations(antanna_pos_list, 2):
        dist_vector = Pos(antanna_pos2.x - antanna_pos1.x, antanna_pos2.y - antanna_pos1.y)
        g = gcd(dist_vector.x, dist_vector.y)
        dist_vector = Pos(dist_vector.x // g, dist_vector.y // g)

        # check direction of a1->a2
        current_pos = antanna_pos2
        while in_grid(current_pos):
            antinode_set.add(current_pos)
            current_pos = Pos(current_pos.x + dist_vector.x, current_pos.y + dist_vector.y)


        # check direction of a2->a1
        current_pos = antanna_pos1
        while in_grid(current_pos):
            antinode_set.add(current_pos)
            current_pos = Pos(current_pos.x - dist_vector.x, current_pos.y - dist_vector.y)

print(len(antinode_set))

