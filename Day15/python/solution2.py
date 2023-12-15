import re
from collections import defaultdict


def hash_label(label):
    """Compute hash value for a given label."""
    value = 0
    for char in label:
        value = (value + ord(char)) * 17 % 256
    return value


def process_file(file_path):
    """Process the file and return the total focusing power."""
    try:
        with open(file_path, "r") as file:
            line = file.read().replace("\n", "")

        boxes = defaultdict(list)
        focal_lengths = {}

        for label, operation, focal_length in re.findall(r"([a-z]+)([=-])(\d)?", line):
            hashed = hash_label(label)
            destination = boxes[hashed]

            print(f"Processing step: {label}{operation}{focal_length}, Box: {hashed}")

            if operation == "=":
                if label not in destination:
                    destination.append(label)
                focal_lengths[label] = int(focal_length)
            else:
                if label in destination:
                    destination.remove(label)
                focal_lengths.pop(label, None)

        total_power = sum(
            (box_number + 1) * (i + 1) * focal_lengths[label]
            for box_number, labels in boxes.items()
            for i, label in enumerate(labels)
        )

        return total_power
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def test_algorithm():
    """Test the algorithm with the test file."""
    test_result = process_file("../test.txt")
    print(f"Test Result: {test_result}")
    assert (
        test_result == 145
    ), f"Test failed. Expected result is 145, got {test_result}."


def main():
    """Main function to run the algorithm on the input file."""
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
