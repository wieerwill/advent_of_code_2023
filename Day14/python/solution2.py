def read_grid(file_path):
    """Reads the grid from a file and returns it as a 2D list."""
    try:
        with open(file_path, "r") as file:
            grid = [list(line.strip()) for line in file]
        return grid
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise


def tilt_grid(grid, direction):
    """Tilts the grid in the specified direction and moves the rounded rocks."""
    rows, cols = len(grid), len(grid[0])

    # North: Move rocks upwards
    if direction == "north":
        for col in range(cols):
            for row in range(1, rows):
                if grid[row][col] == "O":
                    target_row = row
                    while target_row > 0 and grid[target_row - 1][col] == ".":
                        target_row -= 1
                    if target_row != row:
                        grid[target_row][col], grid[row][col] = (
                            grid[row][col],
                            grid[target_row][col],
                        )

    # West: Move rocks to the left
    elif direction == "west":
        for row in range(rows):
            for col in range(1, cols):
                if grid[row][col] == "O":
                    target_col = col
                    while target_col > 0 and grid[row][target_col - 1] == ".":
                        target_col -= 1
                    if target_col != col:
                        grid[row][target_col], grid[row][col] = (
                            grid[row][col],
                            grid[row][target_col],
                        )

    # South: Move rocks downwards
    elif direction == "south":
        for col in range(cols):
            for row in range(rows - 2, -1, -1):  # Start from the second last row
                if grid[row][col] == "O":
                    target_row = row
                    while target_row < rows - 1 and grid[target_row + 1][col] == ".":
                        target_row += 1
                    if target_row != row:
                        grid[target_row][col], grid[row][col] = (
                            grid[row][col],
                            grid[target_row][col],
                        )

    # East: Move rocks to the right
    elif direction == "east":
        for row in range(rows):
            for col in range(cols - 2, -1, -1):  # Start from the second last column
                if grid[row][col] == "O":
                    target_col = col
                    while target_col < cols - 1 and grid[row][target_col + 1] == ".":
                        target_col += 1
                    if target_col != col:
                        grid[row][target_col], grid[row][col] = (
                            grid[row][col],
                            grid[row][target_col],
                        )


def run_spin_cycles(grid, cycles):
    """Runs the specified number of spin cycles on the grid."""
    for _ in range(cycles):
        for direction in ["north", "west", "south", "east"]:
            tilt_grid(grid, direction)
            # Implement pattern detection or optimization here if needed


def run_simulation_with_cycles(file_path, cycles):
    """Runs the simulation with spin cycles and returns the total load."""
    try:
        grid = read_grid(file_path)
        actual_cycles = run_spin_cycles_with_optimization(grid, cycles)
        total_load = calculate_load(grid)
        return total_load
    except Exception as e:
        print(f"Error during simulation for file {file_path}: {e}")
        raise


def grid_to_string(grid):
    """Converts the grid to a string for easy comparison."""
    return "\n".join("".join(row) for row in grid)


def run_spin_cycles_with_optimization(grid, max_cycles):
    """Runs spin cycles on the grid with optimizations for large cycle numbers."""
    seen_states = set()
    for cycle in range(max_cycles):
        previous_state = grid_to_string(grid)

        if previous_state in seen_states:
            print(f"Repeating state detected at cycle {cycle}. Exiting early.")
            break

        seen_states.add(previous_state)

        for direction in ["north", "west", "south", "east"]:
            tilt_grid(grid, direction)

    return cycle  # Return the number of cycles actually run


def test_simulation_with_cycles():
    """Tests the simulation with spin cycles."""
    test_file = "../test.txt"
    expected_load_after_cycles = 64  # Expected load after cycles in the test case

    print("Running test simulation with cycles...")
    actual_load = run_simulation_with_cycles(test_file, 1000000000)
    print(f"Test simulation load after cycles: {actual_load}")

    assert (
        actual_load == expected_load_after_cycles
    ), f"Test failed: expected {expected_load_after_cycles}, got {actual_load}"
    print("Test passed successfully.")


def main():
    """Main function to run the test and then the actual simulation with cycles."""
    try:
        test_simulation_with_cycles()
        input_file = "../input.txt"
        cycles = 1000000000
        print("\nRunning actual simulation with cycles...")
        grid = read_grid(input_file)
        actual_cycles = run_spin_cycles_with_optimization(grid, cycles)
        total_load = calculate_load(grid)
        # total_load = run_simulation_with_cycles(input_file, cycles)
        print(f"Total load from actual simulation with cycles: {total_load}")
    except Exception as e:
        print(f"Error in main function: {e}")


# Run the main function
if __name__ == "__main__":
    main()
