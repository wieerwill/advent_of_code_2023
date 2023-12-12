import sys


def read_grid(file_path):
    """Reads the grid from the file and returns it as a 2D list."""
    try:
        with open(file_path, "r") as file:
            return [list(line.strip()) for line in file]
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)


def find_empty_rows_and_cols(grid):
    """Finds empty rows and columns in the grid."""
    empty_rows = [i for i, row in enumerate(grid) if "#" not in row]
    empty_cols = [j for j in range(len(grid[0])) if all(row[j] == "." for row in grid)]
    return empty_rows, empty_cols


def locate_galaxies(grid):
    """Locates the coordinates of galaxies in the grid."""
    return [
        (r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == "#"
    ]


def calculate_distances(grid, galaxies, expansion_factor):
    """Calculates the sum of distances between all pairs of galaxies."""
    empty_rows, empty_cols = find_empty_rows_and_cols(grid)
    total_distance = 0

    for i, (r1, c1) in enumerate(galaxies):
        for r2, c2 in galaxies[i:]:
            distance = abs(r2 - r1) + abs(c2 - c1)
            distance += sum(
                expansion_factor
                for er in empty_rows
                if min(r1, r2) <= er <= max(r1, r2)
            )
            distance += sum(
                expansion_factor
                for ec in empty_cols
                if min(c1, c2) <= ec <= max(c1, c2)
            )
            total_distance += distance

    return total_distance


def run_test():
    """Runs the test using the test file."""
    test_grid = read_grid("../test.txt")
    test_galaxies = locate_galaxies(test_grid)
    test_result = calculate_distances(test_grid, test_galaxies, 1)
    assert test_result == 374, f"Test failed: Expected 374, got {test_result}"
    print("Test passed successfully.")


def main():
    print("Starting puzzle solution...")

    grid = read_grid("../input.txt")
    galaxies = locate_galaxies(grid)

    for part2 in [False, True]:
        expansion_factor = 10**6 - 1 if part2 else 1
        print(f"Calculating distances for part {'2' if part2 else '1'}...")
        total_distance = calculate_distances(grid, galaxies, expansion_factor)
        print(f"Total distance for part {'2' if part2 else '1'}: {total_distance}")


if __name__ == "__main__":
    run_test()
    main()
