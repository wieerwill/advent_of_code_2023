use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let path = Path::new("../input.txt");
    match read_lines(path) {
        Ok(lines) => {
            let mut total = 0;
            // Using flatten to directly iterate over Ok values
            for ip in lines.flatten() {
                let value = extract_calibration_value(&ip);
                println!("Line: '{}', Calibration Value: {}", ip, value);
                total += value;
            }
            println!("Total Calibration Value: {}", total);
        }
        Err(e) => println!("Error: {}", e),
    }
}

// Function to read lines from a file
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn extract_calibration_value(line: &str) -> u32 {
    let digits = extract_digits(line);
    match (digits.first(), digits.last()) {
        (Some(first), Some(last)) => format!("{}{}", first, last).parse::<u32>().unwrap_or(0),
        _ => 0,
    }
}

fn extract_digits(line: &str) -> Vec<u32> {
    let digit_map = vec![
        ("zero", 0),
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ];

    let mut digits = Vec::new();
    let mut current_line = line.to_string();

    while !current_line.is_empty() {
        let mut found = false;

        for (word, digit) in &digit_map {
            if current_line.starts_with(word) {
                digits.push(*digit);
                current_line = current_line[word.len()..].to_string();
                found = true;
                break;
            }
        }

        if !found {
            if let Some(first_char) = current_line.chars().next() {
                if let Some(digit) = first_char.to_digit(10) {
                    digits.push(digit);
                }
                current_line = current_line[1..].to_string();
            }
        }
    }

    digits
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_calibration_value() {
        let test_cases = vec![
            ("two1nine", 29),
            ("eightwothree", 83),
            ("abcone2threexyz", 13),
            ("xtwone3four", 24),
            ("4nineeightseven2", 42),
            ("zoneight234", 14),
            ("7pqrstsixteen", 76),
        ];

        for (input, expected) in test_cases {
            assert_eq!(
                extract_calibration_value(input),
                expected,
                "Failed on input: {}",
                input
            );
        }
    }
}
