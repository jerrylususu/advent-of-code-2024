use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

type Grid = Vec<Vec<Option<i32>>>;
type Point = (usize, usize);

fn parse_input(path: &str) -> Result<Grid, Box<dyn Error>> {
    let lines = read_file(path)?;
    let grid = lines
        .iter()
        .map(|line| {
            line.chars()
                .map(|c| {
                    if c.is_ascii_digit() {
                        Some(c.to_digit(10).unwrap() as i32)
                    } else {
                        None
                    }
                })
                .collect()
        })
        .collect();
    Ok(grid)
}

fn in_grid(x: i32, y: i32, n_row: i32, n_col: i32) -> bool {
    x >= 0 && x < n_row && y >= 0 && y < n_col
}

fn find_start_points(grid: &Grid) -> Vec<Point> {
    let mut start_points = Vec::new();
    for (i, row) in grid.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {
            if cell == Some(0) {
                start_points.push((i, j));
            }
        }
    }
    start_points
}

fn get_next_positions(grid: &Grid, x: usize, y: usize) -> Vec<Point> {
    let current = grid[x][y].unwrap();
    let n_row = grid.len() as i32;
    let n_col = grid[0].len() as i32;
    let directions = [(0, 1), (0, -1), (1, 0), (-1, 0)];
    
    directions.iter()
        .filter_map(|&(dx, dy)| {
            let nx = x as i32 + dx;
            let ny = y as i32 + dy;
            if in_grid(nx, ny, n_row, n_col) {
                let next_value = grid[nx as usize][ny as usize];
                if next_value == Some(current + 1) {
                    return Some((nx as usize, ny as usize));
                }
            }
            None
        })
        .collect()
}

fn build_paths(
    grid: &Grid,
    cur_pos: Point,
    current_path: Vec<Point>,
    all_paths: &mut Vec<Vec<Point>>,
) {
    if grid[cur_pos.0][cur_pos.1] == Some(9) {
        all_paths.push(current_path);
        return;
    }
    
    let next_positions = get_next_positions(grid, cur_pos.0, cur_pos.1);
    for next_pos in next_positions {
        let mut new_path = current_path.clone();
        new_path.push(next_pos);
        build_paths(grid, next_pos, new_path, all_paths);
    }
}

fn find_paths(grid: &Grid, start_point: Point) -> Vec<Vec<Point>> {
    let mut all_paths = Vec::new();
    build_paths(grid, start_point, vec![start_point], &mut all_paths);
    all_paths
}

fn solve_p1(path: &str) -> Result<usize, Box<dyn Error>> {
    let grid = parse_input(path)?;
    let start_points = find_start_points(&grid);
    
    let total_endpoint_count = start_points.iter()
        .map(|&start_point| {
            let paths = find_paths(&grid, start_point);
            let endpoint_set: HashSet<_> = paths.iter()
                .map(|path| *path.last().unwrap())
                .collect();
            endpoint_set.len()
        })
        .sum();
    
    Ok(total_endpoint_count)
}

fn solve_p2(path: &str) -> Result<usize, Box<dyn Error>> {
    let grid = parse_input(path)?;
    let start_points = find_start_points(&grid);
    
    let total_path_count = start_points.iter()
        .map(|&start_point| find_paths(&grid, start_point).len())
        .sum();
    
    Ok(total_path_count)
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
        let result = solve_p1("data/day10.txt").unwrap();
        assert_eq!(result, 717);

        let result_example = solve_p1("data/day10_example.txt").unwrap();
        assert_eq!(result_example, 36);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day10.txt").unwrap();
        assert_eq!(result, 1686);

        let result_example = solve_p2("data/day10_example.txt").unwrap();
        assert_eq!(result_example, 81);
    }
} 