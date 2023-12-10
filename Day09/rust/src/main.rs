use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

fn generate_difference_table(history: &[i32]) -> Vec<Vec<i32>> {
    // Generates a difference table for a given history
    let mut table: Vec<Vec<i32>> = vec![history.to_vec()];
    while !table.last().unwrap().iter().all(|&x| x == 0) {
        let next_row: Vec<i32> = table
            .last()
            .unwrap()
            .windows(2)
            .map(|pair| pair[1] - pair[0])
            .collect();
        table.push(next_row);
    }
    table
}

fn extrapolate_previous_value(table: &mut Vec<Vec<i32>>) -> i32 {
    // Extrapolates the previous value from the difference table
    for i in (0..table.len() - 1).rev() {
        let diff = table[i][0] - table[i + 1][0];
        table[i].insert(0, diff);
    }
    table[0][0]
}

fn solve_puzzle(filename: &str) -> Result<i32, io::Error> {
    // Solves the puzzle by reading histories from the file and summing their extrapolated previous values
    let path = Path::new(filename);
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut total = 0;
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let history: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        let mut diff_table = generate_difference_table(&history);
        let prev_value = extrapolate_previous_value(&mut diff_table);
        total += prev_value;
    }

    Ok(total)
}

fn test() -> Result<(), io::Error> {
    // Runs the test using the test.txt file and asserts the expected outcome
    let expected = 2; // Expected result from the test data for the second part
    let result = solve_puzzle("../test.txt")?;
    assert_eq!(
        result, expected,
        "Test failed: Expected {}, got {}",
        expected, result
    );
    println!("Test passed successfully.");
    Ok(())
}

fn main() -> Result<(), io::Error> {
    // Main function to run the test and then solve the puzzle
    println!("Running test for the second part...");
    test()?;
    println!("Test completed. Solving the puzzle for the second part...");
    let result = solve_puzzle("../input.txt")?;
    println!("Puzzle result for the second part: {}", result);
    Ok(())
}
