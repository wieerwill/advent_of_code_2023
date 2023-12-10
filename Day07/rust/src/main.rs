use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};

fn read_hands(filename: &str) -> io::Result<Vec<(String, i32)>> {
    let file = File::open(filename)?;
    let lines = io::BufReader::new(file).lines();

    let mut hands = Vec::new();
    for line in lines.flatten() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() == 2 {
            let hand = parts[0].to_string();
            let bid: i32 = parts[1].parse().unwrap();
            hands.push((hand, bid));
        }
    }
    Ok(hands)
}

fn replace_face_cards(hand: &str) -> String {
    let mut replaced = hand.to_string();
    replaced = replaced.replace('T', "a");
    replaced = replaced.replace('J', "1");
    replaced = replaced.replace('Q', "c");
    replaced = replaced.replace('K', "d");
    replaced = replaced.replace('A', "e");
    replaced
}

fn calculate_strength(hand: &str) -> (i32, String) {
    let replaced_hand = replace_face_cards(hand);
    let mut counts = HashMap::new();
    for c in replaced_hand.chars() {
        *counts.entry(c).or_insert(0) += 1;
    }

    let mut joker_count = 0;
    if counts.contains_key(&'1') {
        joker_count = counts.remove(&'1').unwrap();
    }

    let mut best_category = 4; // Default to High card
    for (card, count) in &counts {
        let adjusted_count = if *card != '1' {
            count + joker_count
        } else {
            *count
        };
        best_category = best_category.max(match adjusted_count {
            5 => 10,
            4 => 9,
            3 if counts.values().any(|&v| v == 2) => 8,
            3 => 7,
            _ => best_category,
        });
    }

    // Use original hand for tie-breaking
    let tie_breaker_hand = hand.chars().collect::<String>();
    println!(
        "Hand: {}, Strength: {}, Tie-breaker hand: {}",
        hand, best_category, tie_breaker_hand
    );
    (best_category, tie_breaker_hand)
}

fn calculate_total_winnings(hands: Vec<(String, i32)>) -> i32 {
    let mut sorted_hands = hands;
    // Sort based on strength and original hand for tie-breaking
    sorted_hands.sort_unstable_by(|a, b| {
        let (strength_a, tie_breaker_a) = calculate_strength(&a.0);
        let (strength_b, tie_breaker_b) = calculate_strength(&b.0);
        (strength_b, tie_breaker_b).cmp(&(strength_a, tie_breaker_a))
    });

    sorted_hands
        .iter()
        .enumerate()
        .fold(0, |acc, (i, (hand, bid))| {
            let winnings = bid * (i as i32 + 1);
            println!(
                "Hand: {}, Rank: {}, Bid: {}, Winnings: {}",
                hand,
                i + 1,
                bid,
                winnings
            );
            acc + winnings
        })
}

fn main() {
    let test_hands = read_hands("../test.txt").expect("Failed to read test file");
    let test_total = calculate_total_winnings(test_hands);
    assert_eq!(
        test_total, 5905,
        "Test failed: expected 5905, got {}",
        test_total
    );
    println!("Test passed: Total winnings = {}", test_total);

    let hands = read_hands("../input.txt").expect("Failed to read input file");
    let total_winnings = calculate_total_winnings(hands);
    println!("Total winnings from input.txt: {}", total_winnings);
}
