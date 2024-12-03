use regex::Regex;
use std::error::Error;
use std::io::BufRead;
use std::{fs::File, io};

#[derive(Debug)]
struct MutItem {
    left: i64,
    right: i64,
    begin_index: usize,
}

#[derive(Debug)]
struct StatusItem {
    enabled: bool,
    begin_index: usize,
}

#[derive(Debug)]
enum Item {
    Mut(MutItem),
    Status(StatusItem),
}

fn read_file(path: &str) -> Result<Vec<Item>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);

    let mut_re = Regex::new(r"mul\((\d+),(\d+)\)")?;
    let do_re = Regex::new(r"do\(\)")?;
    let dont_re = Regex::new(r"don't\(\)")?;

    let mut lines: Vec<String> = Vec::new();

    for line in reader.lines() {
        let line = line?;
        lines.push(line);
    }

    let line = lines.join("");

    let mut items: Vec<Item> = Vec::new();

    for matched in mut_re.captures_iter(&line) {
        let left = matched
            .get(1)
            .ok_or("left not found")?
            .as_str()
            .parse::<i64>()?;
        let right = matched
            .get(2)
            .ok_or("left not found")?
            .as_str()
            .parse::<i64>()?;
        let whole = matched.get(0).ok_or("whole not found")?;
        items.push(Item::Mut(MutItem {
            left,
            right,
            begin_index: whole.start(),
        }));
    }

    for matched in do_re.find_iter(&line) {
        items.push(Item::Status(StatusItem {
            enabled: true,
            begin_index: matched.start(),
        }));
    }

    for matched in dont_re.find_iter(&line) {
        items.push(Item::Status(StatusItem {
            enabled: false,
            begin_index: matched.start(),
        }));
    }

    items.sort_by_key(|item| -> usize {
        match item {
            Item::Mut(mut_item) => mut_item.begin_index,
            Item::Status(status_item) => status_item.begin_index,
        }
    });

    Ok(items)
}

fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    let items = read_file(path)?;
    Ok(items
        .iter()
        .map(|item| -> i64 {
            match item {
                Item::Mut(mut_item) => mut_item.left * mut_item.right,
                Item::Status(_) => 0,
            }
        })
        .sum())
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let items = read_file(path)?;

    let mut mut_enabled = true;
    let mut sum: i64 = 0;

    for item in items {
        match item {
            Item::Mut(mut_item) => {
                if mut_enabled {
                    sum += mut_item.left * mut_item.right;
                }
            }
            Item::Status(StatusItem {
                enabled: true,
                begin_index: _,
            }) => {
                mut_enabled = true;
            }
            Item::Status(StatusItem {
                enabled: false,
                begin_index: _,
            }) => {
                mut_enabled = false;
            }
        }
    }

    Ok(sum)
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
        let result = solve_p1("data/day3.txt").unwrap();
        assert_eq!(result, 191183308);

        let result_example = solve_p1("data/day3_example.txt").unwrap();
        assert_eq!(result_example, 161);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day3.txt").unwrap();
        assert_eq!(result, 92082041);

        let result_example = solve_p2("data/day3_example.txt").unwrap();
        assert_eq!(result_example, 48);
    }
}
