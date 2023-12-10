def parse_file(file_path):
    """Parse the input file to extract instructions and the node map."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        instructions = lines[0].strip()
        node_map = {}
        for line in lines[2:]:
            node, neighbors = line.strip().split(" = ")
            node_map[node] = tuple(neighbors[1:-1].split(", "))

        return instructions, node_map
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        raise


def find_repeating_unit(sequence):
    """Find the repeating unit in a sequence."""
    for i in range(1, len(sequence) + 1):
        unit = sequence[:i]
        if sequence == unit * (len(sequence) // len(unit)):
            return unit
    return sequence


def navigate_network(instructions, node_map, start_node="AAA", end_node="ZZZ"):
    """Navigate the network based on the instructions and return the number of steps."""
    current_node = start_node
    steps = 0
    visited = set()
    instruction_index = 0
    instructions = find_repeating_unit(instructions)

    while current_node != end_node:
        if (current_node, instruction_index) in visited:
            print(
                f"Loop detected at {current_node} with instruction index {instruction_index}"
            )
            return -1  # Indicates a loop without reaching the end node

        visited.add((current_node, instruction_index))
        direction = instructions[instruction_index % len(instructions)]
        current_node = node_map[current_node][0 if direction == "L" else 1]
        instruction_index += 1
        steps += 1

    return steps


def run_test():
    """Run the test with the provided file path."""
    try:
        expected_result = 6
        instructions, node_map = parse_file("../test.txt")
        result = navigate_network(instructions, node_map)
        assert (
            result == expected_result
        ), f"Test failed, expected {expected_result} but got {result}"
        print(f"Test passed with {result} steps.")
    except AssertionError as error:
        print(error)


def main():
    print("Start Tests")
    run_test()

    try:
        print("Start input.txt")
        instructions, node_map = parse_file("../input.txt")
        result = navigate_network(instructions, node_map)
        if result == -1:
            print("Failed to reach the end node due to a loop.")
        else:
            print(f"Reached the end node in {result} steps.")
    except Exception as e:
        print(f"Error during main execution: {e}")


if __name__ == "__main__":
    main()
