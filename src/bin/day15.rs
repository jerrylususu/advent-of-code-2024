use std::fs;
use std::collections::{HashSet, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq)]
enum Cell {
    Empty,
    Wall,
    Robot,
    BoxLeft,
    BoxRight,
    Box,
}

impl Cell {
    fn from_char(c: char) -> Cell {
        match c {
            '.' => Cell::Empty,
            '#' => Cell::Wall,
            '@' => Cell::Robot,
            '[' => Cell::BoxLeft,
            ']' => Cell::BoxRight,
            'O' => Cell::Box,
            _ => panic!("Invalid cell character: {}", c),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Pos {
    row: i32,
    col: i32,
}

impl Pos {
    fn new(row: i32, col: i32) -> Self {
        Self { row, col }
    }

    fn next_pos(&self, op: char) -> Self {
        match op {
            'v' => Self::new(self.row + 1, self.col),
            '^' => Self::new(self.row - 1, self.col),
            '>' => Self::new(self.row, self.col + 1),
            '<' => Self::new(self.row, self.col - 1),
            _ => panic!("Invalid operation: {}", op),
        }
    }
}

struct Grid {
    cells: Vec<Vec<Cell>>,
    n_row: i32,
    n_col: i32,
}

impl Grid {
    fn parse(contents: &str, part2: bool) -> (Self, Vec<char>) {
        let mut grid = Vec::new();
        let mut operations = Vec::new();
        
        for line in contents.lines() {
            let line = line.trim();
            if line.starts_with('#') && line.ends_with('#') {
                let row: Vec<Cell> = line[1..line.len()-1]
                    .chars()
                    .map(Cell::from_char)
                    .collect();
                grid.push(row);
            } else if !line.is_empty() {
                operations.extend(line.chars());
            }
        }
        
        grid = grid[1..grid.len()-1].to_vec();
        
        if part2 {
            let mut new_grid = Vec::new();
            for row in grid {
                let mut new_row = Vec::new();
                for cell in row {
                    match cell {
                        Cell::Robot => {
                            new_row.push(Cell::Robot);
                            new_row.push(Cell::Empty);
                        }
                        Cell::Wall => {
                            new_row.push(Cell::Wall);
                            new_row.push(Cell::Wall);
                        }
                        Cell::Box => {
                            new_row.push(Cell::BoxLeft);
                            new_row.push(Cell::BoxRight);
                        }
                        Cell::Empty => {
                            new_row.push(Cell::Empty);
                            new_row.push(Cell::Empty);
                        }
                        _ => panic!("Unexpected cell type during transform"),
                    }
                }
                new_grid.push(new_row);
            }
            grid = new_grid;
        }
        
        let n_row = grid.len() as i32;
        let n_col = grid[0].len() as i32;
        
        (Self { cells: grid, n_row, n_col }, operations)
    }

    fn get_robot_pos(&self) -> Pos {
        for row in 0..self.n_row {
            for col in 0..self.n_col {
                if self.cells[row as usize][col as usize] == Cell::Robot {
                    return Pos::new(row, col);
                }
            }
        }
        panic!("Robot not found");
    }

    fn in_bounds(&self, pos: Pos) -> bool {
        pos.row >= 0 && pos.row < self.n_row && pos.col >= 0 && pos.col < self.n_col
    }

    fn get(&self, pos: Pos) -> Cell {
        self.cells[pos.row as usize][pos.col as usize]
    }

    fn set(&mut self, pos: Pos, cell: Cell) {
        self.cells[pos.row as usize][pos.col as usize] = cell;
    }

    fn get_another_box_pos(&self, pos: Pos) -> Pos {
        match self.get(pos) {
            Cell::BoxLeft => Pos::new(pos.row, pos.col + 1),
            Cell::BoxRight => Pos::new(pos.row, pos.col - 1),
            _ => panic!("Not a box position"),
        }
    }

    fn find_connected_boxes(&self, robot_pos: Pos, direction: char) -> HashSet<Pos> {
        let mut visited = HashSet::new();
        let mut queue = VecDeque::new();
        queue.push_back(robot_pos);

        while let Some(pos) = queue.pop_front() {
            if visited.contains(&pos) {
                continue;
            }
            visited.insert(pos);

            let next_pos = pos.next_pos(direction);
            if self.in_bounds(next_pos) {
                match self.get(next_pos) {
                    Cell::BoxLeft | Cell::BoxRight => {
                        queue.push_back(next_pos);
                        queue.push_back(self.get_another_box_pos(next_pos));
                    }
                    Cell::Box => {
                        queue.push_back(next_pos);
                    }
                    _ => {}
                }
            }
        }
        visited
    }

    

    fn step(&mut self, robot_pos: Pos, operation: char) -> Pos {
        let next_pos = robot_pos.next_pos(operation);
        
        if !self.in_bounds(next_pos) {
            return robot_pos;
        }

        if self.get(next_pos) == Cell::Empty {
            self.set(robot_pos, Cell::Empty);
            self.set(next_pos, Cell::Robot);
            return next_pos;
        }

        // 检查是否可以推动箱子
        let connected_boxes = self.find_connected_boxes(robot_pos, operation);
        let next_positions: Vec<Pos> = connected_boxes.iter()
            .map(|&pos| pos.next_pos(operation))
            .collect();

        // 检查所有下一个位置是否可用
        let can_move = next_positions.iter().all(|&pos| {
            self.in_bounds(pos) && 
            (self.get(pos) == Cell::Empty || connected_boxes.contains(&pos))
        });

        if can_move {
            // 移动所有连接的箱子和机器人
            let grid_copy = self.cells.clone();
            
            // 先移动到新位置
            for (old_pos, new_pos) in connected_boxes.iter().zip(next_positions.iter()) {
                let cell = grid_copy[old_pos.row as usize][old_pos.col as usize];
                self.set(*new_pos, cell);
            }

            // 清理旧位置
            for old_pos in connected_boxes {
                if !next_positions.contains(&old_pos) {
                    self.set(old_pos, Cell::Empty);
                }
            }

            return next_pos;
        }

        robot_pos
    }

    fn calculate_score(&self, part2: bool) -> i32 {
        let mut sum = 0;
        for row in 0..self.n_row {
            for col in 0..self.n_col {
                let pos = Pos::new(row, col);
                match (self.get(pos), part2) {
                    (Cell::BoxLeft, true) => {
                        sum += (row + 1) * 100 + (col + 2);
                    }
                    (Cell::Box, false) => {
                        sum += (row + 1) * 100 + (col + 1);
                    }
                    _ => {}
                }
            }
        }
        sum
    }
}

fn solve_p1(path: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let contents = fs::read_to_string(path)?;
    let (mut grid, operations) = Grid::parse(&contents, false);
    
    let mut robot_pos = grid.get_robot_pos();
    for &op in operations.iter() {
        robot_pos = grid.step(robot_pos, op);
    }
    
    Ok(grid.calculate_score(false))
}

fn solve_p2(path: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let contents = fs::read_to_string(path)?;
    let (mut grid, operations) = Grid::parse(&contents, true);
    
    let mut robot_pos = grid.get_robot_pos();
    for &op in operations.iter() {
        robot_pos = grid.step(robot_pos, op);
    }
    
    Ok(grid.calculate_score(true))
}

fn main() {
    match (solve_p1("data/day15.txt"), solve_p2("data/day15.txt")) {
        (Ok(p1), Ok(p2)) => {
            println!("Part 1: {}", p1);
            println!("Part 2: {}", p2);
        }
        (Err(e), _) | (_, Err(e)) => eprintln!("Error: {}", e),
    }
}

#[cfg(test)]
mod tests {
    use super::*;


    #[test]
    fn test_solve_p1() {
        let result = solve_p1("data/day15.txt").unwrap();
        assert_eq!(result, 1429911);

        let result_example = solve_p1("data/day15_example.txt").unwrap();
        assert_eq!(result_example, 10092);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day15.txt").unwrap();
        assert_eq!(result, 1453087);

        let result_example = solve_p2("data/day15_example.txt").unwrap();
        assert_eq!(result_example, 9021);
    }
} 