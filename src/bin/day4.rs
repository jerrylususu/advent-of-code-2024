use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

type Grid = Vec<Vec<char>>;

fn read_file(path: &str) -> Result<Grid, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let mut grid = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let chars: Vec<char> = line.trim().chars().collect();
        grid.push(chars);
    }

    Ok(grid)
}

fn pos_in_grid(grid: &Grid, x: i32, y: i32) -> bool {
    let n_rows: Option<i32> = grid.len().try_into().ok();
    let n_cols: Option<i32> = grid[0].len().try_into().ok();

    if n_rows.is_none() || n_cols.is_none() {
        return false;
    }

    x >= 0 && x < n_rows.unwrap() && y >= 0 && y < n_cols.unwrap()
}

// Part 1 functions
fn is_xmas(chars: &[char]) -> bool {
    if chars.len() != 4 {
        return false;
    }
    chars[0] == 'X' && chars[1] == 'M' && chars[2] == 'A' && chars[3] == 'S'
}

fn count_xmas_whole_line(line: &[char]) -> i32 {
    if line.len() < 4 {
        return 0;
    }

    let mut count = 0;

    // rust 和 py 的切片在边界行为不一致
    for i in 0..=line.len().saturating_sub(4) {
        if is_xmas(&line[i..i + 4]) {
            count += 1;
        }
    }
    count
}

fn traverse_x(grid: &Grid) -> Vec<Vec<char>> {
    grid.clone()
}

fn traverse_y(grid: &Grid) -> Vec<Vec<char>> {
    let mut results = Vec::new();
    for i in 0..grid[0].len() {
        results.push(grid.iter().map(|line| line[i]).collect());
    }
    results
}

fn traverse_diag1(grid: &Grid) -> Vec<Vec<char>> {
    let mut results = Vec::new();
    let n_rows = grid.len();
    let n_cols = grid[0].len();

    let mut left_and_up_edge_pos_list = Vec::new();
    for i in (1..n_rows).rev() {
        left_and_up_edge_pos_list.push((i, 0));
    }
    for i in 0..n_cols {
        left_and_up_edge_pos_list.push((0, i));
    }

    for &(start_x, start_y) in &left_and_up_edge_pos_list {
        let mut collected = Vec::new();
        let mut x = start_x as i32;
        let mut y = start_y as i32;
        while pos_in_grid(grid, x, y) {
            collected.push(grid[x as usize][y as usize]);
            x += 1;
            y += 1;
        }
        results.push(collected);
    }

    results
}

fn traverse_diag2(grid: &Grid) -> Vec<Vec<char>> {
    let mut results = Vec::new();
    let n_rows = grid.len();
    let n_cols = grid[0].len();

    let mut left_and_down_edge_pos_list = Vec::new();
    for i in 0..n_rows {
        left_and_down_edge_pos_list.push((i, 0));
    }
    for i in 1..n_cols {
        left_and_down_edge_pos_list.push((n_rows - 1, i));
    }

    for &(start_x, start_y) in &left_and_down_edge_pos_list {
        let mut collected = Vec::new();
        let mut x = start_x as i32;
        let mut y = start_y as i32;
        while pos_in_grid(grid, x, y) {
            collected.push(grid[x as usize][y as usize]);
            x -= 1;
            y += 1;
        }
        results.push(collected);
    }

    results
}

fn solve_p1(path: &str) -> Result<i32, Box<dyn Error>> {
    let grid = read_file(path)?;
    let possible_lines = [
        traverse_x(&grid),
        traverse_y(&grid),
        traverse_diag1(&grid),
        traverse_diag2(&grid),
    ]
    .concat();

    let mut total = 0;
    for line in possible_lines {
        total += count_xmas_whole_line(&line);
        total += count_xmas_whole_line(&line.iter().rev().copied().collect::<Vec<_>>());
    }

    Ok(total)
}

// Part 2 functions
fn check_pos(grid: &Grid, x: usize, y: usize) -> bool {
    let edge_len = 2 as usize;

    // Check boundary
    for i in 0..=edge_len {
        for j in 0..=edge_len {
            if !pos_in_grid(grid, (x + i) as i32, (y + j) as i32) {
                return false;
            }
        }
    }

    // Check center
    if grid[(x + 1) as usize][(y + 1) as usize] != 'A' {
        return false;
    }

    let valid_configs = ["MMSS", "MSMS", "SSMM", "SMSM"];
    let x = x as usize;
    let y = y as usize;

    for config in valid_configs {
        let chars: Vec<char> = config.chars().collect();
        if grid[x][y] == chars[0]
            && grid[x + edge_len][y] == chars[1]
            && grid[x][y + edge_len] == chars[2]
            && grid[x + edge_len][y + edge_len] == chars[3]
        {
            return true;
        }
    }
    false
}

fn solve_p2(path: &str) -> Result<i32, Box<dyn Error>> {
    let grid = read_file(path)?;
    let n_rows = grid.len();
    let n_cols = grid[0].len();

    let mut total = 0;
    for i in 0..n_rows {
        for j in 0..n_cols {
            if check_pos(&grid, i, j) {
                total += 1;
            }
        }
    }

    Ok(total)
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
        let result = solve_p1("data/day4.txt").unwrap();
        assert_eq!(result, 2397);

        let result_example = solve_p1("data/day4_example.txt").unwrap();
        assert_eq!(result_example, 18);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day4.txt").unwrap();
        assert_eq!(result, 1824);

        let result_example = solve_p2("data/day4_example.txt").unwrap();
        assert_eq!(result_example, 9);
    }
}
