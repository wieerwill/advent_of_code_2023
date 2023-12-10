def generate_difference_table(history):
    """Generates a difference table for a given history."""
    table = [history]
    while not all(value == 0 for value in table[-1]):
        try:
            next_row = [table[-1][i+1] - table[-1][i] for i in range(len(table[-1]) - 1)]
        except IndexError as e:
            print(f"IndexError in generate_difference_table: {e}")
            print(f"Current table: {table}")
            raise
        table.append(next_row)
    return table

def extrapolate_previous_value(table):
    """Extrapolates the previous value from the difference table."""
    try:
        for i in range(len(table) - 2, -1, -1):
            table[i].insert(0, table[i][0] - table[i+1][0])
    except IndexError as e:
        print(f"IndexError in extrapolate_previous_value: {e}")
        print(f"Current table: {table}")
        raise
    return table[0][0]

def solve_puzzle(filename):
    """Solves the puzzle by reading histories from the file and summing their extrapolated previous values."""
    total = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    history = [int(x) for x in line.split()]
                    diff_table = generate_difference_table(history)
                    prev_value = extrapolate_previous_value(diff_table)
                    total += prev_value
                except ValueError as e:
                    print(f"ValueError processing line '{line}': {e}")
                except IndexError as e:
                    print(f"IndexError processing line '{line}': {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: The file {filename} was not found.")
        raise
    except Exception as e:
        print(f"Unexpected error processing file {filename}: {e}")
        raise
    return total

def test():
    """Runs the test using the test.txt file and asserts the expected outcome for the second part of the puzzle."""
    expected = 2  # Expected result from the test data for the second part
    try:
        result = solve_puzzle("../test.txt")
        assert result == expected, f"Test failed: Expected {expected}, got {result}"
        print("Test passed successfully.")
    except AssertionError as e:
        print(e)
        raise

def main():
    """Main function to run the test and then solve the puzzle."""
    print("Running test for the second part...")
    test()
    print("Test completed. Solving the puzzle for the second part...")
    result = solve_puzzle("../input.txt")
    print(f"Puzzle result for the second part: {result}")

if __name__ == "__main__":
    main()
