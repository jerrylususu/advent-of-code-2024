use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};

type Graph = HashMap<String, HashSet<String>>;

fn read_file(path: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let lines: Result<Vec<String>, _> = reader.lines().collect();
    Ok(lines?)
}

fn parse_connections(lines: &[String]) -> Vec<(String, String)> {
    lines.iter()
        .map(|line| {
            let computers: Vec<_> = line.trim().split('-').collect();
            (computers[0].to_string(), computers[1].to_string())
        })
        .collect()
}

fn build_graph(connections: &[(String, String)]) -> Graph {
    let mut graph = HashMap::new();
    
    for (computer1, computer2) in connections {
        graph.entry(computer1.clone())
            .or_insert_with(HashSet::new)
            .insert(computer2.clone());
        graph.entry(computer2.clone())
            .or_insert_with(HashSet::new)
            .insert(computer1.clone());
    }
    
    graph
}

fn find_triangles(graph: &Graph) -> HashSet<Vec<String>> {
    let mut triangles = HashSet::new();
    
    for (a, neighbors_a) in graph {
        for b in neighbors_a {
            if b > a {
                if let Some(neighbors_b) = graph.get(b) {
                    for c in neighbors_b {
                        if c > b && neighbors_a.contains(c) {
                            let mut triangle = vec![a.clone(), b.clone(), c.clone()];
                            triangle.sort();
                            triangles.insert(triangle);
                        }
                    }
                }
            }
        }
    }
    
    triangles
}

fn bron_kerbosch(graph: &Graph, r: &mut HashSet<String>, p: &mut HashSet<String>, x: &mut HashSet<String>, cliques: &mut Vec<HashSet<String>>) {
    if p.is_empty() && x.is_empty() {
        cliques.push(r.clone());
        return;
    }
    
    let pivot = p.union(x).next().unwrap().clone();
    let p_copy = p.clone();
    
    for v in p_copy {
        if !graph[&pivot].contains(&v) {
            let neighbors = graph.get(&v).unwrap();
            let mut new_r = r.clone();
            new_r.insert(v.clone());
            let mut new_p = p.intersection(neighbors).cloned().collect();
            let mut new_x = x.intersection(neighbors).cloned().collect();
            
            bron_kerbosch(graph, &mut new_r, &mut new_p, &mut new_x, cliques);
            p.remove(&v);
            x.insert(v.clone());
        }
    }
}

fn find_largest_clique(graph: &Graph) -> HashSet<String> {
    let mut cliques = Vec::new();
    let mut r = HashSet::new();
    let mut p: HashSet<_> = graph.keys().cloned().collect();
    let mut x = HashSet::new();
    
    bron_kerbosch(graph, &mut r, &mut p, &mut x, &mut cliques);
    
    cliques.into_iter().max_by_key(|clique| clique.len()).unwrap()
}

fn solve_p1(path: &str) -> Result<usize, Box<dyn Error>> {
    let lines = read_file(path)?;
    let connections = parse_connections(&lines);
    let graph = build_graph(&connections);
    let triangles = find_triangles(&graph);
    
    let t_triangles = triangles.iter()
        .filter(|triangle| triangle.iter().any(|computer| computer.starts_with('t')))
        .count();
    
    Ok(t_triangles)
}

fn solve_p2(path: &str) -> Result<String, Box<dyn Error>> {
    let lines = read_file(path)?;
    let connections = parse_connections(&lines);
    let graph = build_graph(&connections);
    
    let largest_clique = find_largest_clique(&graph);
    let mut result: Vec<_> = largest_clique.into_iter().collect();
    result.sort();
    
    Ok(result.join(","))
}

fn main() -> Result<(), Box<dyn Error>> {
    let t_triangles = solve_p1("input.txt")?;
    println!("Part 1: {}", t_triangles);

    let result_p2 = solve_p2("input.txt")?;
    println!("Part 2: {}", result_p2);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_p1() {
        let result = solve_p1("data/day23.txt").unwrap();
        assert_eq!(result, 1230);

        let result2 = solve_p1("data/day23_example.txt").unwrap();
        assert_eq!(result2, 7);
    }

    #[test]
    fn test_solve_p2() {
        let result = solve_p2("data/day23.txt").unwrap();
        assert_eq!(result, "az,cj,kp,lm,lt,nj,rf,rx,sn,ty,ui,wp,zo");

        let result2 = solve_p2("data/day23_example.txt").unwrap();
        assert_eq!(result2, "co,de,ka,ta");
    }
} 