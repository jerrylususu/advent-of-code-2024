use std::collections::HashSet;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

type OrderSet = HashSet<(i32, i32)>;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn get_middle_of_list(list: &[i32]) -> Result<i32, Box<dyn Error>> {
    let n = list.len();
    if n % 2 == 0 {
        return Err("List length must be odd".into());
    }
    Ok(list[(n - 1) / 2])
}

fn list_is_in_order(list: &[i32], order_set: &OrderSet) -> (bool, Option<(usize, usize)>) {
    let n = list.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if order_set.contains(&(list[j], list[i])) {
                return (false, Some((i, j)));
            }
        }
    }
    (true, None)
}

fn swap_item_in_list(list: &mut Vec<i32>, i: usize, j: usize) {
    list.swap(i, j);
}

fn build_order_set_and_lists(lines: Vec<String>) -> Result<(OrderSet, Vec<Vec<i32>>), Box<dyn Error>> {
    let mut order_set = OrderSet::new();
    let mut lists = Vec::new();

    for line in lines {
        if line.contains('|') {
            let parts: Vec<&str> = line.split('|').collect();
            let a: i32 = parts[0].trim().parse()?;
            let b: i32 = parts[1].trim().parse()?;
            order_set.insert((a, b));
        } else if line.contains(',') {
            let list: Vec<i32> = line
                .split(',')
                .map(|x| x.trim().parse::<i32>())
                .collect::<Result<_, _>>()?;
            lists.push(list);
        }
    }

    Ok((order_set, lists))
}

fn solve_p1(path: &str) -> Result<i32, Box<dyn Error>> {
    let lines = read_file(path)?;
    let (order_set, lists) = build_order_set_and_lists(lines)?;
    let mut total = 0;

    for list in lists {
        if list_is_in_order(&list, &order_set).0 {
            total += get_middle_of_list(&list)?;
        }
    }

    Ok(total)
}

fn solve_p2(path: &str) -> Result<i32, Box<dyn Error>> {
    let lines = read_file(path)?;
    let (order_set, lists) = build_order_set_and_lists(lines)?;
    let mut total = 0;

    for mut list in lists {
        let (mut already_in_order, mut reverse_pair) = list_is_in_order(&list, &order_set);
        
        if already_in_order {
            continue;
        }

        while !already_in_order {
            if let Some((i, j)) = reverse_pair {
                swap_item_in_list(&mut list, i, j);
                let check = list_is_in_order(&list, &order_set);
                already_in_order = check.0;
                reverse_pair = check.1;
            }
        }

        total += get_middle_of_list(&list)?;
    }

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
        let result = solve_p1("data/day5.txt").unwrap();
        assert_eq!(result, 5391);

        let result_example = solve_p1("data/day5_example.txt").unwrap();
        assert_eq!(result_example, 143);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day5.txt").unwrap();
        assert_eq!(result, 6142);

        let result_example = solve_p2("data/day5_example.txt").unwrap();
        assert_eq!(result_example, 123);
    }
}
