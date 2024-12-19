use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::HashSet;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_input(path: &str) -> Result<(Vec<String>, Vec<String>), Box<dyn Error>> {
    let lines = read_file(path)?;
    let mut words_list = Vec::new();
    let mut target_list = Vec::new();
    
    if let Some(first_line) = lines.first() {
        words_list = first_line.split(',')
            .map(|w| w.trim().to_string())
            .collect();
    }
    
    for line in lines.iter().skip(1) {
        if !line.trim().is_empty() {
            target_list.push(line.trim().to_string());
        }
    }
    
    Ok((words_list, target_list))
}

fn try_get_all_combination(
    target: &str, 
    words_list: &[String],
    known_uncomposable: &mut HashSet<String>,
    memo: &mut HashMap<String, usize>
) -> usize {
    if target.is_empty() {
        return 1;
    }
    
    if known_uncomposable.contains(target) {
        return 0;
    }
    
    if let Some(&count) = memo.get(target) {
        return count;
    }
    
    let mut sum_of_comb_count = 0;
    
    for word in words_list {
        if target.starts_with(word) {
            let remaining = &target[word.len()..];
            let comb_count = try_get_all_combination(
                remaining, 
                words_list,
                known_uncomposable,
                memo
            );
            if comb_count > 0 {
                sum_of_comb_count += comb_count;
            }
        }
    }
    
    if sum_of_comb_count == 0 {
        known_uncomposable.insert(target.to_string());
    }
    
    memo.insert(target.to_string(), sum_of_comb_count);
    sum_of_comb_count
}

fn solve_p1(path: &str) -> Result<usize, Box<dyn Error>> {
    let (words_list, target_list) = parse_input(path)?;
    let mut known_uncomposable = HashSet::new();
    let mut memo = HashMap::new();
    
    let mut can_compose_count = 0;
    for target in target_list {
        if try_get_all_combination(&target, &words_list, &mut known_uncomposable, &mut memo) > 0 {
            can_compose_count += 1;
        }
    }
    
    Ok(can_compose_count)
}

fn solve_p2(path: &str) -> Result<usize, Box<dyn Error>> {
    let (words_list, target_list) = parse_input(path)?;
    let mut known_uncomposable = HashSet::new();
    let mut memo = HashMap::new();
    
    let total_count: usize = target_list.iter()
        .map(|target| {
            try_get_all_combination(target, &words_list, &mut known_uncomposable, &mut memo)
        })
        .sum();
    
    Ok(total_count)
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
        let result = solve_p1("data/day19.txt").unwrap();
        assert_eq!(result, 290);

        let result_example = solve_p1("data/day19_example.txt").unwrap();
        assert_eq!(result_example, 6);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day19.txt").unwrap();
        assert_eq!(result, 712058625427487);

        let result_example = solve_p2("data/day19_example.txt").unwrap();
        assert_eq!(result_example, 16);
    }
} 