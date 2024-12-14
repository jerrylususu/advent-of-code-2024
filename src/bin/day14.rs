use std::fs;

#[derive(Debug)]
struct Robot {
    pos_row: i32,
    pos_col: i32, 
    vel_row: i32,
    vel_col: i32,
}

fn parse_line_to_robot(line: &str) -> Robot {
    let parts: Vec<&str> = line.split(" ").collect();
    let p_str = parts[0];
    let v_str = parts[1];
    
    let p_parts: Vec<&str> = p_str.split("=").nth(1).unwrap().split(",").collect();
    let v_parts: Vec<&str> = v_str.split("=").nth(1).unwrap().split(",").collect();
    
    Robot {
        pos_row: p_parts[1].parse().unwrap(),
        pos_col: p_parts[0].parse().unwrap(),
        vel_row: v_parts[1].parse().unwrap(),
        vel_col: v_parts[0].parse().unwrap(),
    }
}

fn get_quadrant_of_pos(pos_row: i32, pos_col: i32, n_row: i32, n_col: i32) -> Option<i32> {
    let middle_row = n_row / 2;
    let middle_col = n_col / 2;
    
    // 0 | 1
    // -----
    // 2 | 3
    
    if pos_row < middle_row && pos_col < middle_col {
        Some(0)
    } else if pos_row < middle_row && pos_col > middle_col {
        Some(1)
    } else if pos_row > middle_row && pos_col < middle_col {
        Some(2)
    } else if pos_row > middle_row && pos_col > middle_col {
        Some(3)
    } else {
        None
    }
}

fn solve_p1(path: &str, n_row: i32, n_col: i32, total_steps: i32) -> Result<i32, Box<dyn std::error::Error>> {
    let contents = fs::read_to_string(path)?;
    let lines: Vec<&str> = contents.lines().collect();
    
    let mut robots: Vec<Robot> = lines.iter()
        .map(|line| parse_line_to_robot(line))
        .collect();
        
    // 模拟移动
    for _ in 0..total_steps {
        for robot in robots.iter_mut() {
            robot.pos_row = (robot.pos_row + robot.vel_row).rem_euclid(n_row);
            robot.pos_col = (robot.pos_col + robot.vel_col).rem_euclid(n_col);
        }
    }
    
    let mut quad_count_map = vec![0; 4];
    
    for r in &robots {
        if let Some(quad) = get_quadrant_of_pos(r.pos_row, r.pos_col, n_row, n_col) {
            quad_count_map[quad as usize] += 1;
        }
    }
    
    Ok(quad_count_map.iter().fold(1, |acc, &count| acc * count))
}

fn main() {
    const N_ROW: i32 = 103;
    const N_COL: i32 = 101;
    const TOTAL_STEPS: i32 = 100;
    
    match solve_p1("data/day14.txt", N_ROW, N_COL, TOTAL_STEPS) {
        Ok(result) => {
            println!("Result: {}", result);
        },
        Err(e) => {
            eprintln!("Error: {}", e);
        }
    }

    // p2 is not applicable to solve programtically
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_p1() {
        let result = solve_p1(
            "data/day14.txt", 
            103, 
            101, 
            100
        ).unwrap();
        assert_eq!(result, 230436441);

        let result_example = solve_p1(
            "data/day14_example.txt",
            7,
            11,
            100
        ).unwrap();
        assert_eq!(result_example, 12);
    }
}