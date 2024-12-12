use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    Left,
    Right,
    Up,
    Down,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Side {
    direction: Direction,
    row_or_col_1: i32,
    row_or_col_2: i32,
    locate_col_or_row: i32,
}

type TypeWithId = (char, i32);
type Point = (i32, i32);

struct Grid {
    data: Vec<Vec<char>>,
    n_row: i32,
    n_col: i32,
}

impl Grid {
    fn new(lines: Vec<String>) -> Self {
        let data: Vec<Vec<char>> = lines.iter()
            .map(|line| line.chars().collect())
            .collect();
        let n_row = data.len() as i32;
        let n_col = data[0].len() as i32;
        Grid { data, n_row, n_col }
    }

    fn in_grid(&self, x: i32, y: i32) -> bool {
        x >= 0 && x < self.n_row && y >= 0 && y < self.n_col
    }

    fn get(&self, x: i32, y: i32) -> char {
        self.data[x as usize][y as usize]
    }
}

fn flood_fill(grid: &Grid, visited: &mut Vec<Vec<bool>>, type_count_map: &mut HashMap<char, i32>) 
    -> HashMap<TypeWithId, Vec<Point>> {
    let mut type_with_id_to_points = HashMap::new();

    for x in 0..grid.n_row {
        for y in 0..grid.n_col {
            if !visited[x as usize][y as usize] {
                let current_type = grid.get(x, y);
                let count = type_count_map.entry(current_type).or_insert(0);
                *count += 1;
                let type_with_id = (current_type, *count);

                let mut points = Vec::new();
                let mut queue = VecDeque::new();
                queue.push_back((x, y));

                while let Some((cx, cy)) = queue.pop_front() {
                    if visited[cx as usize][cy as usize] {
                        continue;
                    }
                    visited[cx as usize][cy as usize] = true;
                    points.push((cx, cy));

                    for (nx, ny, _) in get_neighbours(cx, cy) {
                        if !grid.in_grid(nx, ny) {
                            continue;
                        }
                        if !visited[nx as usize][ny as usize] && grid.get(nx, ny) == current_type {
                            queue.push_back((nx, ny));
                        }
                    }
                }

                type_with_id_to_points.insert(type_with_id, points);
            }
        }
    }

    type_with_id_to_points
}

fn get_neighbours(x: i32, y: i32) -> Vec<(i32, i32, Direction)> {
    vec![
        (x, y - 1, Direction::Left),
        (x, y + 1, Direction::Right),
        (x - 1, y, Direction::Up),
        (x + 1, y, Direction::Down),
    ]
}

fn build_side(direction: Direction, row_or_col_1: i32, row_or_col_2: i32, locate_col_or_row: i32) -> Side {
    let lesser = row_or_col_1.min(row_or_col_2);
    let greater = row_or_col_1.max(row_or_col_2);
    Side {
        direction,
        row_or_col_1: lesser,
        row_or_col_2: greater,
        locate_col_or_row,
    }
}

fn count_continuous_ranges(nums: &[i32]) -> i32 {
    if nums.is_empty() {
        return 0;
    }
    
    let mut count = 1;
    for i in 1..nums.len() {
        if nums[i] != nums[i-1] + 1 {
            count += 1;
        }
    }
    count
}

fn merge_sides(side_set: &HashSet<Side>) -> i32 {
    let mut side_map: HashMap<(Direction, i32, i32), Vec<i32>> = HashMap::new();
    
    for side in side_set {
        let key = (side.direction, side.row_or_col_1, side.row_or_col_2);
        side_map.entry(key)
            .or_default()
            .push(side.locate_col_or_row);
    }

    let mut total = 0;
    for (_, mut values) in side_map {
        values.sort_unstable();
        total += count_continuous_ranges(&values);
    }
    
    total
}

fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let grid = Grid::new(lines);
    
    let mut visited = vec![vec![false; grid.n_col as usize]; grid.n_row as usize];
    let mut type_count_map = HashMap::new();
    
    let type_with_id_to_points = flood_fill(&grid, &mut visited, &mut type_count_map);
    let mut total_cost = 0;

    for (type_with_id, points) in type_with_id_to_points.iter() {
        let area = points.len();
        let mut perimeter = 0;

        for &(x, y) in points {
            for (nx, ny, _) in get_neighbours(x, y) {
                if !grid.in_grid(nx, ny) || grid.get(nx, ny) != type_with_id.0 {
                    perimeter += 1;
                }
            }
        }

        total_cost += (perimeter * area) as i64;
    }

    Ok(total_cost)
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let grid = Grid::new(lines);
    
    let mut visited = vec![vec![false; grid.n_col as usize]; grid.n_row as usize];
    let mut type_count_map = HashMap::new();
    
    let type_with_id_to_points = flood_fill(&grid, &mut visited, &mut type_count_map);
    let mut total_cost = 0;

    for (type_with_id, points) in type_with_id_to_points.iter() {
        let mut side_set = HashSet::new();
        
        for &(row, col) in points {
            for (i_row, i_col, direction) in get_neighbours(row, col) {
                if grid.in_grid(i_row, i_col) && grid.get(i_row, i_col) == type_with_id.0 {
                    continue;
                }

                let side = match direction {
                    Direction::Left | Direction::Right => 
                        build_side(direction, col, i_col, row),
                    Direction::Up | Direction::Down => 
                        build_side(direction, row, i_row, col),
                };
                side_set.insert(side);
            }
        }

        let area = points.len() as i64;
        let side_count = merge_sides(&side_set) as i64;
        total_cost += area * side_count;
    }

    Ok(total_cost)
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
        let result = solve_p1("data/day12.txt").unwrap();
        assert_eq!(result, 1437300);

        let result_example = solve_p1("data/day12_example.txt").unwrap();
        assert_eq!(result_example, 1930);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day12.txt").unwrap();
        assert_eq!(result, 849332);

        let result_example = solve_p2("data/day12_example.txt").unwrap();
        assert_eq!(result_example, 1206);
    }
} 