use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

fn parse_schematic(file_path: &Path) -> io::Result<Vec<String>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);
    reader.lines().collect()
}

fn get_adjacent_positions(rows: usize, cols: usize, row: usize, col: usize) -> Vec<(usize, usize)> {
    let mut positions = Vec::new();
    for i in row.saturating_sub(1)..=(row + 1).min(rows - 1) {
        for j in col.saturating_sub(1)..=(col + 1).min(cols - 1) {
            if i != row || j != col {
                positions.push((i, j));
            }
        }
    }
    positions
}

fn find_start_of_number(schematic: &[String], row: usize, mut col: usize) -> usize {
    while col > 0 && schematic[row].chars().nth(col - 1).unwrap().is_digit(10) {
        col -= 1;
    }
    col
}

fn extract_full_number(schematic: &mut [String], start_row: usize, start_col: usize) -> i32 {
    let start_col = find_start_of_number(schematic, start_row, start_col);
    let mut number = String::new();
    let mut col = start_col;

    while col < schematic[start_row].len() && schematic[start_row].chars().nth(col).unwrap().is_digit(10) {
        number.push(schematic[start_row].chars().nth(col).unwrap());
        schematic[start_row].replace_range(col..=col, ".");
        col += 1;
    }

    number.parse::<i32>().unwrap_or(0)
}

fn find_gears_and_calculate_ratios(schematic: &mut Vec<String>) -> i32 {
    let rows = schematic.len();
    let cols = schematic[0].len();
    let mut total_ratio_sum = 0;

    for row in 0..rows {
        for col in 0..cols {
            if schematic[row].chars().nth(col).unwrap() == '*' {
                let mut part_numbers = Vec::new();
                for (i, j) in get_adjacent_positions(rows, cols, row, col) {
                    if schematic[i].chars().nth(j).unwrap().is_digit(10) {
                        let part_number = extract_full_number(schematic, i, j);
                        if !part_numbers.contains(&part_number) {
                            part_numbers.push(part_number);
                        }
                    }
                }

                if part_numbers.len() == 2 {
                    let gear_ratio = part_numbers[0] * part_numbers[1];
                    total_ratio_sum += gear_ratio;
                    println!("Found gear at line {} with ratio {}", row + 1, gear_ratio);
                }
            }
        }
    }

    total_ratio_sum
}

fn main() {
    let test_path = Path::new("../test.txt");
    let input_path = Path::new("../input.txt");

    match parse_schematic(test_path) {
        Ok(mut test_schematic) => {
            let test_result = find_gears_and_calculate_ratios(&mut test_schematic);
            println!("Test Result: {}", test_result);
            assert_eq!(test_result, 467835, "Test failed: Expected 467835");
        }
        Err(e) => println!("Error reading test file: {}", e),
    }

    match parse_schematic(input_path) {
        Ok(mut input_schematic) => {
            let total_ratio_sum = find_gears_and_calculate_ratios(&mut input_schematic);
            println!("Total sum of gear ratios: {}", total_ratio_sum);
        }
        Err(e) => println!("Error reading input file: {}", e),
    }
}
