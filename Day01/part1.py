def extract_calibration_value(line):
    """
    Extract the calibration value from a line of text.
    The calibration value is formed by combining the first digit and the last digit in the line.

    :param line: A string representing a line of text from the document.
    :return: The calibration value as an integer.
    """
    first_digit = None
    last_digit = None

    # Find the first digit in the line
    for char in line:
        if char.isdigit():
            first_digit = char
            break
    
    # Find the last digit in the line
    for char in reversed(line):
        if char.isdigit():
            last_digit = char
            break

    # Combine the first and last digits to form the calibration value
    if first_digit and last_digit:
        return int(first_digit + last_digit)
    else:
        return 0

def sum_calibration_values(filename):
    """
    Calculate the sum of all calibration values in the document.

    :param filename: The name of the file containing the document.
    :return: The sum of all calibration values.
    """
    total = 0

    # Open the file and process each line
    with open(filename, 'r') as file:
        for line in file:
            total += extract_calibration_value(line)

    return total

# Main execution
if __name__ == "__main__":
    filename = "coordinates.txt"
    total_calibration_value = sum_calibration_values(filename)
    print(f"Total Sum of Calibration Values: {total_calibration_value}")
