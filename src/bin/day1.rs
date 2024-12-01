use std::collections::HashMap;
use std::collections::hash_map::Entry::{Occupied, Vacant};
use std::error::Error;
use std::io::BufRead;
use std::{fs::File, io};

fn read_file_to_lr(input_path: &str) -> Result<(Vec<u64>, Vec<u64>), Box<dyn Error>> {
    let mut lefts: Vec<u64> = Vec::new();
    let mut rights: Vec<u64> = Vec::new();

    let file = File::open(input_path)?;
    let reader = io::BufReader::new(file);

    for line in reader.lines() {
        let line = match line {
            Ok(line) => line,
            Err(e) => {
                println!("Error reading line: {}", e);
                return Err(e.into());
            }
        };

        let numbers: Vec<u64> = line
            .split_whitespace()
            .map(|s| {
                s.parse::<u64>().map_err(|e| -> Box<dyn Error> {
                    println!("Error parsing number: {}", e);
                    e.into()
                })
            })
            .collect::<Result<Vec<u64>, Box<dyn Error>>>()?;

        lefts.push(numbers[0]);
        rights.push(numbers[1]);
    }

    Ok((lefts, rights))
}

fn u64_diff_abs(a: u64, b: u64) -> u64 {
    if a > b {
        a - b
    } else {
        b - a
    }
}

fn solve_p1(input_path: &str) -> Result<u64, Box<dyn Error>> {
    let (mut lefts, mut rights) = read_file_to_lr(input_path)?;
    
    lefts.sort();
    rights.sort();

    let total: u64 = lefts.iter().zip(rights.iter())
        .map(|(l, r)| u64_diff_abs(*l, *r))
        .sum();

    Ok(total)
}

fn solve_p2(input_path: &str) -> Result<u64, Box<dyn Error>> {
    let (lefts, rights) = read_file_to_lr(input_path)?;

    let mut right_counter: HashMap<u64, u64> = HashMap::new();
    for num in rights {
        let entry = right_counter.entry(num);
        match entry {
            Occupied(mut entry) => {
                entry.insert(entry.get() + 1);
            },
            Vacant(entry) => {
                entry.insert(1);
            },
        }
    }

    let total: u64 = lefts.iter()
        .map(|l| l * right_counter.get(l).unwrap_or(&0))
        .sum();

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
        let result = solve_p1("data/day1.txt").unwrap();
        assert_eq!(result, 1388114);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day1.txt").unwrap();
        assert_eq!(result, 23529853);
    }
}