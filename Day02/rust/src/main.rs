use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn parse_game_data(line: &str) -> (i32, HashMap<String, i32>) {
    let parts: Vec<&str> = line.split(": ").collect();
    let game_id = parts[0]
        .split_whitespace()
        .nth(1)
        .unwrap()
        .parse::<i32>()
        .unwrap();
    let mut color_counts = HashMap::new();
    color_counts.insert("red".to_string(), 0);
    color_counts.insert("green".to_string(), 0);
    color_counts.insert("blue".to_string(), 0);

    let subsets = parts[1].split("; ");
    for subset in subsets {
        let colors = subset.split(", ");
        for color in colors {
            let color_parts: Vec<&str> = color.split_whitespace().collect();
            let count = color_parts[0].parse::<i32>().unwrap();
            let color_name = color_parts[1];
            let max_count = color_counts.get(color_name).unwrap_or(&0).max(&count);
            color_counts.insert(color_name.to_string(), *max_count);
        }
    }

    (game_id, color_counts)
}

fn calculate_power_of_set(game_data: &HashMap<String, i32>) -> i32 {
    game_data.get("red").unwrap_or(&0)
        * game_data.get("green").unwrap_or(&0)
        * game_data.get("blue").unwrap_or(&0)
}

fn process_games(file_path: &Path) -> i32 {
    let file = File::open(file_path).unwrap();
    let reader = io::BufReader::new(file);

    let mut sum_of_powers = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        let (_, game_data) = parse_game_data(&line);
        let power = calculate_power_of_set(&game_data);
        sum_of_powers += power;
    }

    sum_of_powers
}

fn main() {
    // Test the function with test data
    let test_result = process_games(Path::new("../test.txt"));
    assert_eq!(
        test_result, 2286,
        "Test failed: expected sum of powers to be 2286, but got {}",
        test_result
    );
    println!(
        "Test Passed: Sum of powers for the minimum cube sets is {}\n",
        test_result
    );

    // Process the actual input file
    let result = process_games(Path::new("../input.txt"));
    println!(
        "From input.txt: Sum of powers for the minimum cube sets is {}",
        result
    );
}
