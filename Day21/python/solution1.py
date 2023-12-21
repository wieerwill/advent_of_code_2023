from collections import deque

def read_grid(file_path):
    """Reads the grid from a file and returns it along with the starting position."""
    with open(file_path, 'r') as file:
        grid = [list(line.strip()) for line in file.readlines()]

    start = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
                break
        if start:
            break

    assert start is not None, "Starting position 'S' not found in the grid."
    print(f"Grid loaded from {file_path}. Start position: {start}")
    return grid, start

def bfs(grid, start):
    """Performs BFS on the grid to track the minimum steps to each plot."""
    printf("Start BFS")
    steps = 64
    queue = deque([(start[0], start[1], 0)])
    distances = {}
    while queue:
        x, y, step = queue.popleft()
        if step > steps:
            continue  # Skip plots that are more than 64 steps away
        if step == steps:
            distances[(x, y)] = step  # Only consider plots at exactly 64 steps
        else:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == '.' and (nx, ny) not in distances:
                    queue.append((nx, ny, step + 1))

    print(f"BFS completed. Number of plots visited: {len(distances)}")
    return distances

def count_reachable_plots(distances, steps):
    """Counts the number of plots reachable in exactly the given number of steps."""
    count = sum(1 for d in distances.values() if d == steps)
    print(f"Number of plots reachable in exactly {steps} steps: {count}")
    return count

def run_test():
    """Runs the algorithm with the test data and asserts the result."""
    print("Running test...")
    test_grid, test_start = read_grid("../test.txt")
    distances = bfs(test_grid, test_start)
    test_result = count_reachable_plots(distances, 64)
    assert test_result == 16, f"Test failed: Expected 16, got {test_result}"
    print("Test passed successfully.")

def main():
    """Main function to run the algorithm with the actual puzzle data."""
    try:
        run_test()
        grid, start = read_grid("../input.txt")
        distances = bfs(grid, start)
        result = count_reachable_plots(distances, 64)
        print(f"Final Result: Number of reachable plots in exactly 64 steps: {result}")
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
    except FileNotFoundError as fnfe:
        print(f"File not found error: {fnfe}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
