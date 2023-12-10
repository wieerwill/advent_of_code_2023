def parse_input(file_path):
    """Parse the input file into race times and record distances."""
    with open(file_path, "r") as file:
        lines = file.readlines()
        times = [int(value) for value in lines[0].strip().split() if value.isdigit()]
        distances = [
            int(value) for value in lines[1].strip().split() if value.isdigit()
        ]
    print(f"Input parsed. Times: {times}, Distances: {distances}")
    return times, distances


def calculate_winning_ways(time, record):
    """Calculate the number of ways to beat the record for a single race."""
    print(f"Calculating winning ways for time: {time}, record: {record}")
    winning_ways = 0
    # Check hold times from 0 up to (time - 1)
    for hold_time in range(time):
        speed = hold_time
        remaining_time = time - hold_time
        distance = speed * remaining_time
        print(
            f"Hold Time: {hold_time}, Speed: {speed}, Remaining Time: {remaining_time}, Distance: {distance}"
        )
        # Count as winning way if distance is greater than the record
        if distance > record:
            winning_ways += 1
    print(f"Winning ways for this race: {winning_ways}")
    return winning_ways


def total_winning_combinations(times, distances):
    """Calculate the total number of winning combinations for all races."""
    print("Calculating total winning combinations.")
    total_combinations = 1
    for time, record in zip(times, distances):
        winning_ways = calculate_winning_ways(time, record)
        if winning_ways == 0:
            print("No winning way for a race. Exiting.")
            return 0  # Early exit if no winning way for a race
        total_combinations *= winning_ways
    print(f"Total winning combinations: {total_combinations}")
    return total_combinations


def run_test(file_path):
    """Run the test with assertions to verify the functionality."""
    print(f"Running test with file: {file_path}")
    times, distances = parse_input(file_path)
    result = total_winning_combinations(times, distances)
    print(f"Test result: {result}")
    assert result == 288, f"Test failed! Expected 288, got {result}"
    print("Test passed successfully.")


def main():
    """Main function to run the test and then process the input file."""
    try:
        test_file_path = "../test.txt"
        run_test(test_file_path)

        input_file_path = "../input.txt"
        print(f"\nProcessing input file: {input_file_path}")
        times, distances = parse_input(input_file_path)
        result = total_winning_combinations(times, distances)
        print(f"Final result from input file: {result}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except AssertionError as e:
        print(f"Assertion Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
