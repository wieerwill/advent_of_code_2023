import sys


def parse_input(file_path):
    """Parse the input file into workflows and parts."""
    with open(file_path) as file:
        rules, parts = file.read().strip().split("\n\n")

    workflows = {}
    for rule in rules.split("\n"):
        name, rest = rule.split("{")
        workflows[name] = rest[:-1]

    return workflows, parts.split("\n")


def parse_conditions(rule):
    """Parse the conditions and results from a rule string."""
    conditions = []
    for cmd in rule.split(","):
        if ":" in cmd:
            condition, result = cmd.split(":")
            conditions.append((condition, result))
        else:
            conditions.append((None, cmd))
    return conditions


def accepted(workflows, part):
    """Determine if a part is accepted by the workflows."""
    state = "in"
    while True:
        conditions = parse_conditions(workflows[state])
        for condition, result in conditions:
            if not condition or evaluate_condition(part, condition):
                if result == "A":
                    return True
                elif result == "R":
                    return False
                state = result
                break


def evaluate_condition(part, condition):
    """Evaluate a condition against a part's attributes."""
    var, op, n = condition[0], condition[1], int(condition[2:])
    if op == ">":
        return part[var] > n
    else:
        return part[var] < n


def calculate_sum_of_accepted_parts(workflows, parts):
    """Calculate the sum of all accepted parts."""
    total_sum = 0
    for part_str in parts:
        part = parse_part(part_str)
        if accepted(workflows, part):
            total_sum += sum(part.values())
    return total_sum


def parse_part(part_str):
    """Parse a part string into a dictionary of attributes."""
    part_str = part_str[1:-1]
    return {x.split("=")[0]: int(x.split("=")[1]) for x in part_str.split(",")}


def test_algorithm():
    """Test the algorithm with the test input."""
    workflows, parts = parse_input("../test.txt")
    expected_result = 19114  # Expected result from the test input
    result = calculate_sum_of_accepted_parts(workflows, parts)
    assert (
        result == expected_result
    ), f"Test failed: Expected {expected_result}, got {result}"
    print("Test passed successfully.")


def main():
    """Main function to run the algorithm."""
    try:
        test_algorithm()  # Run the test first
        workflows, parts = parse_input("../input.txt")
        result = calculate_sum_of_accepted_parts(workflows, parts)
        print(f"Result for the puzzle input: {result}")
    except AssertionError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
