use std::error::Error;
use std::io::BufRead;
use std::{fs::File, io};

fn read_file(path: &str) -> Result<Vec<Vec<i64>>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);

    let mut result: Vec<Vec<i64>> = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let arr = line
            .split_whitespace()
            .map(|s| s.parse::<i64>().map_err(|e| e.into()))
            .collect::<Result<Vec<i64>, Box<dyn Error>>>()?;
        result.push(arr);
    }

    Ok(result)
}

fn check_arr(arr: &Vec<i64>) -> bool {
    #[derive(Clone, Copy, PartialEq, Eq)]
    enum Direction {
        Up,
        Down,
    }

    let mut last_direction: Option<Direction> = None;

    for i in 0..arr.len() - 1 {
        let a1 = arr[i];
        let a2 = arr[i + 1];

        let diff = a1 - a2;
        let diff_abs = diff.abs();
        if diff_abs < 1 || diff_abs > 3 {
            return false;
        }

        let direction = if a1 > a2 {
            Direction::Up
        } else {
            Direction::Down
        };

        match last_direction {
            None => last_direction = Some(direction),
            Some(last_direction) => {
                if last_direction != direction {
                    return false;
                }
            }
        };
    }

    true
}

fn solve_p1(input_path: &str) -> Result<usize, Box<dyn Error>> {
    let arrs = read_file(input_path)?;

    Ok(arrs.iter().filter(|arr| check_arr(arr)).count())
}

fn check_arr_with_skip_idx(arr: &Vec<i64>) -> bool {
    if check_arr(arr) {
        return true;
    }

    for i in 0..arr.len() {
        let mut arr_copy = arr.clone();
        arr_copy.remove(i);
        if check_arr(&arr_copy) {
            return true;
        }
    }

    false
}

fn solve_p2(input_path: &str) -> Result<usize, Box<dyn Error>> {
    let arrs = read_file(input_path)?;
    Ok(arrs
        .iter()
        .filter(|arr| check_arr_with_skip_idx(arr))
        .count())
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
        let result = solve_p1("data/day2.txt").unwrap();
        assert_eq!(result, 591);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day2.txt").unwrap();
        assert_eq!(result, 621);
    }
}
