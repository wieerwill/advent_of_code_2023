def parse_instructions(file_path):
    """Parse instructions from the given file."""
    try:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
        print(f"Parsed {len(lines)} instructions from {file_path}")
        return lines
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise


def calculate_area(lines):
    """Calculate the area inside the loop defined by the instructions."""
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    points = [(0, 0)]
    boundary = 0

    for line in lines:
        *_, color = line.split()
        instructions = color[2:-1]
        dr, dc = DIRECTIONS[int(instructions[-1])]
        steps = int(instructions[:-1], 16)
        boundary += steps
        row, column = points[-1]
        points.append((row + dr * steps, column + dc * steps))

    area = (
        abs(
            sum(
                x1 * y2 - x2 * y1
                for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])
            )
        )
        // 2
        + boundary // 2
        + 1
    )

    return area


def run_test(test_file, expected_result):
    """Run the algorithm with test input and compare with the expected result."""
    try:
        lines = parse_instructions(test_file)
        calculated_area = calculate_area(lines)
        assert (
            calculated_area == expected_result
        ), f"Test failed, expected {expected_result}, got {calculated_area}"
        print(f"Test passed, area: {calculated_area}")
    except AssertionError as e:
        print(e)
        raise
    except Exception as e:
        print(f"Error during test execution: {e}")
        raise


def main():
    """Main function to run the puzzle solution."""
    test_file = "../test.txt"
    input_file = "../input.txt"
    expected_test_area = (
        952408144115  # Replace with the correct expected area for the test
    )

    # Run test
    try:
        run_test(test_file, expected_test_area)

        # Process actual puzzle input
        lines = parse_instructions(input_file)
        area = calculate_area(lines)
        print(f"Puzzle result (area): {area}")
    except Exception as e:
        print(f"Execution halted due to error: {e}")


if __name__ == "__main__":
    main()
