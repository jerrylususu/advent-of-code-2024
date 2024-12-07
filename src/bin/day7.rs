use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use rayon::prelude::*;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_lines(lines: Vec<String>) -> Result<Vec<(i64, Vec<i64>)>, Box<dyn Error>> {
    lines
        .into_iter()
        .map(|line| {
            let parts: Vec<&str> = line.split(':').collect();
            let target: i64 = parts[0].trim().parse()?;
            let values: Vec<i64> = parts[1]
                .split_whitespace()
                .map(|s| s.parse::<i64>())
                .collect::<Result<_, _>>()?;
            Ok((target, values))
        })
        .collect()
}


#[derive(Debug, Clone, Copy, PartialEq)]
enum Op {
    Add,
    Multiply,
    Concat,
}

fn eval_expr(expr: &[i64], ops: &[Op], early_break: Option<i64>) -> Option<i64> {
    if expr.len() == 1 {
        return Some(expr[0]);
    }
    
    let (op1, op2) = (expr[0], expr[1]);
    if let Some(break_val) = early_break {
        if op1 > break_val {
            return None;
        }
    }
    
    let res = match ops[0] {
        Op::Add => op1 + op2,
        Op::Multiply => op1 * op2,
        Op::Concat => {
            format!("{}{}", op1, op2).parse::<i64>().unwrap()
        }
    };
    
    let mut new_expr = vec![res];
    new_expr.extend_from_slice(&expr[2..]);
    let new_ops = &ops[1..];
    
    eval_expr(&new_expr, new_ops, early_break)
}

fn make_expr_ops(n_space: usize, supported_ops: &[Op]) -> Vec<Vec<Op>> {
    let mut result = Vec::new();
    
    fn generate(current: Vec<Op>, remaining: usize, supported_ops: &[Op], result: &mut Vec<Vec<Op>>) {
        if remaining == 0 {
            result.push(current);
            return;
        }
        for &op in supported_ops {
            let mut new_current = current.clone();
            new_current.push(op);
            generate(new_current, remaining - 1, supported_ops, result);
        }
    }
    
    generate(Vec::new(), n_space, supported_ops, &mut result);
    result
}


fn solve_p1(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let parsed_lines = parse_lines(lines)?;
    let mut total = 0;
    
    let supported_ops = [Op::Add, Op::Multiply];
    
    for (target, values) in parsed_lines {
        let n_space = values.len() - 1;
        let all_ops = make_expr_ops(n_space, &supported_ops);
        
        for ops in all_ops {
            if let Some(result) = eval_expr(&values, &ops, None) {
                if result == target {
                    total += target;
                    break;
                }
            }
        }
    }
    
    Ok(total)
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let parsed_lines = parse_lines(lines)?;
    
    let total: i64 = parsed_lines
        .par_iter()
        .enumerate()
        .map(|(i, (target, values))| {
            println!("at {}", i);
            
            let n_space = values.len() - 1;
            let all_ops = make_expr_ops(n_space, &[Op::Add, Op::Multiply, Op::Concat]);
            
            for ops in all_ops {
                if let Some(result) = eval_expr(values, &ops, Some(*target)) {
                    if result == *target {
                        return *target;
                    }
                }
            }
            0
        })
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
        let result = solve_p1("data/day7.txt").unwrap();
        assert_eq!(result, 2941973819040);

        let result_example = solve_p1("data/day7_example.txt").unwrap();
        assert_eq!(result_example, 3749);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day7.txt").unwrap();
        assert_eq!(result, 249943041417600);   

        let result_example = solve_p2("data/day7_example.txt").unwrap();
        assert_eq!(result_example, 11387);
    }
} 