from itertools import groupby

def find_mirror(group):
    """
    Find the line of symmetry in the pattern.
    For vertical symmetry, `group` should be the original group of lines.
    For horizontal symmetry, `group` should be the transposed group.
    Returns the position of the line of symmetry or 0 if none found.
    """
    for i in range(1, len(group)):
        above = group[:i][::-1]
        below = group[i:]
        if all(a == b for a, b in zip(above, below)):
            return i
    return 0

def process_file(filename):
    """
    Process the given file to find the sum of mirror lines.
    Handles both vertical and horizontal reflections.
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
        assert test_result == 405, "Test failed. Expected result is 405."
        print("Test passed.")
    except AssertionError as ae:
        print(ae)
    except Exception as e:
        print(f"Test error: {e}")

def main():
    """
    Main function to run the test and then process the actual input file.
    """
    print("Starting tests...")
    test()

    print("\nProcessing main input file...")
    final_result = process_file("../input.txt")
    print(f"Final result: {final_result}")

if __name__ == "__main__":
    main()
