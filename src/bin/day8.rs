use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};
use itertools::Itertools;

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Pos {
    x: i32,
    y: i32,
}

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_grid(lines: Vec<String>) -> (Vec<Vec<char>>, HashMap<char, Vec<Pos>>) {
    let grid: Vec<Vec<char>> = lines.iter()
        .map(|line| line.chars().collect())
        .collect();
    
    let n_row = grid.len() as i32;
    let n_col = grid[0].len() as i32;
    let mut antanna_map = HashMap::new();

    for i in 0..n_row {
        for j in 0..n_col {
            let c = grid[i as usize][j as usize];
            if c == '.' {
                continue;
            }
            antanna_map.entry(c)
                .or_insert_with(Vec::new)
                .push(Pos{x: i, y: j});
        }
    }

    (grid, antanna_map)
}

fn in_grid(pos: &Pos, n_row: i32, n_col: i32) -> bool {
    pos.x >= 0 && pos.x < n_row && pos.y >= 0 && pos.y < n_col
}

fn gcd(mut a: i32, mut b: i32) -> i32 {
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    a
}

fn solve_p1(path: &str) -> Result<usize, Box<dyn Error>> {
    let lines = read_file(path)?;
    let (grid, antanna_map) = parse_grid(lines);
    let n_row = grid.len() as i32;
    let n_col = grid[0].len() as i32;
    
    let mut antinode_set = HashSet::new();

    for antanna_pos_list in antanna_map.values() {
        for (pos1, pos2) in antanna_pos_list.iter().tuple_combinations() {
            let dist_vector = Pos{x:pos2.x - pos1.x, y:pos2.y - pos1.y};
            
            // after a2
            let antinode_2 = Pos{x: pos2.x + dist_vector.x, y: pos2.y + dist_vector.y};
            if in_grid(&antinode_2, n_row, n_col) {
                antinode_set.insert(antinode_2);
            }

            // before a1
            let antinode_1 = Pos{x: pos1.x - dist_vector.x, y: pos1.y - dist_vector.y};
            if in_grid(&antinode_1, n_row, n_col) {
                antinode_set.insert(antinode_1);
            }
        }
    }

    Ok(antinode_set.len())
}

fn solve_p2(path: &str) -> Result<usize, Box<dyn Error>> {
    let lines = read_file(path)?;
    let (grid, antanna_map) = parse_grid(lines);
    let n_row = grid.len() as i32;
    let n_col = grid[0].len() as i32;
    
    let mut antinode_set = HashSet::new();

    for antanna_pos_list in antanna_map.values() {
        for (pos1, pos2) in antanna_pos_list.iter().tuple_combinations() {
            let dx = pos2.x - pos1.x;
            let dy = pos2.y - pos1.y;
            let g = gcd(dx, dy);
            let dist_vector = Pos{x: dx / g, y: dy / g};

            // a1->a2
            let mut current_pos = *pos2;
            while in_grid(&current_pos, n_row, n_col) {
                antinode_set.insert(current_pos);
                current_pos = Pos{x: current_pos.x + dist_vector.x, y: current_pos.y + dist_vector.y};
            }

            // a2->a1
            let mut current_pos = *pos1;
            while in_grid(&current_pos, n_row, n_col) {
                antinode_set.insert(current_pos);
                current_pos = Pos{x: current_pos.x - dist_vector.x, y: current_pos.y - dist_vector.y};
            }
        }
    }

    Ok(antinode_set.len())
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
        let result = solve_p1("data/day8.txt").unwrap();
        assert_eq!(result, 398);

        let result_example = solve_p1("data/day8_example.txt").unwrap();
        assert_eq!(result_example, 14);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day8.txt").unwrap();
        assert_eq!(result, 1333);

        let result_example = solve_p2("data/day8_example.txt").unwrap();
        assert_eq!(result_example, 34);
    }
} 