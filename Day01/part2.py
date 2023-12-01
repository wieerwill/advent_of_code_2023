def extract_digits(line):
    """Extracts all digits (as numbers) from the line in the order they appear."""
    digit_map = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }

    # Add single digit mappings
    digit_map.update({str(k): str(k) for k in range(10)})

    digits_found = []
    i = 0
    while i < len(line):
        matched = False
        for word, digit in digit_map.items():
            if line.startswith(word, i):
                digits_found.append(int(digit))
                i += len(word) - 1  # Advance the index
                matched = True
                break
        i += 1  # Move to the next character if no match

    return digits_found

def extract_calibration_value(line):
    """Extracts the calibration value from a line."""
    digits = extract_digits(line)
    if digits:
        return int(str(digits[0]) + str(digits[-1]))
    return 0

def sum_calibration_values(file_path):
    """Extracts calibration values from each line and sums them up."""
    total_sum = 0
    with open(file_path, 'r') as file:
        for line in file:
            calibration_value = extract_calibration_value(line.strip())
            if calibration_value:
                # Use the first and last found digit to form the calibration value
                total_sum += calibration_value
                print(f"Line: {line.strip()} - Calibration Value: {calibration_value}")
            else:
                print(f"Line: {line.strip()} - No digits found")

    return total_sum

# Main execution
if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    total_calibration_value = sum_calibration_values(filename)
    print(f"Total Sum of Calibration Values: {total_calibration_value}")
