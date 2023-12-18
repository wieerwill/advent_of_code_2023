def parse_instructions(file_path):
    """Parse instructions from the given file."""
    try:
        with open(file_path, 'r') as file:
            instructions = [line.strip().split() for line in file.readlines()]
            print(f"Parsed {len(instructions)} instructions from {file_path}")
            return instructions
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise

def apply_instruction(grid, position, direction, steps):
    """Apply a single instruction to the grid and update the position."""
    deltas = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    dx, dy = deltas[direction]
    for _ in range(steps):
        position = (position[0] + dx, position[1] + dy)
        grid.add(position)
        #print(f"Moved {direction} to {position}")
    return position

def create_path(instructions):
    """Create the path based on the instructions."""
    grid = set()
    position = (0, 0)
    grid.add(position)

    for instruction in instructions:
        direction, steps = instruction[0], int(instruction[1])
        print(f"Applying instruction: {direction} {steps}")
        position = apply_instruction(grid, position, direction, steps)
    
    return grid

def flood_fill(grid, bounds):
    """Perform flood-fill to find cells outside the path."""
    filled = set()
    to_fill = [(bounds[0], y) for y in range(bounds[2], bounds[3] + 1)] \
            + [(bounds[1], y) for y in range(bounds[2], bounds[3] + 1)] \
            + [(x, bounds[2]) for x in range(bounds[0], bounds[1] + 1)] \
            + [(x, bounds[3]) for x in range(bounds[0], bounds[1] + 1)]

    while to_fill:
        x, y = to_fill.pop()
        if (x, y) in filled or (x, y) in grid:
            continue
        filled.add((x, y))
        if x > bounds[0]: to_fill.append((x - 1, y))
        if x < bounds[1]: to_fill.append((x + 1, y))
        if y > bounds[2]: to_fill.append((x, y - 1))
        if y < bounds[3]: to_fill.append((x, y + 1))

    return filled

def calculate_area(grid):
    """Calculate the area inside the loop."""
    min_x = min(grid, key=lambda x: x[0])[0]
    max_x = max(grid, key=lambda x: x[0])[0]
    min_y = min(grid, key=lambda x: x[1])[1]
    max_y = max(grid, key=lambda x: x[1])[1]
    bounds = (min_x, max_x, min_y, max_y)

    outside_area = flood_fill(grid, bounds)
    total_area = (max_x - min_x + 1) * (max_y - min_y + 1)
    inside_area = total_area - len(outside_area)

    return inside_area

def run_test(test_file):
    """Run the algorithm with test input."""
    try:
        instructions = parse_instructions(test_file)
        grid = create_path(instructions)
        area = calculate_area(grid)
        assert area == 62, f"Test failed. Expected 62 but got {area} with grid {grid}"
        print("Test passed successfully.")
        return True
    except AssertionError as e:
        print(f"Assertion Error: {e}")
        return False

def main():
    """Main function to run the puzzle solution."""
    test_file = "../test.txt"
    input_file = "../input.txt"

    # Run test
    if run_test(test_file):
        # Process actual puzzle input
        try:
            instructions = parse_instructions(input_file)
            grid = create_path(instructions)
            area = calculate_area(grid)
            print(f"Puzzle result (area): {area}")
        except Exception as e:
            print(f"Error during puzzle execution: {e}")
    else:
        print("Test failed. Halting execution.")

if __name__ == "__main__":
    main()