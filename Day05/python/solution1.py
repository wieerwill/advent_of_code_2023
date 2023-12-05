import os

def map_seed_through_category(seed, line):
    """Maps a single seed through a category based on a mapping line."""
    dest_start, source_start, range_length = map(int, line.split())
    if source_start <= seed < source_start + range_length:
        return dest_start + (seed - source_start)
    return seed

def process_category(file, seeds):
    """Processes seeds through a single category based on the file lines."""
    print(f"Starting category processing")
    updated_seeds = [-1] * len(seeds)  # Initialize with -1 to indicate unmapped seeds

    for line in file:
        line = line.strip()
        print(f"Processing category line: {line}")
        if not line or ':' in line:  # End of the current category map
            break

        dest_start, source_start, range_length = map(int, line.split())
        for i, seed in enumerate(seeds):
            if updated_seeds[i] == -1 and source_start <= seed < source_start + range_length:
                updated_seeds[i] = dest_start + (seed - source_start)

    # For seeds that weren't mapped in this category, keep their original value
    for i, seed in enumerate(updated_seeds):
        if seed == -1:
            updated_seeds[i] = seeds[i]

    print(f"Seeds after category processing: {updated_seeds}")
    return updated_seeds

def process_file(file_path, is_test=False):
    """Processes the file to find the lowest location number for the seeds."""
    try:
        with open(file_path, 'r') as file:
            seeds = list(map(int, file.readline().split(':')[1].split()))
            print(f"Initial Seeds: {seeds}")

            while True:
                line = file.readline()
                if not line:  # End of file
                    break
                if ':' in line:  # Start of a new category map
                    seeds = process_category(file, seeds)

            lowest_location = min(seeds)
            print(f"Lowest location from {file_path}: {lowest_location}")
            return lowest_location

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred processing '{file_path}': {e}")

def test():
    """Run tests using the test.txt file."""
    expected_result = 35  # Based on the given example
    result = process_file('../test.txt')
    assert result == expected_result, f"Test failed, expected 35 but got {result}"
    print(f"Test passed: {result}")

def main():
    """Main function to process the input file and display results."""
    try:
        # Run tests first
        test()

        # Process actual input
        result = process_file("../input.txt")
        print(f"Total result from input.txt: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
