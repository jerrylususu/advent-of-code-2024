use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::{HashSet, VecDeque};

type Position = (i32, i32);

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_input(path: &str) -> Result<Vec<Position>, Box<dyn Error>> {
    let lines = read_file(path)?;
    let mut pos_list = Vec::new();
    
    for line in lines {
        let parts: Vec<&str> = line.trim().split(',').collect();
        if parts.len() >= 2 {
            let col = parts[0].parse::<i32>()?;
            let row = parts[1].parse::<i32>()?;
            pos_list.push((col, row));
        }
    }
    
    Ok(pos_list)
}

fn get_next_positions(pos: Position) -> Vec<Position> {
    let (col, row) = pos;
    vec![
        (col + 1, row),
        (col - 1, row),
        (col, row + 1),
        (col, row - 1),
    ]
}

fn is_valid_position(pos: Position, side_len: i32, obstacles: &HashSet<Position>) -> bool {
    let (col, row) = pos;
    if !(0..side_len).contains(&col) || !(0..side_len).contains(&row) {
        return false;
    }
    !obstacles.contains(&pos)
}

fn bfs(
    start_pos: Position,
    end_pos: Position,
    side_len: i32,
    obstacles: &HashSet<Position>,
) -> Option<Vec<Position>> {
    let mut queue = VecDeque::new();
    let mut visited = HashSet::new();
    queue.push_back((start_pos, vec![start_pos]));

    while let Some((pos, path)) = queue.pop_front() {
        if visited.contains(&pos) {
            continue;
        }
        visited.insert(pos);

        if pos == end_pos {
            return Some(path);
        }

        for next_pos in get_next_positions(pos) {
            if is_valid_position(next_pos, side_len, obstacles) {
                let mut new_path = path.clone();
                new_path.push(next_pos);
                queue.push_back((next_pos, new_path));
            }
        }
    }
    None
}

fn solve_p1(path: &str, side_len: i32, stop_at: usize) -> Result<usize, Box<dyn Error>> {
    let pos_list = parse_input(path)?;
    let start_pos = (0, 0);
    let end_pos = (side_len - 1, side_len - 1);

    let obstacles: HashSet<Position> = pos_list.iter()
        .take(stop_at)
        .copied()
        .collect();

    if let Some(path) = bfs(start_pos, end_pos, side_len, &obstacles) {
        Ok(path.len() - 1)
    } else {
        Err("No path found".into())
    }
}

fn solve_p2(path: &str, side_len: i32) -> Result<String, Box<dyn Error>> {
    let pos_list = parse_input(path)?;
    let start_pos = (0, 0);
    let end_pos = (side_len - 1, side_len - 1);

    let mut left = 0;
    let mut right = pos_list.len() - 1;
    let mut result = None;

    while left <= right {
        let mid = (left + right) / 2;
        let obstacles: HashSet<Position> = pos_list.iter()
            .take(mid + 1)
            .copied()
            .collect();

        if bfs(start_pos, end_pos, side_len, &obstacles).is_some() {
            left = mid + 1;
        } else {
            result = Some(mid);
            right = mid - 1;
        }
    }

    if let Some(index) = result {
        Ok(format!("{},{}", pos_list[index].0, pos_list[index].1))
    } else {
        Err("No solution found".into())
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let result_p1 = solve_p1("input.txt", 71, 1024)?;
    println!("Part 1: {}", result_p1);

    let result_p2 = solve_p2("input.txt", 71)?;
    println!("Part 2: {}", result_p2);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_p1() {
        let result = solve_p1("data/day18.txt", 71, 1024).unwrap();
        assert_eq!(result, 226);

        let result_example = solve_p1("data/day18_example.txt", 7, 12).unwrap();
        assert_eq!(result_example, 22);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day18.txt", 71).unwrap();
        assert_eq!(result, "60,46");

        let result_example = solve_p2("data/day18_example.txt", 7).unwrap();
        assert_eq!(result_example, "6,1");
    }
} 