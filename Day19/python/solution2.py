import math
import sys
from itertools import groupby


def parse_input(file_path):
    """Parse input file to extract workflows."""
    with open(file_path) as f:
        lines = f.read().splitlines()

    workflows_raw, _ = [
        tuple(group) for not_empty, group in groupby(lines, bool) if not_empty
    ]

    workflows = {}
    for workflow in workflows_raw:
        name, rules_str = workflow.split("{")
        rules = rules_str[:-1].split(",")
        workflows[name] = ([], rules.pop())
        for rule in rules:
            condition, target = rule.split(":")
            key, comparison, *value = tuple(condition)
            workflows[name][0].append((key, comparison, int("".join(value)), target))

    return workflows


def count_ranges(workflows, ranges, name="in"):
    """Count the number of valid ranges recursively."""
    if name == "R":
        return 0
    if name == "A":
        return math.prod(stop - start + 1 for start, stop in ranges.values())

    rules, fallback = workflows[name]
    total = 0
    for key, comparison, value, target in rules:
        start, stop = ranges[key]

        if comparison == "<":
            t_start, t_stop = start, value - 1
            f_start, f_stop = value, stop
        else:
            t_start, t_stop = value + 1, stop
            f_start, f_stop = start, value

        if t_start <= t_stop:
            total += count_ranges(workflows, {**ranges, key: (t_start, t_stop)}, target)
        if f_start <= f_stop:
            ranges[key] = (f_start, f_stop)
        else:
            break
    else:
        total += count_ranges(workflows, ranges, fallback)

    return total


def test_algorithm():
    """Run the algorithm on a test file and compare the result."""
    test_file = "../test.txt"
    expected_result = 167409079868000
    workflows = parse_input(test_file)
    result = count_ranges(workflows, {category: (1, 4000) for category in "xmas"})
    assert (
        result == expected_result
    ), f"Test failed: Expected {expected_result}, got {result}"
    print("Test passed successfully.")


def main():
    """Main function to execute the algorithm."""
    try:  # Expected result for the test input
        print("Running test...")
        test_algorithm()

        print("Test passed. Running on actual input...")
        input_file = "../input.txt"
        workflows = parse_input(input_file)
        result = count_ranges(workflows, {category: (1, 4000) for category in "xmas"})
        print(f"Result for the puzzle input: {result}")
    except AssertionError as e:
        print(f"Assertion Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
