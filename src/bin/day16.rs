use std::collections::{BinaryHeap, HashSet, HashMap};
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::cmp::Ordering;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Facing {
    East = 0,
    South = 1,
    West = 2,
    North = 3,
}

impl Facing {
    fn turn_right(&self) -> Self {
        match self {
            Facing::East => Facing::South,
            Facing::South => Facing::West,
            Facing::West => Facing::North,
            Facing::North => Facing::East,
        }
    }

    fn turn_left(&self) -> Self {
        match self {
            Facing::East => Facing::North,
            Facing::South => Facing::East,
            Facing::West => Facing::South,
            Facing::North => Facing::West,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Position {
    row: i32,
    col: i32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct State {
    score: i32,
    pos: Position,
    facing: Facing,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.score.cmp(&self.score)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn get_next_pos(pos: Position, facing: Facing) -> Position {
    match facing {
        Facing::East => Position { row: pos.row, col: pos.col + 1 },
        Facing::South => Position { row: pos.row + 1, col: pos.col },
        Facing::West => Position { row: pos.row, col: pos.col - 1 },
        Facing::North => Position { row: pos.row - 1, col: pos.col },
    }
}

fn is_valid_move(grid: &Vec<Vec<char>>, pos: Position) -> bool {
    if pos.row < 0 || pos.row >= grid.len() as i32 || 
       pos.col < 0 || pos.col >= grid[0].len() as i32 {
        return false;
    }
    grid[pos.row as usize][pos.col as usize] != '#'
}

fn solve_dijkstra_with_parents(grid: &Vec<Vec<char>>, start_pos: Position, end_pos: Position) 
    -> (i32, HashMap<(Position, Facing), Vec<(Position, Facing)>>) 
{
    let mut queue = BinaryHeap::new();
    let mut visited = HashSet::new();
    let mut best_scores = HashMap::new();
    let mut parents = HashMap::new();

    queue.push(State {
        score: 0,
        pos: start_pos,
        facing: Facing::East,
    });

    while let Some(State { score, pos, facing }) = queue.pop() {
        if visited.contains(&(pos, facing)) {
            continue;
        }

        visited.insert((pos, facing));

        if pos == end_pos {
            return (score, parents);
        }

        // 尝试向前移动
        let next_pos = get_next_pos(pos, facing);
        if is_valid_move(grid, next_pos) {
            let next_score = score + 1;
            let next_state = (next_pos, facing);
            if !visited.contains(&next_state) && 
               (!best_scores.contains_key(&next_state) || next_score <= *best_scores.get(&next_state).unwrap()) {
                best_scores.insert(next_state, next_score);
                parents.entry(next_state)
                    .or_insert_with(Vec::new)
                    .push((pos, facing));
                queue.push(State {
                    score: next_score,
                    pos: next_pos,
                    facing,
                });
            }
        }

        // 尝试转向
        for turn_direction in [Facing::turn_right, Facing::turn_left] {
            let next_facing = turn_direction(&facing);
            let next_score = score + 1000;
            let next_state = (pos, next_facing);
            if !visited.contains(&next_state) &&
               (!best_scores.contains_key(&next_state) || next_score <= *best_scores.get(&next_state).unwrap()) {
                best_scores.insert(next_state, next_score);
                parents.entry(next_state)
                    .or_insert_with(Vec::new)
                    .push((pos, facing));
                queue.push(State {
                    score: next_score,
                    pos,
                    facing: next_facing,
                });
            }
        }
    }

    (i32::MAX, parents)
}

fn backtrack_paths(
    state: (Position, Facing),
    start_pos: Position,
    parents: &HashMap<(Position, Facing), Vec<(Position, Facing)>>,
    positions: &mut HashSet<Position>
) {
    positions.insert(state.0);
    
    if state.0 == start_pos {
        return;
    }

    if let Some(parent_states) = parents.get(&state) {
        for &parent_state in parent_states {
            backtrack_paths(parent_state, start_pos, parents, positions);
        }
    }
}

fn find_positions(grid: &Vec<Vec<char>>) -> (Position, Position) {
    let mut start_pos = Position { row: 0, col: 0 };
    let mut end_pos = Position { row: 0, col: 0 };

    for (row, line) in grid.iter().enumerate() {
        for (col, &ch) in line.iter().enumerate() {
            match ch {
                'S' => start_pos = Position { row: row as i32, col: col as i32 },
                'E' => end_pos = Position { row: row as i32, col: col as i32 },
                _ => (),
            }
        }
    }
    (start_pos, end_pos)
}

fn solve_p1(path: &str) -> Result<i32, Box<dyn Error>> {
    let lines = read_file(path)?;
    let grid: Vec<Vec<char>> = lines.iter()
        .map(|line| line.chars().collect())
        .collect();

    let (start_pos, end_pos) = find_positions(&grid);
    let (min_score, _) = solve_dijkstra_with_parents(&grid, start_pos, end_pos);
    Ok(min_score)
}

fn solve_p2(path: &str) -> Result<usize, Box<dyn Error>> {
    let lines = read_file(path)?;
    let grid: Vec<Vec<char>> = lines.iter()
        .map(|line| line.chars().collect())
        .collect();

    let (start_pos, end_pos) = find_positions(&grid);
    
    let (_, parents) = solve_dijkstra_with_parents(&grid, start_pos, end_pos);
    let mut min_score_positions = HashSet::new();

    // 从终点开始回溯所有最短路径
    for facing in [Facing::East, Facing::South, Facing::West, Facing::North] {
        let end_state = (end_pos, facing);
        backtrack_paths(end_state, start_pos, &parents, &mut min_score_positions);
    }

    Ok(min_score_positions.len())
}

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
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
        let result = solve_p1("data/day16.txt").unwrap();
        assert_eq!(result, 107512);

        let result_example = solve_p1("data/day16_example.txt").unwrap();
        assert_eq!(result_example, 7036);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day16.txt").unwrap();
        assert_eq!(result, 561);

        let result_example = solve_p2("data/day16_example.txt").unwrap();
        assert_eq!(result_example, 45);
    }
} 