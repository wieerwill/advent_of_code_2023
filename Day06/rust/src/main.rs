use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn parse_input(file_path: &str) -> io::Result<(i64, i64)> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let time_line = lines.next().ok_or(io::Error::new(io::ErrorKind::Other, "Missing time line"))??;
    let distance_line = lines.next().ok_or(io::Error::new(io::ErrorKind::Other, "Missing distance line"))??;

    let time = time_line.chars().filter(|c| c.is_digit(10)).collect::<String>().parse::<i64>().unwrap_or(0);
    let distance = distance_line.chars().filter(|c| c.is_digit(10)).collect::<String>().parse::<i64>().unwrap_or(0);

    Ok((time, distance))
}

fn calculate_winning_ways(time: i64, record: i64) -> i64 {
    let mut min_hold_time = 0;
    while min_hold_time * (time - min_hold_time) <= record && min_hold_time < time {
        min_hold_time += 1;
    }
    let mut max_hold_time = time - 1;
    while max_hold_time * (time - max_hold_time) <= record && max_hold_time >= 0 {
        max_hold_time -= 1;
    }
    std::cmp::max(0, max_hold_time - min_hold_time + 1)
}

fn run_test(file_path: &str, expected_result: i64) -> io::Result<()> {
    let (time, distance) = parse_input(file_path)?;
    let result = calculate_winning_ways(time, distance);
    assert_eq!(result, expected_result, "Test failed! Expected {}, got {}", expected_result, result);
    println!("Test passed successfully.");
    Ok(())
}

fn main() {
    let test_file_path = "../test.txt";
    let expected_test_result = 71503; // Expected result from the test file
    if let Err(e) = run_test(test_file_path, expected_test_result) {
        eprintln!("An error occurred during test: {}", e);
        return;
    }

    let input_file_path = "../input.txt";
    match parse_input(input_file_path) {
        Ok((time, distance)) => {
            let result = calculate_winning_ways(time, distance);
            println!("Final result from input file: {}", result);
        }
        Err(e) => eprintln!("An error occurred while processing input file: {}", e),
    }
}
