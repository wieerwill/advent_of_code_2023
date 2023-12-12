use std::fs;
use std::collections::HashMap;

fn read_data(file_path: &str) -> Result<Vec<String>, String> {
    fs::read_to_string(file_path)
        .map_err(|e| e.to_string())
        .map(|contents| contents.lines().map(String::from).collect())
}

fn unfold_record(record: &str) -> (String, Vec<usize>) {
    let parts: Vec<&str> = record.split(' ').collect();
    let dots = parts[0].repeat(5).split("").collect::<Vec<&str>>().join("?");
    let blocks = parts[1].split(',').map(|x| x.parse::<usize>().unwrap()).collect::<Vec<usize>>();
    let unfolded_blocks = blocks.iter().flat_map(|&b| vec![b; 5]).collect();
    (dots, unfolded_blocks)
}

fn count_arrangements(dots: &str, blocks: &[usize], i: usize, bi: usize, current: usize, memo: &mut HashMap<(usize, usize, usize), usize>) -> usize {
    let key = (i, bi, current);
    if let Some(&result) = memo.get(&key) {
        return result;
    }

    if i == dots.len() {
        return if bi == blocks.len() && current == 0 {
            1
        } else {
            0
        };
    }

    let mut ans = 0;
    let c = dots.chars().nth(i).unwrap();

    if c == '.' || c == '?' {
        if current == 0 {
            ans += count_arrangements(dots, blocks, i + 1, bi, 0, memo);
        } else if bi < blocks.len() && current == blocks[bi] {
            ans += count_arrangements(dots, blocks, i + 1, bi + 1, 0, memo);
        }
    }

    if c == '#' || c == '?' {
        if bi < blocks.len() && (current + 1 <= blocks[bi]) {
            ans += count_arrangements(dots, blocks, i + 1, bi, current + 1, memo);
        }
    }

    memo.insert(key, ans);
    ans
}

fn solve_puzzle(lines: &[String]) -> usize {
    lines.iter().fold(0, |acc, line| {
        println!("Processing: {}", line);
        let (dots, blocks) = unfold_record(line);
        let line_result = count_arrangements(&dots, &blocks, 0, 0, 0, &mut HashMap::new());
        println!("Line result: {}", line_result);
        acc + line_result
    })
}

fn test_puzzle() -> Result<(), String> {
    println!("Running tests...");
    let test_lines = read_data("../test.txt")?;
    let test_result = solve_puzzle(&test_lines);
    println!("Test result: {}", test_result);
    assert_eq!(test_result, 525152, "Test failed!");
    println!("Test passed.");
    Ok(())
}

fn main() -> Result<(), String> {
    test_puzzle()?;

    let input_lines = read_data("../input.txt")?;
    println!("Processing input data...");
    let result = solve_puzzle(&input_lines);
    println!("Final result: {}", result);

    Ok(())
}
