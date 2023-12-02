# Advent of Code 2023

## Overview
Welcome to my repository where I share my solutions for the [Advent of Code 2023](https://adventofcode.com/2023). Advent of Code is an annual online event where participants solve a series of programming puzzles released daily from December 1st until December 25th. Each puzzle is a fun and unique challenge designed to test problem-solving skills.

## Structure
This repository is organized to make navigation through the solutions as seamless as possible. 
Each day's puzzle solution is in its respective folder, named `DayXX`, where `XX` is the day of the month.

- `Day01`
- `Day02`
- `...`
- `Day25`

Within each folder, you'll find:

- `README.md`: A brief description of the day's problem.
- Source code files: My solution for the day's puzzle, typically in Python or Rust
- `input.txt`: The input data provided for the puzzle.
- Additional resources or notes if applicable.

## My Approach
For Advent of Code 2023, I've decided to primarily use Python due to its readability and the extensive libraries available, which make it an excellent choice for solving diverse and complex problems quickly. In each solution, I focus not only on solving the problem but also on writing clean, efficient, and well-documented code.

## Progress
Here I'll track my progress throughout the event. 
I aim to complete each day's puzzle on the same day, but as with any challenge, there might be some delays.

## Progress

| Day | Part One | Part Two | Reflections |
|-----|----------|----------|-------------|
| 01  | ✅       | ✅       | [Day01 README](/Day01/README.md) |
| 02  | ❓       | ❓       | [Day02 README](/Day02/README.md) |
| ... | ...      | ...      | ...         |
| 25  | ❓       | ❓       | [Day25 README](/Day25/README.md) |

- ✅ Completed
- ❓ Not Started / In Progress

## Running the Solutions
Each solution is a standalone script. 

## Python
To run any of the solutions, navigate to the respective day's directory and run the script using a Python interpreter. 
For example:

```bash
cd Day01/python
python3 part2.py test.txt # for testing
python3 part2.py
```

Make sure you have Python installed on your machine. The solutions are developed using Python 3.x.

## Rust
For Rust you have to use the rust project generated in each Day. 
Make sure you have Rust and Cargo installed.
You can either test or run the solution:

```bash
cd Day01/rust
cargo test #running tests
cargo run
```

## JavaScript
Using solutions in JavaScript requires NodeJS installed on your system. Then:
```bash
cd Day01/js
node solution.js
```

## TypeScript
Normally you can use compile the TS file to JS using the tsc compiler. But for ease in this simple scripts i suggest installing: `npm install -g typescript ts-node`. With this you can just run the TS file at once and get the output without compiling and running over and over.
```bash
cd Day01/ts
ts-node solution.ts
```

## Feedback and Collaboration
I'm always open to feedback and suggestions for improving the solutions. 
If you have ideas or find an issue, feel free to open an issue or submit a pull request.
