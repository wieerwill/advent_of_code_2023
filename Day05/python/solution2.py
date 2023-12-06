import os
import gc
from itertools import groupby

def free_up_memory():
    """Explicitly frees up memory."""
    gc.collect()

def parse_input(file_path):
    """Parses the input file into seeds and categories."""
    with open(file_path) as file:
        lines = file.read().splitlines()

    groups = [tuple(group) for not_empty, group in groupby(lines, bool) if not_empty]
    seeds, *categories = groups
    seeds_ranges = tuple(map(int, seeds[0].split()[1:]))
    seeds_numbers = [
        (seeds_ranges[i], seeds_ranges[i] + seeds_ranges[i + 1])
        for i in range(0, len(seeds_ranges), 2)
    ]
    return seeds_numbers, categories

def process_categories(seeds_numbers, categories):
    """Processes the seed ranges through all categories."""
    for category in categories:
        ranges = [tuple(map(int, numbers.split())) for numbers in category[1:]]

        sources = []
        while seeds_numbers:
            start, end = seeds_numbers.pop()
            for destination, source, length in ranges:
                overlap_start = max(start, source)
                overlap_end = min(end, source + length)
                if overlap_start < overlap_end:
                    sources.append(
                        (
                            overlap_start - source + destination,
                            overlap_end - source + destination,
                        )
                    )
                    if overlap_start > start:
                        seeds_numbers.append((start, overlap_start))
                    if end > overlap_end:
                        seeds_numbers.append((overlap_end, end))
                    break
            else:
                sources.append((start, end))

        seeds_numbers = sources
    return seeds_numbers

def find_lowest_location(file_path, is_test=False, expected_result=None):
    """Finds the lowest location number from the input file."""
    try:
        seeds_numbers, categories = parse_input(file_path)
        seeds_numbers = process_categories(seeds_numbers, categories)
        lowest_location = min(seeds_numbers)[0]

        if is_test:
            assert lowest_location == expected_result, f"Test failed, expected {expected_result} but got {lowest_location}"
            print("Test passed.")
        else:
            print(f"Lowest location from {file_path}: {lowest_location}")
        return lowest_location

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred processing '{file_path}': {e}")

def test():
    """Run tests using the test.txt file."""
    print("Starting test")
    expected_result = 46  # Updated expected result for the new puzzle
    find_lowest_location('../test.txt', is_test=True, expected_result=expected_result)

def main():
    """Main function to process the input file and display results."""
    try:
        test()
        free_up_memory()  # Free memory after testing

        print("Starting input.txt")
        find_lowest_location("../input.txt")
        free_up_memory()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
