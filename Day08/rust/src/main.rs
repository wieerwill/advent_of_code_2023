use std::fs;
use std::collections::HashMap;
use std::path::Path;

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

fn lcm(a: u64, b: u64) -> u64 {
    a / gcd(a, b) * b
}

fn parse_file(file_path: &Path) -> Result<(Vec<u8>, HashMap<String, (String, String)>), String> {
    let data = fs::read_to_string(file_path).map_err(|e| e.to_string())?;
    let mut sections = data.trim().split("\n\n");
    let steps = sections.next().unwrap()
        .chars()
        .map(|c| if c == 'L' { 0 } else { 1 })
        .collect();
    let rules_section = sections.next().unwrap();

    let mut rules = HashMap::new();
    for line in rules_section.lines() {
        let mut parts = line.split('=').map(str::trim);
        let state = parts.next().unwrap().to_string();
        let directions = parts.next().unwrap()
            .split(',')
            .map(str::trim)
            .map(|s| s.trim_matches(|c: char| c == '(' || c == ')').to_string())
            .collect::<Vec<_>>();

        rules.insert(state, (directions[0].clone(), directions[1].clone()));
    }

    Ok((steps, rules))
}

fn navigate_network_simultaneously(steps: &[u8], rules: &HashMap<String, (String, String)>) -> u64 {
    let start_nodes: Vec<String> = rules.keys()
        .filter(|k| k.ends_with('A'))
        .cloned()
        .collect();
    let mut current_nodes = start_nodes.clone();
    let mut step_count = 0;
    let mut time_to_z = HashMap::new();

    while time_to_z.len() < start_nodes.len() {
        for (i, node) in current_nodes.iter_mut().enumerate() {
            let direction = if steps[step_count % steps.len()] == 0 { 'L' } else { 'R' };
            let next_node = if direction == 'L' { &rules[node].0 } else { &rules[node].1 };
            *node = next_node.clone();
            
            if next_node.ends_with('Z') && !time_to_z.contains_key(&i) {
                time_to_z.insert(i, step_count + 1);
            }
        }

        if time_to_z.len() == start_nodes.len() {
            break;
        }

        step_count += 1;
        println!("Step {}: Current nodes - {:?}", step_count, current_nodes);
    }

    time_to_z.values().fold(1, |acc, &val| lcm(acc, val as u64))
}

fn run_test(test_file: &Path) {
    println!("Running test...");
    let (steps, rules) = parse_file(test_file).expect("Failed to parse test file");
    let result = navigate_network_simultaneously(&steps, &rules);
    assert_eq!(result, 6, "Test failed: expected 6, got {}", result);
    println!("Test passed with {} steps.", result);
}

fn main() {
    let test_path = Path::new("../test.txt");
    run_test(&test_path);

    let input_path = Path::new("../input.txt");
    let (steps, rules) = parse_file(&input_path).expect("Failed to parse input file");
    let result = navigate_network_simultaneously(&steps, &rules);
    println!("All paths reached 'Z' nodes simultaneously in {} steps.", result);
}
