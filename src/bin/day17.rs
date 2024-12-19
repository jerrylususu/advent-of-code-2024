use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};

#[derive(Debug)]
struct VMState {
    reg_a: i64,
    reg_b: i64,
    reg_c: i64,
    pc: usize,
}

impl VMState {
    fn new(reg_a: i64, reg_b: i64, reg_c: i64) -> Self {
        Self {
            reg_a,
            reg_b,
            reg_c,
            pc: 0,
        }
    }
}

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_input(path: &str) -> Result<(i64, i64, i64, Vec<i64>), Box<dyn Error>> {
    let lines = read_file(path)?;
    let mut reg_a = 0;
    let mut reg_b = 0;
    let mut reg_c = 0;
    let mut program = Vec::new();

    for line in lines {
        if line.starts_with("Register A") {
            reg_a = line.split(':').nth(1).unwrap().trim().parse()?;
        } else if line.starts_with("Register B") {
            reg_b = line.split(':').nth(1).unwrap().trim().parse()?;
        } else if line.starts_with("Register C") {
            reg_c = line.split(':').nth(1).unwrap().trim().parse()?;
        } else if line.starts_with("Program") {
            program = line.split(':')
                .nth(1)
                .unwrap()
                .trim()
                .split(',')
                .map(|x| x.trim().parse())
                .collect::<Result<Vec<i64>, _>>()?;
        }
    }

    Ok((reg_a, reg_b, reg_c, program))
}

fn get_combo_operand(vm_state: &VMState, operand: i64) -> i64 {
    match operand {
        0..=3 => operand,
        4 => vm_state.reg_a,
        5 => vm_state.reg_b,
        6 => vm_state.reg_c,
        _ => panic!("Invalid operand"),
    }
}

fn run_program(program: &[i64], reg_a: i64, reg_b: i64, reg_c: i64, max_iter: usize) -> Vec<i64> {
    let mut vm_state = VMState::new(reg_a, reg_b, reg_c);
    let mut output = Vec::new();

    for _ in 0..max_iter {
        if vm_state.pc >= program.len() {
            break;
        }

        let opcode = program[vm_state.pc];
        let operand = program[vm_state.pc + 1];

        match opcode {
            0 => {
                // adv, combo
                let denominator = 2_i64.pow(get_combo_operand(&vm_state, operand) as u32);
                vm_state.reg_a /= denominator;
                vm_state.pc += 2;
            }
            1 => {
                // bxl, literal
                vm_state.reg_b ^= operand;
                vm_state.pc += 2;
            }
            2 => {
                // bst, combo
                vm_state.reg_b = get_combo_operand(&vm_state, operand) % 8;
                vm_state.pc += 2;
            }
            3 => {
                // jnz
                if vm_state.reg_a == 0 {
                    vm_state.pc += 2;
                } else {
                    vm_state.pc = operand as usize;
                }
            }
            4 => {
                // bxc
                vm_state.reg_b ^= vm_state.reg_c;
                vm_state.pc += 2;
            }
            5 => {
                // out, combo
                output.push(get_combo_operand(&vm_state, operand) % 8);
                vm_state.pc += 2;
            }
            6 => {
                // bdv combo
                let denominator = 2_i64.pow(get_combo_operand(&vm_state, operand) as u32);
                vm_state.reg_b = vm_state.reg_a / denominator;
                vm_state.pc += 2;
            }
            7 => {
                // cdv combo
                let denominator = 2_i64.pow(get_combo_operand(&vm_state, operand) as u32);
                vm_state.reg_c = vm_state.reg_a / denominator;
                vm_state.pc += 2;
            }
            _ => panic!("Invalid opcode"),
        }
    }

    output
}

fn solve_p1(path: &str) -> Result<String, Box<dyn Error>> {
    let (reg_a, reg_b, reg_c, program) = parse_input(path)?;
    let output = run_program(&program, reg_a, reg_b, reg_c, 1000);
    Ok(output.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(","))
}

fn check_backward_until_index(target_index: usize, program: &[i64], output: &[i64]) -> bool {
    for i in (target_index..program.len()).rev() {
        if i >= output.len() || program[i] != output[i] {
            return false;
        }
    }
    true
}

fn recursive_check(
    program: &[i64],
    reg_b: i64,
    reg_c: i64,
    lower_limit: i64,
    upper_limit: i64,
    index: i32,
    all_founds: &mut Vec<i64>,
) -> Option<(i64, i64)> {

    if index == -1 {
        return Some((lower_limit, upper_limit));
    }

    if upper_limit - lower_limit < 10000 {
        for i in lower_limit..upper_limit {
            let output = run_program(program, i, reg_b, reg_c, 100000);
            if output == program {
                all_founds.push(i);
                break;
            }
        }
        return None;
    }

    let precision = 12;
    let seg_count = 2_i64.pow(precision);
    let range_len = upper_limit - lower_limit;
    let range_len_div_by_seg_count = range_len / seg_count;

    let mut hit_indices = Vec::new();

    for j in 0..=seg_count {
        let new_reg_a = lower_limit + range_len_div_by_seg_count * j;
        let output = run_program(program, new_reg_a, reg_b, reg_c, 100000);

        if check_backward_until_index(index as usize, program, &output) {
            hit_indices.push(j);
        }
    }

    if hit_indices.is_empty() {
        return None;
    }

    let mut consecutive_ranges = Vec::new();
    let mut i = 0;
    while i < hit_indices.len() {
        let start_idx = i;
        while i + 1 < hit_indices.len() && hit_indices[i + 1] == hit_indices[i] + 1 {
            i += 1;
        }
        consecutive_ranges.push((start_idx, i));
        i += 1;
    }

    println!(
        "finish {} {} {} ranges {:?}",
        lower_limit, upper_limit, index, consecutive_ranges
    );

    for (start, end) in consecutive_ranges {
        let new_lower = lower_limit + range_len_div_by_seg_count * hit_indices[start];
        let new_upper = lower_limit + range_len_div_by_seg_count * hit_indices[end];

        if let Some(result) = recursive_check(
            program,
            reg_b,
            reg_c,
            new_lower,
            new_upper,
            index - 1,
            all_founds,
        ) {
            return Some(result);
        }
    }

    None
}

fn solve_p2(path: &str) -> Result<i64, Box<dyn Error>> {
    let (_, reg_b, reg_c, program) = parse_input(path)?;
    
    let lower_limit = 2_i64.pow(45);
    let upper_limit = 2_i64.pow(48);
    
    let mut all_founds = Vec::new();
    recursive_check(
        &program,
        reg_b,
        reg_c,
        lower_limit,
        upper_limit,
        program.len() as i32 - 1,
        &mut all_founds,
    );

    if all_founds.is_empty() {
        Ok(-1)
    } else {
        Ok(*all_founds.iter().min().unwrap())
    }
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
        let result = solve_p1("data/day17.txt").unwrap();
        assert_eq!(result, "4,0,4,7,1,2,7,1,6");

        let result_example = solve_p1("data/day17_example.txt").unwrap();
        assert_eq!(result_example, "4,6,3,5,6,3,5,2,1,0");
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day17.txt").unwrap();
        assert_eq!(result, 202322348616234);
    }
} 