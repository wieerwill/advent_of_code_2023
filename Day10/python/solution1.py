def parse_grid(file_path):
    """Parses the grid from a file and returns the graph and starting position."""
    print(f"Parsing grid from file: {file_path}")
    grid = {}
    start = None
    try:
        with open(file_path, 'r') as file:
            for y, line in enumerate(file.read().splitlines()):
                for x, char in enumerate(line):
                    match char:
                        case "|":
                            grid[(y, x)] = {(y - 1, x), (y + 1, x)}
                        case "-":
                            grid[(y, x)] = {(y, x - 1), (y, x + 1)}
                        case "L":
                            grid[(y, x)] = {(y - 1, x), (y, x + 1)}
                        case "J":
                            grid[(y, x)] = {(y, x - 1), (y - 1, x)}
                        case "7":
                            grid[(y, x)] = {(y, x - 1), (y + 1, x)}
                        case "F":
                            grid[(y, x)] = {(y + 1, x), (y, x + 1)}
                        case "S":
                            start = (y, x)
                            grid[(y, x)] = {(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)}
                        case _:
                            pass

        if start is None:
            raise ValueError("Start position 'S' not found in the grid.")
        grid[start] = {dst for dst in grid[start] if start in grid.get(dst, set())}
        return grid, start
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except Exception as e:
        print(f"Error parsing grid: {str(e)}")
        raise

def find_cycle(grid, start):
    """Finds all nodes in the cycle starting from the starting position."""
    print(f"Finding cycle from start position: {start}")
    seen = {start}
    queue = [start]
    while queue:
        current = queue.pop(0)
        for dst in grid[current]:
            if dst not in seen:
                seen.add(dst)
                queue.append(dst)
    return seen

def bfs_distance(grid, start, target):
    """Performs BFS to find distance from start to target."""
    #print(f"Calculating BFS distance from {start} to {target}")
    queue = [(start, 0)]
    visited = set()
    while queue:
        current, distance = queue.pop(0)
        if current == target:
            return distance
        visited.add(current)
        for neighbor in grid[current]:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    return -1

def find_longest_distance(grid, cycle, start):
    """Finds the longest distance from the start in the cycle."""
    print("Finding longest distance from start in the cycle.")
    max_distance = 0
    for node in cycle:
        if node != start:
            distance = bfs_distance(grid, start, node)
            max_distance = max(max_distance, distance)
    return max_distance

def run(file_path):
    """Runs the entire algorithm for the given file path."""
    print(f"Running algorithm for file: {file_path}")
    grid, start = parse_grid(file_path)
    cycle = find_cycle(grid, start)
    longest_distance = find_longest_distance(grid, cycle, start)
    print(f"Longest distance: {longest_distance}")
    return longest_distance

def test():
    """Test function to validate the algorithm with a test file."""
    print("Starting test...")
    expected_result = 8  # Expected result for the test file
    result = run("../test.txt")
    assert result == expected_result, f"Test failed: Expected {expected_result}, got {result}"
    print("Test passed successfully.")

def main():
    """Main function to run the test and then the algorithm for the input file."""
    try:
        test()
        final_result = run("../input.txt")
        print(f"Final Result: {final_result}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
