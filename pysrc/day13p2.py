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


def calc_cost(a_press: int, b_press: int):
    return a_press * 3 + b_press * 1

def find_combination(game: GameSetting):
    a_x = game.button_a_x
    b_x = game.button_b_x
    a_y = game.button_a_y
    b_y = game.button_b_y
    t_x = game.prize_x
    t_y = game.prize_y

    b_n = (t_x*a_y - t_y*a_x) / (a_y*b_x - b_y*a_x)
    a_n = (t_x - b_n * b_x) / a_x

    if not a_n.is_integer() or not b_n.is_integer():
        return None, None

    return int(a_n), int(b_n)


def try_solve_game(game: GameSetting):
    a_n, b_n = find_combination(game)
    if a_n is None or b_n is None:
        return None

    return calc_cost(a_n, b_n)

ADD_TARGET = 10000000000000

total_token = 0
for game in games:
    updated_game = GameSetting(
        button_a_x=game.button_a_x,
        button_a_y=game.button_a_y,
        button_b_x=game.button_b_x,
        button_b_y=game.button_b_y,
        prize_x=game.prize_x + ADD_TARGET,
        prize_y=game.prize_y + ADD_TARGET,
    )
    result = try_solve_game(updated_game)
    print(updated_game, result)
    if result is not None:
        total_token += result

print(total_token)
