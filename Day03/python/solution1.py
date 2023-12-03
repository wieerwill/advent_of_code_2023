import os

def parse_schematic(file_path):
    """Reads the engine schematic from a file and returns it as a list of strings."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")

def is_symbol(char):
    """Checks if a character is a symbol (not a digit or a period)."""
    return not char.isdigit() and char != '.'

def get_adjacent_positions(rows, cols, row, col):
    """Generates positions adjacent (including diagonally) to the given coordinates."""
    for i in range(max(0, row - 1), min(row + 2, rows)):
        for j in range(max(0, col - 1), min(col + 2, cols)):
            if i != row or j != col:
                yield i, j

def find_start_of_number(schematic, row, col):
    """Finds the start position of the number that includes the given digit."""
    while col > 0 and schematic[row][col - 1].isdigit():
        col -= 1
    return row, col

def extract_full_number(schematic, start_row, start_col):
    """Extracts the full number starting from the given digit coordinates."""
    start_row, start_col = find_start_of_number(schematic, start_row, start_col)
    number = ''
    rows, cols = len(schematic), len(schematic[0])
    col = start_col

    while col < cols and schematic[start_row][col].isdigit():
        number += schematic[start_row][col]
        schematic[start_row] = schematic[start_row][:col] + '.' + schematic[start_row][col + 1:]
        col += 1

    return int(number) if number else 0

def sum_part_numbers(file_path):
    """Calculates the sum of all part numbers in the engine schematic."""
    schematic = parse_schematic(file_path)
    total_sum = 0
    visited = set()

    for row in range(len(schematic)):
        for col in range(len(schematic[row])):
            if is_symbol(schematic[row][col]):
                for i, j in get_adjacent_positions(len(schematic), len(schematic[row]), row, col):
                    if schematic[i][j].isdigit() and (i, j) not in visited:
                        visited.add((i, j))
                        number = extract_full_number(schematic, i, j)
                        print(f"Found number {number} at line {i+1}")
                        total_sum += number

    return total_sum

def run_tests():
    """Runs tests on the test file and prints the results."""
    test_result = sum_part_numbers("../test.txt")
    print(f"Test Result: {test_result}")
    assert test_result == 4361, f"Test failed: Expected 4361, got {test_result}"

def main():
    """Main function to run the test and then process the input file."""
    try:
        run_tests()
        print("Test passed successfully.")
        final_result = sum_part_numbers("../input.txt")
        print(f"Final Result: {final_result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
