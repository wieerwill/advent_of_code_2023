def parse_line(line):
    """
    Parse a line into spring states and group sizes.
    """
    try:
        parts = line.strip().split()
        states = parts[0]
        group_sizes = [int(x) for x in parts[1].split(',')]
        return states, group_sizes
    except Exception as e:
        print(f"Error parsing line '{line}': {e}")
        raise

def is_valid_configuration(states, group_sizes):
    """
    Check if a given configuration of springs is valid based on group sizes.
    """
    try:
        i, size_index = 0, 0
        while i < len(states):
            if states[i] == '#':
                if size_index >= len(group_sizes):
                    return False  # More broken springs than groups

                count = 0
                while i < len(states) and states[i] == '#':
                    count += 1
                    i += 1

                if count != group_sizes[size_index]:
                    return False  # Group size mismatch
                size_index += 1
            else:
                i += 1

        return size_index == len(group_sizes)  # All groups must be accounted for
    except Exception as e:
        print(f"Error in is_valid_configuration: {e}")
        raise

def count_configurations(states, group_sizes, index=0, memo=None):
    """
    Count the number of valid configurations using backtracking and memoization.
    """
    if memo is None:
        memo = {}

    key = (tuple(states), index)
    if key in memo:
        return memo[key]

    if index == len(states):
        memo[key] = 1 if is_valid_configuration(states, group_sizes) else 0
        return memo[key]

    if states[index] != '?':
        memo[key] = count_configurations(states, group_sizes, index + 1, memo)
        return memo[key]

    count = 0
    for state in ['.', '#']:
        states[index] = state
        count += count_configurations(states, group_sizes, index + 1, memo)
        states[index] = '?'

    memo[key] = count
    return count

def solve_puzzle(file_path):
    """
    Solve the puzzle for each line in the file and return the total count of configurations.
    """
    try:
        total_count = 0
        with open(file_path, 'r') as file:
            for line in file:
                states, group_sizes = parse_line(line)
                count = count_configurations(list(states), group_sizes)
                total_count += count
                print(f"Line: {line.strip()}, Possible Configurations: {count}")
        return total_count
    except Exception as e:
        print(f"Error in solve_puzzle: {e}")
        raise

def test():
    """
    Test the solution with a test file.
    """
    print("Running tests...")
    test_result = solve_puzzle("../test.txt")
    print(f"Test Result: {test_result}")
    assert test_result == 21, f"Test failed, expected 21, got {test_result}"
    print("Test passed successfully.")

def main():
    """
    Main function to run the test and then solve the puzzle.
    """
    try:
        test()
        result = solve_puzzle("../input.txt")
        print(f"Final Result: {result}")
    except Exception as e:
        print(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main()
