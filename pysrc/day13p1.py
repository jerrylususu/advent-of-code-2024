from dataclasses import dataclass
import re

with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

@dataclass(frozen=True)
class GameSetting:
    button_a_x: int
    button_a_y: int
    button_b_x: int
    button_b_y: int
    prize_x: int
    prize_y: int

BUTTON_PATTERN = re.compile(r"Button (\w): X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN = re.compile(r"Prize: X\=(\d+), Y\=(\d+)")

def parse_button_line(lines: str):
    if len(lines) != 3:
        raise Exception("invalid")

    button_a_match = BUTTON_PATTERN.match(lines[0])
    button_b_match = BUTTON_PATTERN.match(lines[1])
    prize_match = PRIZE_PATTERN.match(lines[2])

    if not button_a_match or not button_b_match or not prize_match:
        raise Exception("invalid")

    return GameSetting(
        button_a_x=int(button_a_match.groups()[1]),
        button_a_y=int(button_a_match.groups()[2]),
        button_b_x=int(button_b_match.groups()[1]),
        button_b_y=int(button_b_match.groups()[2]),
        prize_x=int(prize_match.groups()[0]),
        prize_y=int(prize_match.groups()[1]),
    )


games = []

current_game_lines = []
for line in lines:
    if line.strip() == "":
        games.append(parse_button_line(current_game_lines))
        current_game_lines = []
    else:
        current_game_lines.append(line)

games.append(parse_button_line(current_game_lines))
# print(games)

UPPER_LIMIT = 100

def calc_cost(a_press: int, b_press: int):
    return a_press * 3 + b_press * 1

def try_solve_game(game: GameSetting):

    # None = unsolvable
    minimum_cost = None

    for a_press in range(UPPER_LIMIT + 1):
        for b_press in range(UPPER_LIMIT + 1):
            x_pos = a_press * game.button_a_x + b_press * game.button_b_x
            y_pos = a_press * game.button_a_y + b_press * game.button_b_y

            if x_pos == game.prize_x and y_pos == game.prize_y:
                cost = calc_cost(a_press, b_press)
                if minimum_cost is None or cost < minimum_cost:
                    minimum_cost = cost

    return minimum_cost

total_token = 0
for game in games:
    result = try_solve_game(game)
    if result is not None:
        total_token += result

print(total_token)
