use std::collections::HashMap;
use std::fs;

fn hash_label(label: &str) -> usize {
    label
        .chars()
        .fold(0, |acc, c| (acc + (c as usize)) * 17 % 256)
}

fn process_steps(steps: Vec<&str>) -> usize {
    let mut boxes = vec![Vec::new(); 256];
    let mut focal_lengths: HashMap<String, usize> = HashMap::new();

    for step in steps.iter() {
        let (label, operation, value) = parse_step(step);
        let hashed = hash_label(label);

        println!("Processing step: {}, Box: {}", step, hashed);

        match operation {
            '=' => {
                let focal_length = value.parse::<usize>().expect("Invalid focal length");
                if !boxes[hashed].contains(&label.to_string()) {
                    boxes[hashed].push(label.to_string());
                }
                focal_lengths.insert(label.to_string(), focal_length);
            }
            '-' => {
                boxes[hashed].retain(|l| l != label);
                focal_lengths.remove(label);
            }
            _ => panic!("Invalid operation character: {}", operation),
        }
    }

    boxes.iter().enumerate().fold(0, |acc, (box_num, labels)| {
        acc + labels.iter().enumerate().fold(0, |acc, (i, label)| {
            acc + (box_num + 1) * (i + 1) * focal_lengths.get(label).unwrap_or(&0)
        })
    })
}

fn parse_step(step: &str) -> (&str, char, &str) {
    let operation_index = step
        .find(|c: char| c == '=' || c == '-')
        .expect("Invalid step format");
    let label = &step[..operation_index];
    let operation = step
        .chars()
        .nth(operation_index)
        .expect("Invalid step format");
    let value = &step[operation_index + 1..];

    (label, operation, value)
}

fn read_file_content(file_path: &str) -> String {
    fs::read_to_string(file_path).expect(&format!("Error reading file at {}", file_path))
}

fn test_algorithm() {
    let test_content = read_file_content("../test.txt");
    let test_steps: Vec<&str> = test_content.trim().split(',').collect();
    let test_result = process_steps(test_steps);

    println!("Test Result: {}", test_result);
    assert_eq!(
        test_result, 145,
        "Test failed. Expected result is 145, got {}.",
        test_result
    );
}

fn main() {
    test_algorithm();
    println!("Test passed.");

    let input_content = read_file_content("../input.txt");
    let input_steps: Vec<&str> = input_content.trim().split(',').collect();
    let final_result = process_steps(input_steps);

    println!("Final Result: {}", final_result);
}
