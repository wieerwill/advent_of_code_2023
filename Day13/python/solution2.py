from itertools import groupby

def find_mirror(group):
    """
    Find the line of symmetry in the pattern, considering there may be one smudge.
    Returns the position of the line of symmetry or 0 if none found.
    """
    for i in range(1, len(group)):
        above = group[:i][::-1]
        below = group[i:]
        if sum(sum(a != b for a, b in zip(x, y)) for x, y in zip(above, below)) == 1:
            return i
    return 0

def process_file(filename):
    """
    Process the given file to find the sum of mirror lines considering smudges.
    """
    try:
        with open(filename) as f:
            lines = f.read().splitlines()

        groups = [tuple(group) for not_empty, group in groupby(lines, bool) if not_empty]

        res = 0
        for group in groups:
            # Vertical reflection
            res += find_mirror(group) * 100
            # Horizontal reflection
            res += find_mirror(tuple(zip(*group)))
        
        return res

    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        raise

def test():
    """
    Test function to verify the algorithm with test data.
    """
    try:
        test_result = process_file("../test.txt")
        print(f"Test result: {test_result}")
        expected_result = 400  # Adjust this based on the expected outcome of the test data
        assert test_result == expected_result, f"Test failed. Expected result is {expected_result}."
        print("Test passed.")
    except AssertionError as ae:
        print(ae)
    except Exception as e:
        print(f"Test error: {e}")

def main():
    """
    Main function to process the actual input file.
    """
    print("Starting tests...")
    test()
    
    try:
        final_result = process_file("../input.txt")
        print(f"Final result: {final_result}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
