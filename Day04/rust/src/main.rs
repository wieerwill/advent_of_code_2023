use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() {
    // Run tests
    match run_test("../test.txt") {
        Ok(()) => println!("Tests passed."),
        Err(e) => eprintln!("Test failed: {}", e),
    }

    // Process main puzzle input
    match process_input("../input.txt") {
        Ok(result) => println!("Puzzle result: {}", result),
        Err(e) => eprintln!("Error processing input: {}", e),
    }
}

fn run_test(filename: &str) -> Result<(), String> {
    let input = read_input(filename)?;
    let cards = parse(&input);

    let part_a_result = part_a(&cards);
    let part_b_result = part_b(&cards);

    assert_eq!(part_a_result, 13, "Part A Test failed");
    assert_eq!(part_b_result, 30, "Part B Test failed");

    Ok(())
}

fn process_input(filename: &str) -> Result<u32, String> {
    let input = read_input(filename)?;
    let cards = parse(&input);

    Ok(part_a(&cards) + part_b(&cards))
}

fn part_a(cards: &[Card]) -> u32 {
    cards
        .iter()
        .filter(|x| x.wins > 0)
        .map(|x| 2u32.pow(x.wins.saturating_sub(1) as u32))
        .sum()
}

fn part_b(cards: &[Card]) -> u32 {
    let mut queue = (0..cards.len()).collect::<Vec<_>>();
    let mut visited = 0;

    while let Some(i) = queue.pop() {
        visited += 1;

        let card = &cards[i];
        if card.wins == 0 {
            continue;
        }

        for j in 0..card.wins as usize {
            queue.push(j + i + 1);
        }
    }

    visited as u32
}

fn read_input(filename: &str) -> Result<String, String> {
    let file = File::open(filename).map_err(|e| e.to_string())?;
    let buffer = BufReader::new(file);

    buffer
        .lines()
        .collect::<Result<Vec<_>, io::Error>>()
        .map_err(|e| e.to_string())
        .map(|lines| lines.join("\n"))
}

fn parse(input: &str) -> Vec<Card> {
    input
        .lines()
        .map(|line| {
            let (_, line) = line.split_once(": ").unwrap();
            let (winning, scratch) = line.split_once(" | ").unwrap();
            let parse = |s: &str| {
                s.split_whitespace()
                    .map(|x| x.parse::<u8>().unwrap())
                    .collect::<Vec<u8>>()
            };

            let winning = parse(winning);
            let scratch = parse(scratch);
            
            Card {
                wins: scratch.iter().filter(|x| winning.contains(x)).count() as u8,
            }
        })
        .collect()
}

struct Card {
    wins: u8,
}
