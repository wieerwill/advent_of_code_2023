from collections import deque


def process_modules(filename, debug=False):
    """
    Reads the module configuration from a file, initializes the modules, and simulates the pulse propagation.
    Returns the product of total high and low pulses after 1000 button presses.
    """
    with open(filename) as f:
        lines = f.read().splitlines()

    modules = {}
    broadcaster = []
    for line in lines:
        left, right = line.split(" -> ")
        destinations = right.split(", ")
        if left == "broadcaster":
            broadcaster = destinations
            continue

        module_type = left[0]
        module_name = left[1:]
        modules[module_name] = [
            module_type,
            False if module_type == "%" else {},
            destinations,
        ]

    # Initialize conjunction modules with False for each input
    for name, (_, _, destinations) in modules.items():
        for destination in destinations:
            if destination in modules and modules[destination][0] == "&":
                modules[destination][1][name] = False

    low, high = 0, 0

    for iteration in range(1000):
        queue = deque([("broadcaster", target, False) for target in broadcaster])

        while queue:
            name, target, pulse = queue.popleft()

            if debug:
                print(
                    f"Iteration {iteration}: Processing {target}, Pulse: {'High' if pulse else 'Low'}"
                )

            if target not in modules:
                continue

            module = modules[target]

            if module[0] == "%":
                if pulse:
                    continue
                module[1] = not module[1]
                new_pulse = module[1]
            else:
                module[1][name] = pulse
                new_pulse = not all(module[1].values())

            for destination in module[2]:
                queue.append((target, destination, new_pulse))
                # Count pulses when they are sent
                if new_pulse:
                    high += 1
                else:
                    low += 1

            if debug:
                print(
                    f"Iteration {iteration}: {target} -> {'High' if new_pulse else 'Low'} to {module[2]}"
                )

    return low * high


def test():
    """
    Runs the process_modules function with the test input and checks if it meets the expected outcome.
    """
    expected_result = 11687500  # Replace with the expected result of the test input
    test_result = process_modules("../test.txt", debug=True)
    assert (
        test_result == expected_result
    ), f"Test failed: Expected {expected_result}, got {test_result}"
    print(f"Test passed with result: {test_result}")


def main():
    """
    Main function to run the test and then process the actual puzzle input.
    """
    try:
        print("Running test...")
        test()
        print("Test passed. Running main input...")
        result = process_modules("../input.txt")
        print(f"Puzzle result: {result}")
    except AssertionError as e:
        print(str(e))
        print("Stopping execution due to test failure.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
