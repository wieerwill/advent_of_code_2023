import os

def parse_schematic(file_path):
    """Reads the engine schematic from a file and returns it as a list of strings."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")

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

def find_gears_and_calculate_ratios(schematic):
    """Finds gears in the schematic and calculates their gear ratios."""
    total_ratio_sum = 0
    rows, cols = len(schematic), len(schematic[0])

    for row in range(rows):
        for col in range(cols):
            if schematic[row][col] == '*':
                part_numbers = []
                for i, j in get_adjacent_positions(rows, cols, row, col):
                    if schematic[i][j].isdigit():
                        part_number = extract_full_number(schematic, i, j)
                        if part_number not in part_numbers:
                            part_numbers.append(part_number)

                if len(part_numbers) == 2:
                    gear_ratio = part_numbers[0] * part_numbers[1]
                    total_ratio_sum += gear_ratio
                    print(f"Found gear at line {row + 1} with ratio {gear_ratio}")

    return total_ratio_sum

def run_tests():
    """Runs tests on the test file and prints the results."""
    test_schematic = parse_schematic("../test.txt")
    test_result = find_gears_and_calculate_ratios(test_schematic)
    print(f"Test Result: {test_result}")
    assert test_result == 467835, "Test failed: Expected 467835"

def main():
    """Main function to process the input file and calculate the sum of gear ratios."""
    try:
        run_tests()
        print("Test passed successfully.")
        schematic = parse_schematic("../input.txt")
        total_ratio_sum = find_gears_and_calculate_ratios(schematic)
        print(f"Total sum of gear ratios: {total_ratio_sum}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
