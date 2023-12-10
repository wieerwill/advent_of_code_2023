def parse_grid(file_path):
    """Parses the grid from a file and returns it as a 2D list."""
    try:
        with open(file_path, "r") as file:
            grid = [list(line.strip()) for line in file]
            print(f"Grid parsed from {file_path}:")
            [print("".join(row)) for row in grid]
            return grid
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise


def create_graph(grid):
    """Creates a graph from the grid."""
    graph = {}
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in "|-LJ7FS":
                graph[(r, c)] = get_neighbors(grid, r, c)
    print("Graph created from grid:")
    print(graph)
    return graph


def get_neighbors(grid, r, c):
    """Finds the neighbors of a cell in the grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    # Directions: North, East, South, West
    directions = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
    connected = {
        "|": [0, 2],
        "-": [1, 3],
        "L": [0, 1],
        "J": [0, 3],
        "7": [2, 3],
        "F": [1, 2],
        "S": [0, 1, 2, 3],  # 'S' connects in all directions for initial identification
    }

    for i, (dr, dc) in enumerate(directions):
        if 0 <= dr < rows and 0 <= dc < cols and grid[dr][dc] != ".":
            neighbor_type = grid[dr][dc]
            # Check if there is a valid connection
            if neighbor_type in connected:
                if (
                    i in connected[grid[r][c]] and (3 - i) in connected[neighbor_type]
                ):  # Check reverse direction
                    neighbors.append((dr, dc))

    print(f"Neighbors for ({r}, {c}): {neighbors}")
    return neighbors


def bfs(graph, start):
    """Performs BFS on the graph and returns the maximum distance from the start."""
    visited = set()
    queue = [(start, 0)]
    max_distance = 0
    while queue:
        node, distance = queue.pop(0)
        if node != start or len(visited) == 0:  # Allow revisiting start only initially
            visited.add(node)
            max_distance = max(max_distance, distance)
            print(f"Visited node: {node}, Distance: {distance}")
            for neighbor in graph[node]:
                if neighbor not in visited or (neighbor == start and len(visited) > 1):
                    queue.append((neighbor, distance + 1))
    print(f"Maximum distance from start: {max_distance}")
    return max_distance


def find_start(grid):
    """Finds the starting position 'S' in the grid."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                print(f"Starting position found at: ({r}, {c})")
                return r, c
    raise ValueError("Starting position 'S' not found in the grid")


def run_test(file_path):
    """Runs the algorithm on a test file and asserts the result."""
    print(f"Running test with file: {file_path}")
    grid = parse_grid(file_path)
    graph = create_graph(grid)
    start = find_start(grid)
    max_distance = bfs(graph, start)
    print(f"Max distance for test: {max_distance}")
    return max_distance


def main(file_path):
    """Main function to run the algorithm on the input file."""
    print(f"Running main algorithm with file: {file_path}")
    grid = parse_grid(file_path)
    graph = create_graph(grid)
    start = find_start(grid)
    max_distance = bfs(graph, start)
    print(f"Max distance for input: {max_distance}")
    return max_distance


if __name__ == "__main__":
    test_result = run_test("../test.txt")
    assert test_result == 8, f"Test failed: expected 8, got {test_result}"
    print(f"Test passed with {test_result}")

    input_result = main("../input.txt")
    print(f"Result for input file: {input_result}")
