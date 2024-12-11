use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_input(path: &str) -> Result<Vec<i64>, Box<dyn Error>> {
    let lines = read_file(path)?;
    let values: Vec<i64> = lines[0]
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();
    Ok(values)
}

fn get_next_state(value: i64) -> Vec<i64> {
    if value == 0 {
        return vec![1];
    }
    if value.to_string().len() % 2 == 0 {
        let s = value.to_string();
        let mid = s.len() / 2;
        let left: i64 = s[..mid].parse().unwrap();
        let right: i64 = s[mid..].parse().unwrap();
        return vec![left, right];
    }
    vec![value * 2024]
}

fn solve_recursive(value: i64, remaining_step: i32, memo: &mut HashMap<(i64, i32), i64>) -> i64 {
    if remaining_step == 0 {
        return 1;
    }
    
    if let Some(&count) = memo.get(&(value, remaining_step)) {
        return count;
    }

    let next_values = get_next_state(value);
    let count = next_values.iter()
        .map(|&next_value| solve_recursive(next_value, remaining_step - 1, memo))
        .sum();
    
    memo.insert((value, remaining_step), count);
    count
}

fn solve(path: &str, steps: i32) -> Result<i64, Box<dyn Error>> {
    let values = parse_input(path)?;
    let mut memo = HashMap::new();
    
    let total: i64 = values.iter()
        .map(|&v| solve_recursive(v, steps, &mut memo))
        .sum();
    
    Ok(total)
}

fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    solve(path, 25)
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    solve(path, 75)
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
        let result = solve_p1("data/day11.txt").unwrap();
        assert_eq!(result, 216996);

        let result_example = solve_p1("data/day11_example.txt").unwrap();
        assert_eq!(result_example, 55312);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day11.txt").unwrap();
        assert_eq!(result, 257335372288947);
    }
} 