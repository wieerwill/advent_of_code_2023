def parse_input(file_path):
    """
    Parse the input file to extract the race time and record distance.
    Assumes the file has two lines: first for time, second for distance.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        time = int("".join(filter(str.isdigit, lines[0].strip())))
        distance = int("".join(filter(str.isdigit, lines[1].strip())))
    print(f"Parsed input from {file_path} - Time: {time}, Distance: {distance}")
    return time, distance


def calculate_winning_ways(time, record):
    """
    Calculate the number of ways to beat the record for the race.
    Uses a mathematical approach to find the range of hold times that beat the record.
    """
    print(f"Calculating winning ways for Time: {time}, Record: {record}")
    # Correcting the calculation for min_hold_time and max_hold_time
    min_hold_time = 0
    while min_hold_time * (time - min_hold_time) <= record and min_hold_time < time:
        min_hold_time += 1
    max_hold_time = time - 1
    while max_hold_time * (time - max_hold_time) <= record and max_hold_time >= 0:
        max_hold_time -= 1

    winning_ways = max(0, max_hold_time - min_hold_time + 1)
    print(
        f"Winning ways calculated: {winning_ways} (Min: {min_hold_time}, Max: {max_hold_time})"
    )
    return winning_ways


def run_test(file_path, expected_result):
    """
    Run a test with the given file and compare the result to the expected result.
    """
    print(f"Running test with file: {file_path}")
    time, record = parse_input(file_path)
    result = calculate_winning_ways(time, record)
    print(f"Test result: {result}")
    assert (
        result == expected_result
    ), f"Test failed! Expected {expected_result}, got {result}"
    print("Test passed successfully.")


def main():
    """
    Main function to run the test and then process the actual input file.
    """
    try:
        test_file_path = "../test.txt"
        expected_test_result = 71503  # Expected result from the test file
        run_test(test_file_path, expected_test_result)

        input_file_path = "../input.txt"
        print(f"\nProcessing input file: {input_file_path}")
        time, record = parse_input(input_file_path)
        result = calculate_winning_ways(time, record)
        print(f"Final result from input file: {result}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except AssertionError as e:
        print(f"Assertion Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
