use std::collections::HashMap;
use std::fs;

#[derive(Debug, Clone)]
struct Spring {
    field: Vec<char>,
    springs: Vec<usize>,
}

fn main() {
    match test_puzzle("../test.txt") {
        Ok(_) => println!("Test passed."),
        Err(e) => println!("Test failed: {}", e),
    };

    match run_puzzle("../input.txt") {
        Ok(result) => println!("Final result: {}", result),
        Err(e) => println!("Error: {}", e),
    };
}

fn run_puzzle(file_path: &str) -> Result<usize, String> {
    let input = fs::read_to_string(file_path).map_err(|e| e.to_string())?;
    let springs = parse(&input);
    Ok(springs.iter().map(|s| s.clone().expand().arrangements()).sum())
}

fn test_puzzle(file_path: &str) -> Result<(), String> {
    let input = fs::read_to_string(file_path).map_err(|e| e.to_string())?;
    let springs = parse(&input);
    let result = springs.iter().map(|s| s.clone().expand().arrangements()).sum::<usize>();
    assert_eq!(result, 525152, "Test failed!");
    Ok(())
}

fn parse(input: &str) -> Vec<Spring> {
    input
        .lines()
        .map(|line| {
            let (field, springs) = line.split_once(' ').unwrap();
            let springs = springs.split(',').map(|s| s.parse().unwrap()).collect::<Vec<_>>();
            let mut field = field.chars().collect::<Vec<_>>();
            field.push('.');
            Spring { field, springs }
        })
        .collect()
}

impl Spring {
    fn arrangements(&self) -> usize {
        fn count(
            memo: &mut HashMap<(usize, usize, usize), usize>,
            spring: &Spring,
            pos: usize,
            block: usize,
            sequences: usize,
        ) -> usize {
            if let Some(&res) = memo.get(&(pos, block, sequences)) {
                return res;
            }

            let mut res = 0;
            if pos == spring.field.len() {
                res = (sequences == spring.springs.len()) as usize;
            } else if spring.field[pos] == '#' {
                res = count(memo, spring, pos + 1, block + 1, sequences)
            } else if spring.field[pos] == '.' || sequences == spring.springs.len() {
                if sequences < spring.springs.len() && block == spring.springs[sequences] {
                    res = count(memo, spring, pos + 1, 0, sequences + 1)
                } else if block == 0 {
                    res = count(memo, spring, pos + 1, 0, sequences)
                }
            } else {
                res += count(memo, spring, pos + 1, block + 1, sequences);
                if block == spring.springs[sequences] {
                    res += count(memo, spring, pos + 1, 0, sequences + 1)
                } else if block == 0 {
                    res += count(memo, spring, pos + 1, 0, sequences)
                }
            }

            memo.insert((pos, block, sequences), res);
            res
        }

        count(&mut HashMap::new(), self, 0, 0, 0)
    }

    fn expand(&self) -> Self {
        let mut new_field = self.field.clone();
        *new_field.last_mut().unwrap() = '?';

        Self {
            field: new_field.repeat(5),
            springs: self.springs.repeat(5),
        }
    }
}
