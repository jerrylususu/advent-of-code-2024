use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use rayon::prelude::*;
use std::time::Instant;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn mix_into_secret(secret: u64, value: u64) -> u64 {
    secret ^ value
}

fn prune_secret(secret: u64) -> u64 {
    secret % 16777216
}

fn evolve_secret(mut secret: u64) -> u64 {
    let temp1 = secret * 64;
    secret = mix_into_secret(secret, temp1);
    secret = prune_secret(secret);

    let temp2 = secret / 32;
    secret = mix_into_secret(secret, temp2);
    secret = prune_secret(secret);

    let temp3 = secret * 2048;
    secret = mix_into_secret(secret, temp3);
    secret = prune_secret(secret);

    secret
}

fn get_price_changes(initial_secret: u64, change_count: usize) -> (Vec<i32>, Vec<u64>) {
    let mut price_changes = Vec::new();
    let mut prices = Vec::new();
    let mut last_secret = initial_secret;
    
    for _ in 0..change_count {
        let current_secret = evolve_secret(last_secret);
        let last_price = (last_secret % 10) as i32;
        let current_price = (current_secret % 10) as i32;
        price_changes.push(current_price - last_price);
        prices.push(current_secret % 10);
        last_secret = current_secret;
    }
    
    (price_changes, prices)
}

fn try_match_change_sequence(change_sequence: &[i32], price_changes: &[i32]) -> Option<usize> {
    if change_sequence.len() > price_changes.len() {
        return None;
    }
    
    for i in 0..=price_changes.len() - change_sequence.len() {
        if price_changes[i..i + change_sequence.len()] == change_sequence[..] {
            return Some(i + change_sequence.len() - 1);
        }
    }
    None
}

fn get_all_appeared_change_sequences(secrets: &[u64]) -> HashSet<Vec<i32>> {
    let mut all_sequences = HashSet::new();
    const SEQUENCE_LENGTH: usize = 4;

    for &secret in secrets {
        let (price_changes, _) = get_price_changes(secret, 2000);
        
        // 从价格变化序列中提取所有长度为4的子序列
        for i in 0..=price_changes.len() - SEQUENCE_LENGTH {
            let sequence: Vec<i32> = price_changes[i..i + SEQUENCE_LENGTH].to_vec();
            all_sequences.insert(sequence);
        }
    }

    all_sequences
}

fn get_banana_count(change_sequence: &[i32], price_changes: &[i32], prices: &[u64]) -> u64 {
    match try_match_change_sequence(change_sequence, price_changes) {
        Some(idx) => prices[idx],
        None => 0,
    }
}

fn solve_p1(path: &str) -> Result<u64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let secrets: Vec<u64> = lines
        .iter()
        .map(|line| line.trim().parse().unwrap())
        .collect();

    const STEP: usize = 2000;
    let mut sum_after_step = 0;

    for mut secret in secrets {
        for _ in 0..STEP {
            secret = evolve_secret(secret);
        }
        sum_after_step += secret;
    }

    Ok(sum_after_step)
}

fn solve_p2(path: &str) -> Result<u64, Box<dyn Error>> {
    let lines = read_file(path)?;
    let secrets: Vec<u64> = lines
        .iter()
        .map(|line| line.trim().parse().unwrap())
        .collect();

    let all_sequences: Vec<_> = get_all_appeared_change_sequences(&secrets)
        .into_iter()
        .enumerate()
        .collect();
    
    let total_sequences = all_sequences.len();
    println!("Total possible sequences: {}", total_sequences);
    
    let start_time = Instant::now();
    let progress = std::sync::atomic::AtomicUsize::new(0);

    // 并行计算每个序列能获得的香蕉总数
    let results: Vec<_> = all_sequences
        .par_iter()
        .map(|(index, sequence)| {
            let mut banana_count = 0;
            
            for &secret in &secrets {
                let (price_changes, prices) = get_price_changes(secret, 2000);
                banana_count += get_banana_count(sequence, &price_changes, &prices);
            }

            // 更新进度并计算 ETA
            let completed = progress.fetch_add(1, std::sync::atomic::Ordering::Relaxed) + 1;
            if completed % 5 == 0 || completed == total_sequences {
                let elapsed = start_time.elapsed().as_secs_f64();
                let progress_ratio = completed as f64 / total_sequences as f64;
                let eta_seconds = (elapsed / progress_ratio) - elapsed;
                
                println!(
                    "Progress: {}/{} ({:.1}%) - ETA: {:.1}s - Sequence #{}: {:?} yields {} bananas", 
                    completed, 
                    total_sequences,
                    progress_ratio * 100.0,
                    eta_seconds,
                    index, 
                    sequence, 
                    banana_count
                );
            }

            (sequence.clone(), banana_count)
        })
        .collect();

    let (best_sequence, max_bananas) = results
        .into_iter()
        .max_by_key(|(_, count)| *count)
        .unwrap();

    let total_time = start_time.elapsed().as_secs_f64();
    println!("Best sequence found: {:?}", best_sequence);
    println!("Total execution time: {:.1}s", total_time);
    
    Ok(max_bananas)
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
        let result = solve_p1("data/day22_example.txt").unwrap();
        assert_eq!(result, 37990510);

        let result = solve_p1("data/day22.txt").unwrap();
        assert_eq!(result, 14119253575);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day22_example.txt").unwrap();
        assert_eq!(result, 23);

        // will take very long time, commented out for now
        // let result = solve_p2("data/day22.txt").unwrap();
        // assert_eq!(result, 1600);
    }
} 