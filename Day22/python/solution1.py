import sys

def parse_input(file_path):
    """Reads the input from a file and returns it as a list of bricks."""
    print("Parsing input...")
    try:
        with open(file_path, "r") as file:
            bricks = []
            for line in file:
                st, ed = line.split('~')
                sx, sy, sz = [int(x) for x in st.split(',')]
                ex, ey, ez = [int(x) for x in ed.split(',')]
                brick = []
                if sx == ex and sy == ey:
                    assert sz <= ez
                    for z in range(sz, ez + 1):
                        brick.append((sx, sy, z))
                elif sx == ex and sz == ez:
                    assert sy <= ey
                    for y in range(sy, ey + 1):
                        brick.append((sx, y, sz))
                elif sy == ey and sz == ez:
                    assert sx <= ex
                    for x in range(sx, ex + 1):
                        brick.append((x, sy, sz))
                else:
                    assert False
                assert len(brick) >= 1
                bricks.append(brick)
            print("File parsed successfully.")
            return bricks
    except FileNotFoundError as fnfe:
        print(f"File not found error: {fnfe}")
    except Exception as e:
        print(f"File error: {e}")

def simulate_settling(bricks):
    """Simulates the bricks falling into place."""
    print("Simulating settling of bricks...")
    seen = set()
    for brick in bricks:
        for (x, y, z) in brick:
            seen.add((x, y, z))

    while True:
        any_change = False
        for i, brick in enumerate(bricks):
            ok_to_fall = True
            for (x, y, z) in brick:
                if z == 1 or ((x, y, z - 1) in seen and (x, y, z - 1) not in brick):
                    ok_to_fall = False
                    break
            if ok_to_fall:
                any_change = True
                for (x, y, z) in brick:
                    seen.discard((x, y, z))
                    seen.add((x, y, z - 1))
                bricks[i] = [(x, y, z - 1) for (x, y, z) in brick]
        if not any_change:
            break
    print("Settling simulation completed.")
    return bricks, seen

def find_safe_disintegrations(bricks, seen):
    """Determines which bricks can be safely disintegrated."""
    print("Identifying safe disintegrations...")
    original_seen = seen.copy()
    original_bricks = bricks.copy()
    safe_count = 0

    for i, brick in enumerate(original_bricks):
        temp_seen = original_seen.copy()
        temp_bricks = original_bricks.copy()

        for (x, y, z) in brick:
            temp_seen.discard((x, y, z))

        while True:
            any_change = False
            for j, temp_brick in enumerate(temp_bricks):
                if j == i:
                    continue
                ok_to_fall = True
                for (x, y, z) in temp_brick:
                    if z == 1 or ((x, y, z - 1) in temp_seen and (x, y, z - 1) not in temp_brick):
                        ok_to_fall = False
                        break
                if ok_to_fall:
                    for (x, y, z) in temp_brick:
                        temp_seen.discard((x, y, z))
                        temp_seen.add((x, y, z - 1))
                    temp_bricks[j] = [(x, y, z - 1) for (x, y, z) in temp_brick]
                    any_change = True
            if not any_change:
                break

        # If no bricks fell, increment safe count
        if all(j != i for j in temp_bricks):
            safe_count += 1

    print(f"Found {safe_count} bricks that can be safely disintegrated.")
    return safe_count

def process_puzzle(bricks):
    """Processes the puzzle solution algorithm."""
    settled_bricks, seen = simulate_settling(bricks)
    return find_safe_disintegrations(settled_bricks, seen)

def run_test():
    """Runs the algorithm with the test data and asserts the result."""
    print("Running test...")
    test_bricks = parse_input("../test.txt")
    expected_result = 16  # Assuming expected result is 16
    test_result = process_puzzle(test_bricks)
    assert test_result == expected_result, f"Test failed: Expected {expected_result}, got {test_result}"
    print("Test passed successfully.")

def main():
    """Main function to run the algorithm with the actual puzzle data."""
    try:
        run_test()
        print("Start processing input puzzle...")
        puzzle_bricks = parse_input("../input.txt")
        result = process_puzzle(puzzle_bricks)
        print(f"Final Result: {result}")
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
