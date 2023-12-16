import sys


def read_grid(file_path):
    """Reads the grid from a file."""
    try:
        with open(file_path, "r") as file:
            return [list(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)


def step(r, c, d, DR, DC):
    """Calculates the next position and direction of the beam."""
    return (r + DR[d], c + DC[d], d)


def score(G, sr, sc, sd, DR, DC):
    """Calculates the number of unique tiles energized by the beam."""
    POS = [(sr, sc, sd)]
    SEEN = set()
    SEEN2 = set()
    while POS:
        NP = []
        for r, c, d in POS:
            if 0 <= r < len(G) and 0 <= c < len(G[0]):
                SEEN.add((r, c))
                if (r, c, d) in SEEN2:
                    continue
                SEEN2.add((r, c, d))
                ch = G[r][c]
                if ch == ".":
                    NP.append(step(r, c, d, DR, DC))
                elif ch == "/":
                    NP.append(step(r, c, {0: 1, 1: 0, 2: 3, 3: 2}[d], DR, DC))
                elif ch == "\\":
                    NP.append(step(r, c, {0: 3, 1: 2, 2: 1, 3: 0}[d], DR, DC))
                elif ch == "|":
                    if d in [0, 2]:
                        NP.append(step(r, c, d, DR, DC))
                    else:
                        NP.append(step(r, c, 0, DR, DC))
                        NP.append(step(r, c, 2, DR, DC))
                elif ch == "-":
                    if d in [1, 3]:
                        NP.append(step(r, c, d, DR, DC))
                    else:
                        NP.append(step(r, c, 1, DR, DC))
                        NP.append(step(r, c, 3, DR, DC))
                else:
                    assert False, f"Invalid character '{ch}' in grid."
        POS = NP
    return len(SEEN)


def test():
    """Test function to verify the implementation with test data."""
    G = read_grid("../test.txt")
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    result = score(G, 0, 0, 1, DR, DC)
    expected_result = 46  # Change this to the expected result of your test
    assert (
        result == expected_result
    ), f"Test failed: Expected {expected_result}, got {result}"
    print("Test passed.")


def main():
    """Main function to run the algorithm with actual puzzle input."""
    test()  # Run test first
    G = read_grid("../input.txt")
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    result = score(G, 0, 0, 1, DR, DC)
    print(f"Number of tiles energized: {result}")


if __name__ == "__main__":
    main()
