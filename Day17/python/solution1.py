from heapq import heappush, heappop

# Constants for movement directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def read_grid(filename):
    """
    Reads the grid of numbers from the given file.
    """
    with open(filename) as f:
        return [tuple(map(int, line.strip())) for line in f.readlines()]


def is_valid_position(row, col, grid):
    """
    Checks if the given position is within the bounds of the grid.
    """
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def find_least_heat_loss(grid):
    """
    Finds the path with the least heat loss in the given grid.
    """
    queue = [(0, 0, 0, 0, 0, 0)]  # heat_loss, row, col, dr, dc, n
    seen = set()

    while queue:
        heat_loss, row, col, dr, dc, n = heappop(queue)

        # Check if destination is reached
        if row == len(grid) - 1 and col == len(grid[0]) - 1:
            return heat_loss

        if (row, col, dr, dc, n) in seen:
            continue

        seen.add((row, col, dr, dc, n))

        # Continue in the same direction if not moved more than 3 blocks
        if n < 3 and (dr, dc) != (0, 0):
            new_row, new_col = row + dr, col + dc
            if is_valid_position(new_row, new_col, grid):
                heappush(
                    queue,
                    (
                        heat_loss + grid[new_row][new_col],
                        new_row,
                        new_col,
                        dr,
                        dc,
                        n + 1,
                    ),
                )

        # Explore adjacent directions, avoiding immediate reversals
        for new_dr, new_dc in DIRECTIONS:
            if (new_dr, new_dc) in ((dr, dc), (-dr, -dc)):
                continue

            new_row, new_col = row + new_dr, col + new_dc
            if is_valid_position(new_row, new_col, grid):
                heappush(
                    queue,
                    (
                        heat_loss + grid[new_row][new_col],
                        new_row,
                        new_col,
                        new_dr,
                        new_dc,
                        1,
                    ),
                )

    return -1  # Return -1 if no path is found


def test_algorithm():
    """
    Tests the algorithm with test data and asserts the correct output.
    """
    test_grid = read_grid("../test.txt")
    expected_result = 102  # Expected heat loss
    result = find_least_heat_loss(test_grid)
    assert (
        result == expected_result
    ), f"Test failed: Expected {expected_result}, got {result}"
    print("Test passed successfully!")


def main():
    """
    Main function to run the puzzle solution.
    """
    try:
        # Run test first
        test_algorithm()

        # If test passes, run the main puzzle
        grid = read_grid("../input.txt")
        result = find_least_heat_loss(grid)
        print(f"Least heat loss for the main puzzle: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
