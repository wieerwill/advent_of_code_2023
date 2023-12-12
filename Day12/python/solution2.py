import sys


def read_data(filepath):
    """Reads the data from the given file."""
    try:
        with open(filepath, "r") as file:
            return file.read().strip().split("\n")
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)


def unfold_record(record):
    """Unfolds the record according to the puzzle rules."""
    dots, blocks = record.split()
    dots = "?".join([dots] * 5)
    blocks = ",".join([blocks] * 5)
    return dots, [int(x) for x in blocks.split(",")]


def count_arrangements(dots, blocks, i=0, bi=0, current=0, memo=None):
    """Counts valid arrangements using dynamic programming."""
    if memo is None:
        memo = {}

    key = (i, bi, current)
    if key in memo:
        return memo[key]

    if i == len(dots):
        if bi == len(blocks) and current == 0:
            return 1
        elif bi == len(blocks) - 1 and blocks[bi] == current:
            return 1
        else:
            return 0

    ans = 0
    for c in [".", "#"]:
        if dots[i] == c or dots[i] == "?":
            if c == ".":
                if current == 0:
                    ans += count_arrangements(dots, blocks, i + 1, bi, 0, memo)
                elif current > 0 and bi < len(blocks) and blocks[bi] == current:
                    ans += count_arrangements(dots, blocks, i + 1, bi + 1, 0, memo)
            elif c == "#":
                ans += count_arrangements(dots, blocks, i + 1, bi, current + 1, memo)

    memo[key] = ans
    return ans


def solve_puzzle(lines):
    """Solves the puzzle for the given input lines."""
    total = 0
    for line in lines:
        print(f"Processing: {line}")
        dots, blocks = unfold_record(line)
        total += count_arrangements(dots, blocks)
    return total


def test_puzzle():
    """Runs the puzzle solution on test data."""
    test_data = read_data("../test.txt")
    print("Running tests...")
    test_result = solve_puzzle(test_data)
    print(f"Test result: {test_result}")
    assert test_result == 525152, "Test failed!"
    print("Test passed.")


def main():
    """Main function to run the puzzle solution."""
    test_puzzle()

    input_data = read_data("../input.txt")
    print("Processing input data...")
    result = solve_puzzle(input_data)
    print(f"Final result: {result}")


if __name__ == "__main__":
    main()
