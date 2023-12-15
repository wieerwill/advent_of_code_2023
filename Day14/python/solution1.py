def read_grid(file_path):
    """Reads the grid from a file and returns it as a 2D list."""
    try:
        with open(file_path, "r") as file:
            grid = [list(line.strip()) for line in file]
        return grid
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise


def move_rocks_north(grid):
    """Moves all rounded rocks 'O' north as far as possible."""
    rows = len(grid)
    cols = len(grid[0])

    for col in range(cols):
        for row in range(1, rows):  # Start from second row
            if grid[row][col] == "O":
                target_row = row
                while target_row > 0 and grid[target_row - 1][col] == ".":
                    target_row -= 1
                if target_row != row:
                    grid[target_row][col], grid[row][col] = (
                        grid[row][col],
                        grid[target_row][col],
                    )


def calculate_load(grid):
    """Calculates the total load on the north support beams."""
    rows = len(grid)
    total_load = 0

    for row in range(rows):
        for cell in grid[row]:
            if cell == "O":
                total_load += rows - row

    return total_load


def run_simulation(file_path):
    """Runs the rock-moving simulation and returns the total load."""
    try:
        grid = read_grid(file_path)
        print(f"Initial Grid from {file_path}:")
        for row in grid:
            print("".join(row))

        move_rocks_north(grid)

        print(f"Grid after moving rocks north from {file_path}:")
        for row in grid:
            print("".join(row))

        total_load = calculate_load(grid)
        return total_load
    except Exception as e:
        print(f"Error during simulation for file {file_path}: {e}")
        raise


def test_simulation():
    """Runs test simulation and asserts the expected output."""
    test_file = "../test.txt"
    expected_load = 136  # Expected load from the test case

    print("Running test simulation...")
    actual_load = run_simulation(test_file)
    print(f"Test simulation load: {actual_load}")

    assert (
        actual_load == expected_load
    ), f"Test failed: expected {expected_load}, got {actual_load}"
    print("Test passed successfully.")


def main():
    """Main function to run the test and then the actual simulation."""
    try:
        test_simulation()

        input_file = "../input.txt"
        print("\nRunning actual simulation...")
        total_load = run_simulation(input_file)
        print(f"Total load from actual simulation: {total_load}")
    except Exception as e:
        print(f"Error in main function: {e}")


# Run the main function
if __name__ == "__main__":
    main()
