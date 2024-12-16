from collections import defaultdict
from enum import Enum
import heapq

with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

grid = []
for line in lines:
    grid.append(list(line.strip()))

N_ROW = len(grid)
N_COL = len(grid[0])

START_POS = (0, 0)
END_POS = (0, 0)

for row in range(N_ROW):
    for col in range(N_COL):
        if grid[row][col] == "S":
            START_POS = (row, col)
        if grid[row][col] == "E":
            END_POS = (row, col)

paths = []

class Facing(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    @staticmethod
    def turn_right(facing):
        return Facing((facing.value + 1) % 4)

    @staticmethod
    def turn_left(facing):
        return Facing((facing.value - 1) % 4)
    
def get_next_pos(pos, facing):
    row, col = pos
    if facing == Facing.EAST:
        return (row, col + 1)
    elif facing == Facing.SOUTH:
        return (row + 1, col)
    elif facing == Facing.WEST:
        return (row, col - 1)
    elif facing == Facing.NORTH:
        return (row - 1, col)

def is_valid_move(grid, pos):
    row, col = pos
    if row < 0 or row >= N_ROW or col < 0 or col >= N_COL:
        return False
    return grid[row][col] != "#"

paths = []

parents = defaultdict(list)
best_scores = {}

def solve_dijkstra(grid, end_pos, start_pos):
    min_score = float("inf")
    queue = [(0, start_pos, Facing.EAST.value)]
    visited = set()

    while queue:
        current_score, current_pos, current_facing = heapq.heappop(queue)
        current_facing = Facing(current_facing)

        if (current_pos, current_facing) in visited:
            continue

        visited.add((current_pos, current_facing))

        if current_pos == end_pos:
            if current_score < min_score:
                min_score = current_score
            continue
        
        # try moving forward
        next_pos = get_next_pos(current_pos, current_facing)
        if is_valid_move(grid, next_pos):
            next_facing = current_facing
            next_score = current_score + 1
            next_state = (next_pos, next_facing.value)
            if next_state not in visited \
                and (next_state not in best_scores or next_score <= best_scores[next_state]):
                best_scores[next_state] = next_score
                parents[next_state].append((current_pos, current_facing.value))
                heapq.heappush(queue, (next_score, next_pos, next_facing.value))

        # try turning
        for turn_direction in [Facing.turn_right, Facing.turn_left]:
            next_facing = turn_direction(current_facing)
            next_score = current_score + 1000
            next_state = (current_pos, next_facing.value)
            if next_state not in visited \
                and (next_state not in best_scores or next_score <= best_scores[next_state]):
                best_scores[next_state] = next_score
                parents[next_state].append((current_pos, current_facing.value))
                heapq.heappush(queue, (next_score, current_pos, next_facing.value))


    return min_score

def backtrack(state, path):
    if state[0] == START_POS:
        paths.append(path[::-1])
        return
    for parent in parents[state]:
        next_path = path[:]
        if parent[0] not in next_path:
            next_path.append(parent[0])
        backtrack(parent, next_path)


def visualize_path(grid, path):
    for row in range(N_ROW):
        for col in range(N_COL):
            if (row, col) in path:
                print("O", end="")
            else:
                print(grid[row][col], end="")
        print()

def get_to_next_facing(pos, next_pos):
    if pos[0] == next_pos[0]:
        if pos[1] < next_pos[1]:
            return Facing.EAST
        else:
            return Facing.WEST
    else:
        if pos[0] < next_pos[0]:
            return Facing.SOUTH
        else:
            return Facing.NORTH

def calc_score_on_path(path):
    score = 0
    facing = Facing.EAST
    pos = path[0]
    for idx in range(1, len(path)):
        next_pos = path[idx]
        to_next_facing = get_to_next_facing(pos, next_pos)
        pos = next_pos
        score += 1

        if to_next_facing == facing:
            continue
        else:
            score += 1000
            facing = to_next_facing
    return score


min_score = solve_dijkstra(grid, END_POS, START_POS)
# print(best_scores)
# print(len(parents))
# for state in parents:
    # print(state, parents[state])
end_states = [state for state in best_scores if state[0] == END_POS]
print(end_states)
for state in end_states:
    backtrack(state, [state[0]])

# print(len(paths))
# print(min_score)

min_score_pos_set = set()

for path in paths:
    score = calc_score_on_path(path)
    if score == min_score:
        for pos in path:
            min_score_pos_set.add(pos)
print(len(min_score_pos_set))
