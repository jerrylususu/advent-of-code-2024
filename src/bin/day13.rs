use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

#[derive(Debug, Clone, Copy)]
struct GameSetting {
    button_a_x: i64,
    button_a_y: i64,
    button_b_x: i64,
    button_b_y: i64,
    prize_x: i64,
    prize_y: i64,
}

fn parse_button_line(lines: &[String]) -> Result<GameSetting, Box<dyn Error>> {
    if lines.len() != 3 {
        return Err("Invalid number of lines".into());
    }

    let parse_button = |line: &str| -> Option<(i64, i64)> {
        let parts: Vec<&str> = line.split(": ").nth(1)?.split(", ").collect();
        let x = parts.get(0)?.strip_prefix("X+")?.parse().ok()?;
        let y = parts.get(1)?.strip_prefix("Y+")?.parse().ok()?;
        Some((x, y))
    };

    let parse_prize = |line: &str| -> Option<(i64, i64)> {
        let parts: Vec<&str> = line.split(": ").nth(1)?.split(", ").collect();
        let x = parts.get(0)?.strip_prefix("X=")?.parse().ok()?;
        let y = parts.get(1)?.strip_prefix("Y=")?.parse().ok()?;
        Some((x, y))
    };

    let (button_a_x, button_a_y) = parse_button(&lines[0])
        .ok_or("Failed to parse button A")?;
    let (button_b_x, button_b_y) = parse_button(&lines[1])
        .ok_or("Failed to parse button B")?;
    let (prize_x, prize_y) = parse_prize(&lines[2])
        .ok_or("Failed to parse prize")?;

    Ok(GameSetting {
        button_a_x,
        button_a_y,
        button_b_x,
        button_b_y,
        prize_x,
        prize_y,
    })
}

fn parse_games(lines: Vec<String>) -> Result<Vec<GameSetting>, Box<dyn Error>> {
    let mut games = Vec::new();
    let mut current_game_lines = Vec::new();

    for line in lines {
        if line.trim().is_empty() {
            if !current_game_lines.is_empty() {
                games.push(parse_button_line(&current_game_lines)?);
                current_game_lines.clear();
            }
        } else {
            current_game_lines.push(line);
        }
    }

    if !current_game_lines.is_empty() {
        games.push(parse_button_line(&current_game_lines)?);
    }

    Ok(games)
}

fn calc_cost(a_press: i64, b_press: i64) -> i64 {
    a_press * 3 + b_press * 1
}

fn find_combination(game: &GameSetting) -> Option<(i64, i64)> {
    let a_x = game.button_a_x;
    let b_x = game.button_b_x;
    let a_y = game.button_a_y;
    let b_y = game.button_b_y;
    let t_x = game.prize_x;
    let t_y = game.prize_y;

    let denominator = a_y * b_x - b_y * a_x;
    if denominator == 0 {
        return None;
    }

    let b_n = (t_x * a_y - t_y * a_x) as f64 / denominator as f64;
    let a_n = (t_x as f64 - b_n * b_x as f64) / a_x as f64;

    if !(a_n.fract().abs() < f64::EPSILON) || !(b_n.fract().abs() < f64::EPSILON) {
        return None;
    }

    Some((a_n.round() as i64, b_n.round() as i64))
}

fn try_solve_game(game: &GameSetting) -> Option<i64> {
    find_combination(game).map(|(a_n, b_n)| calc_cost(a_n, b_n))
}

fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let games = parse_games(lines)?;
    
    Ok(games.iter()
        .filter_map(|game| try_solve_game(game))
        .sum())
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let games = parse_games(lines)?;
    const ADD_TARGET: i64 = 10_000_000_000_000;
    
    Ok(games.iter()
        .filter_map(|game| {
            let updated_game = GameSetting {
                button_a_x: game.button_a_x,
                button_a_y: game.button_a_y,
                button_b_x: game.button_b_x,
                button_b_y: game.button_b_y,
                prize_x: game.prize_x + ADD_TARGET,
                prize_y: game.prize_y + ADD_TARGET,
            };
            try_solve_game(&updated_game)
        })
        .sum())
}

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn main() -> Result<(), Box<dyn Error>> {
    let result_p1 = solve_p1("input.txt")?;
    println!("Part 1: {}", result_p1);

    let result_p2 = solve_p2("input.txt")?;
    println!("Part 2: {}", result_p2);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_p1() {
        let result = solve_p1("data/day13.txt").unwrap();
        assert_eq!(result, 40069);

        let result_example = solve_p1("data/day13_example.txt").unwrap();
        assert_eq!(result_example, 480);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day13.txt").unwrap();
        assert_eq!(result, 71493195288102);

        let result_example = solve_p2("data/day13_example.txt").unwrap();
        assert_eq!(result_example, 875318608908);
    }
} 