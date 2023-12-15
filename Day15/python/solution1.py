def hash_algorithm(step):
    """Calculate HASH value for a given step."""
    current_value = 0
    for char in step:
        current_value += ord(char)  # Convert char to ASCII and add to current value
        current_value *= 17  # Multiply by 17
        current_value %= 256  # Modulo 256
    return current_value

def process_file(file_path):
    """Process each step in the file and return the sum of HASH values."""
    try:
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', '')  # Remove newline characters
            steps = data.split(',')  # Split steps by comma
            print(f"Processing {len(steps)} steps from {file_path}")

            total_sum = 0
            for step in steps:
                hash_result = hash_algorithm(step)
                total_sum += hash_result
                print(f"Step: {step}, HASH: {hash_result}")

            return total_sum
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

def test_algorithm():
    """Test the algorithm with the test file."""
    test_result = process_file("../test.txt")
    print(f"Test Result: {test_result}")
    assert test_result == 1320, "Test failed. Expected result is 1320."

def main():
    """Main function to run the HASH algorithm on the input file."""
    try:
        # Run test first
        test_algorithm()
        print("Test passed. Proceeding with main input file.")

        # Process main input file
        final_result = process_file("../input.txt")
        print(f"Final Result: {final_result}")
    except AssertionError as ae:
        print(ae)
    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()
