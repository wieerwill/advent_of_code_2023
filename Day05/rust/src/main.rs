use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::str::FromStr;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn parse_input(file_path: &str) -> io::Result<(Vec<(i32, i32)>, Vec<Vec<(i32, i32, i32)>>)> {
    let mut seeds_numbers = Vec::new();
    let mut categories = Vec::new();
    let mut current_category = Vec::new();
    let mut is_seed_line = true;

    for line in read_lines(file_path)? {
        let line = line?;
        if line.is_empty() {
            if !current_category.is_empty() {
                categories.push(current_category);
                current_category = Vec::new();
            }
            is_seed_line = false;
            continue;
        }

        if is_seed_line {
            let seeds_ranges: Vec<i32> = line.split_whitespace()
                .skip(1)
                .filter_map(|s| i32::from_str(s).ok())
                .collect();

            for seeds in seeds_ranges.chunks(2) {
                if seeds.len() == 2 {
                    seeds_numbers.extend((seeds[0]..seeds[0] + seeds[1]).map(|n| (n, n + 1)));
                }
            }
        } else {
            let numbers: Vec<i32> = line.split_whitespace()
                .filter_map(|s| i32::from_str(s).ok())
                .collect();
            if numbers.len() == 3 {
                current_category.push((numbers[0], numbers[1], numbers[2]));
            }
        }
    }
    if !current_category.is_empty() {
        categories.push(current_category);
    }

    Ok((seeds_numbers, categories))
}

fn process_categories(mut seeds_numbers: Vec<(i32, i32)>, categories: Vec<Vec<(i32, i32, i32)>>) -> Vec<(i32, i32)> {
    for category in categories {
        let mut sources = Vec::new();
        while let Some((start, end)) = seeds_numbers.pop() {
            let mut is_mapped = false;
            for &(destination, source, length) in &category {
                let overlap_start = std::cmp::max(start, source);
                let overlap_end = std::cmp::min(end, source + length);
                if overlap_start < overlap_end {
                    sources.push((overlap_start - source + destination, overlap_end - source + destination));
                    if overlap_start > start {
                        seeds_numbers.push((start, overlap_start));
                    }
                    if end > overlap_end {
                        seeds_numbers.push((overlap_end, end));
                    }
                    is_mapped = true;
                    break;
                }
            }
            if !is_mapped {
                sources.push((start, end));
            }
        }
        seeds_numbers = sources;
    }
    seeds_numbers
}

fn find_lowest_location(file_path: &str) -> io::Result<i32> {
    let (seeds_numbers, categories) = parse_input(file_path)?;
    let processed_seeds = process_categories(seeds_numbers, categories);
    let lowest_location = processed_seeds.iter().map(|&(start, _)| start).min().unwrap();
    Ok(lowest_location)
}

fn main() -> io::Result<()> {
    // Test
    let test_result = find_lowest_location("../test.txt")?;
    assert_eq!(test_result, 46, "Test failed. Expected 46, got {}", test_result);
    println!("Test passed.");

    // Process actual input
    let result = find_lowest_location("../input.txt")?;
    println!("Total result from input.txt: {}", result);

    Ok(())
}
