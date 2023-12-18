use std::fs::File;
use std::io::{self, BufRead};

fn parse_instructions(file_path: &str) -> io::Result<Vec<String>> {
    let file = File::open(file_path)?;
    let lines = io::BufReader::new(file).lines();
    let instructions: Vec<String> = lines.collect::<Result<_, _>>()?;
    println!(
        "Parsed {} instructions from {}",
        instructions.len(),
        file_path
    );
    Ok(instructions)
}

fn calculate_area(lines: &Vec<String>) -> i64 {
    let directions: Vec<(i64, i64)> = vec![(0, 1), (1, 0), (0, -1), (-1, 0)];
    let mut points: Vec<(i64, i64)> = vec![(0, 0)];
    let mut boundary = 0;

    for line in lines {
        if line.is_empty() {
            continue;
        }

        if let Some(color) = line.split(' ').last() {
            let instructions = &color[2..color.len() - 1];
            let direction_index =
                i64::from_str_radix(&instructions[instructions.len() - 1..], 16).unwrap();
            let (dr, dc) = directions[direction_index as usize];
            let steps = i64::from_str_radix(&instructions[..instructions.len() - 1], 16).unwrap();
            boundary += steps;
            let (row, column) = points.last().unwrap();
            points.push((row + dr * steps, column + dc * steps));
        }
    }

    let mut area = 0;
    for i in 0..points.len() {
        let (x1, y1) = points[i];
        let (x2, y2) = points[(i + 1) % points.len()];
        area += x1 * y2 - x2 * y1;
    }

    (area.abs() / 2) + (boundary / 2) + 1
}

fn run_test(test_file: &str, expected_result: i64) -> io::Result<()> {
    let lines = parse_instructions(test_file)?;
    let calculated_area = calculate_area(&lines);
    assert_eq!(calculated_area, expected_result, "Test failed");
    println!("Test passed, area: {}", calculated_area);
    Ok(())
}

fn main() {
    let test_file = "../test.txt";
    let input_file = "../input.txt";
    let expected_test_area: i64 = 952408144115; // Replace with the correct expected area for the test

    if let Err(e) = run_test(test_file, expected_test_area) {
        eprintln!("Execution halted due to error: {}", e);
        return;
    }

    match parse_instructions(input_file) {
        Ok(lines) => {
            let area = calculate_area(&lines);
            println!("Puzzle result (area): {}", area);
        }
        Err(e) => eprintln!("Execution halted due to error: {}", e),
    }
}
