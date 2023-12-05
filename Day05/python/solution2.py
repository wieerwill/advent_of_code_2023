import os
import gc

def free_up_memory():
    """Explicitly frees up memory."""
    gc.collect()

def parse_ranges(line):
    """Parses a line containing seed ranges."""
    numbers = list(map(int, line.split()))
    return [(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]

def map_single_seed_through_category(seed, category_map):
    """Maps a single seed through a category based on the mapping."""
    print(f"map seed {seed} in category map")
    for source_start, (dest_start, range_length) in category_map.items():
        if source_start <= seed < source_start + range_length:
            return dest_start + (seed - source_start)
    return seed

def process_category(file, ranges):
    """Processes seed ranges through a single category based on the file lines."""
    category_map = {}
    for i, line in file:
        line = line.strip()
        if not line or ':' in line:  # End of the current category map
            break
        dest_start, source_start, range_length = map(int, line.split())
        category_map[source_start] = (dest_start, range_length)
        print(f"parsed line {i} in file")

    # Process each seed through the category map
    mapped_seeds = set()
    for start, length in ranges:
        print(f"process range {start} with length {length}")
        for i in range(length):
            seed = start + i
            mapped_seed = map_single_seed_through_category(seed, category_map)
            mapped_seeds.add(mapped_seed)

    return mapped_seeds

def process_file(file_path):
    """Processes the file to find the lowest location number for the seed ranges."""
    try:
        with open(file_path, 'r') as file:
            ranges = parse_ranges(file.readline().split(':')[1])

            while True:
                line = file.readline()
                if not line:  # End of file
                    break
                if ':' in line:  # Start of a new category map
                    ranges = {(seed, 1) for seed in process_category(file, ranges)}

            lowest_location = min(ranges)[0]

            return lowest_location

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred processing '{file_path}': {e}")

def test():
    """Run tests using the test.txt file."""
    print("Starting test")
    expected_result = 46  # Updated expected result for the new puzzle
    result = process_file('../test.txt')
    assert result == expected_result, f"Test failed, expected 46 but got {result}"
    print(f"Test passed: {result}")

def main():
    """Main function to process the input file and display results."""
    try:
        # Run tests first
        test()
        free_up_memory()  # Free memory after testing

        # Process actual input
        print("Starting input.txt")
        result = process_file("../input.txt")
        print(f"Total result from input.txt: {result}")
        free_up_memory()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
