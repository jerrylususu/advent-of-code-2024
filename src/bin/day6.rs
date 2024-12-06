use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

type Grid = Vec<Vec<char>>;
type Position = (usize, usize);

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_grid(lines: Vec<String>) -> Grid {
    lines.iter().map(|line| line.chars().collect()).collect()
}

fn find_initial_position(grid: &Grid) -> Position {
    for (i, row) in grid.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {
            if cell == '^' {
                return (i, j);
            }
        }
    }
    (0, 0)
}

fn in_grid(pos: Position, n_row: usize, n_col: usize) -> bool {
    pos.0 < n_row && pos.1 < n_col
}

fn get_next_pos(pos: Position, direction: Direction) -> Position {
    match direction {
        Direction::Up => (pos.0.wrapping_sub(1), pos.1),
        Direction::Down => (pos.0 + 1, pos.1),
        Direction::Left => (pos.0, pos.1.wrapping_sub(1)),
        Direction::Right => (pos.0, pos.1 + 1),
    }
}

fn is_blocked(grid: &Grid, pos: Position) -> bool {
    if !in_grid(pos, grid.len(), grid[0].len()) {
        return false;
    }
    grid[pos.0][pos.1] == '#'
}

fn turn_right(direction: Direction) -> Direction {
    match direction {
        Direction::Up => Direction::Right,
        Direction::Right => Direction::Down,
        Direction::Down => Direction::Left,
        Direction::Left => Direction::Up,
    }
}

fn solve_p1(path: &str) -> Result<i32, Box<dyn Error>> {
    let lines = read_file(path)?;
    let mut grid = parse_grid(lines);
    let initial_pos = find_initial_position(&grid);
    let mut pos = initial_pos;
    let mut current_direction = Direction::Up;
    let n_row = grid.len();
    let n_col = grid[0].len();

    while in_grid(pos, n_row, n_col) {
        let next_pos = get_next_pos(pos, current_direction);
        if is_blocked(&grid, next_pos) {
            current_direction = turn_right(current_direction);
        } else {
            grid[pos.0][pos.1] = 'X';
            pos = next_pos;
        }
    }

    let total_marked = grid.iter()
        .flat_map(|row| row.iter())
        .filter(|&&c| c == 'X')
        .count();

    Ok(total_marked as i32)
}

fn path_is_circle(grid: &Grid, initial_pos: Position) -> bool {
    use std::collections::HashSet;
    
    let mut pos = initial_pos;
    let mut current_direction = Direction::Up;
    let mut visited = HashSet::new();
    
    loop {
        let state = (pos, current_direction);
        if visited.contains(&state) {
            return true;
        }
        
        if !in_grid(pos, grid.len(), grid[0].len()) {
            return false;
        }
        
        visited.insert(state);
        let next_pos = get_next_pos(pos, current_direction);
        
        if is_blocked(grid, next_pos) {
            current_direction = turn_right(current_direction);
        } else {
            pos = next_pos;
        }
    }
}

fn solve_p2(path: &str) -> Result<i32, Box<dyn Error>> {
    let lines = read_file(path)?;
    let orig_grid = parse_grid(lines);
    let initial_pos = find_initial_position(&orig_grid);
    let n_row = orig_grid.len();
    let n_col = orig_grid[0].len();
    let mut total_placement = 0;

    for i in 0..n_row {
        // slow, show progress
        println!("{}", i);
        for j in 0..n_col {
            let mut grid = orig_grid.clone();
            grid[i][j] = '#';
            if path_is_circle(&grid, initial_pos) {
                total_placement += 1;
            }
        }
    }

    Ok(total_placement)
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
        let result = solve_p1("data/day6.txt").unwrap();
        assert_eq!(result, 5516);

        let result_example = solve_p1("data/day6_example.txt").unwrap();
        assert_eq!(result_example, 41);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day6.txt").unwrap();
        assert_eq!(result, 2008);

        let result_example = solve_p2("data/day6_example.txt").unwrap();
        assert_eq!(result_example, 6);
    }
} 