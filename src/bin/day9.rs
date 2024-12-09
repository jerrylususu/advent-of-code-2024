use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

#[derive(Debug, Clone, Copy, PartialEq)]
enum Entry {
    EmptySpace,
    File,
}

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_input(path: &str) -> Result<Vec<i32>, Box<dyn Error>> {
    let lines = read_file(path)?;
    let line = lines.join("").trim().to_string();
    Ok(line.chars()
        .map(|c| c.to_digit(10).unwrap() as i32)
        .collect())
}

fn calc_hash(arr: &[Option<i32>]) -> i64 {
    arr.iter()
        .enumerate()
        .filter_map(|(idx, &value)| value.map(|v| v as i64 * idx as i64))
        .sum()
}

fn initialize_data(files: &[i32]) -> (Vec<Option<i32>>, Vec<FileInfo>, Vec<EmptySpace>) {
    let mut arr = vec![None; files.iter().sum::<i32>() as usize];
    let mut pos = 0;
    let mut file_id = 0;
    let mut state = Entry::File;
    let mut file_infos = Vec::new();
    let mut empty_spaces = Vec::new();

    for &length in files {
        match state {
            Entry::File => {
                for i in pos..pos+length {
                    arr[i as usize] = Some(file_id);
                }
                file_infos.push(FileInfo {
                    begin: pos,
                    length,
                });
                pos += length;
                state = Entry::EmptySpace;
                file_id += 1;
            }
            Entry::EmptySpace => {
                empty_spaces.push(EmptySpace {
                    length,
                    begin: pos,
                });
                pos += length;
                state = Entry::File;
            }
        }
    }

    (arr, file_infos, empty_spaces)
}

fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    let files = parse_input(path)?;
    let (mut arr, _, _) = initialize_data(&files);

    let mut last_first_empty_idx = None;
    let mut last_last_occupied_idx = None;

    loop {
        let first_empty_idx = (last_first_empty_idx.unwrap_or(0)..arr.len())
            .find(|&i| arr[i].is_none());
        
        let last_occupied_idx = (0..=last_last_occupied_idx.unwrap_or(arr.len()-1))
            .rev()
            .find(|&i| arr[i].is_some());

        match (first_empty_idx, last_occupied_idx) {
            (Some(empty), Some(occupied)) if empty < occupied => {
                arr.swap(empty, occupied);
                last_first_empty_idx = Some(empty);
                last_last_occupied_idx = Some(occupied);
            }
            _ => break
        }
    }

    Ok(calc_hash(&arr))
}

#[derive(Debug, Clone)]
struct FileInfo {
    begin: i32,
    length: i32,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct EmptySpace {
    begin: i32,
    length: i32,
}

fn swap_range(arr: &mut [Option<i32>], src_begin: usize, target_begin: usize, length: usize) {
    let mut tmp = vec![None; length];
    tmp.copy_from_slice(&arr[target_begin..target_begin + length]);
    arr.copy_within(src_begin..src_begin + length, target_begin);
    arr[src_begin..src_begin + length].copy_from_slice(&tmp);
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let files = parse_input(path)?;
    let (mut arr, file_infos, mut empty_spaces) = initialize_data(&files);

    empty_spaces.sort();

    for file_info in file_infos.iter().rev() {
        if let Some(empty_pos) = empty_spaces.iter()
            .position(|space| space.length >= file_info.length && space.begin < file_info.begin)
        {
            let empty_space = empty_spaces.remove(empty_pos);
            let src_begin = file_info.begin as usize;
            let target_begin = empty_space.begin as usize;
            let length = file_info.length as usize;

            swap_range(&mut arr, src_begin, target_begin, length);

            let remaining_length = empty_space.length - file_info.length;
            if remaining_length > 0 {
                empty_spaces.push(EmptySpace {
                    length: remaining_length,
                    begin: empty_space.begin + file_info.length,
                });
                empty_spaces.sort();
            }
        }
    }

    Ok(calc_hash(&arr))
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
        let result = solve_p1("data/day9.txt").unwrap();
        assert_eq!(result, 6356833654075);

        let result_example = solve_p1("data/day9_example.txt").unwrap();
        assert_eq!(result_example, 1928);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day9.txt").unwrap();
        assert_eq!(result, 6389911791746);

        let result_example = solve_p2("data/day9_example.txt").unwrap();
        assert_eq!(result_example, 2858);
    }
} 