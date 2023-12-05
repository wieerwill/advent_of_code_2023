import os
import gc

def free_up_memory():
    """Explicitly frees up memory."""
    gc.collect()

def get_mapped_seed(seed, category_mapping):
    """Finds the mapped seed for a given seed in a category."""
    for line in category_mapping:
        dest_start, source_start, range_length = map(int, line.split())
        if source_start <= seed < source_start + range_length:
            return dest_start + (seed - source_start)
    return seed
    
def process_seed_ranges(seed_ranges, category_mappings):
    """Processes seed ranges through categories to find the minimum location."""
    # Processing each seed range through categories
    min_location = float('inf')
    for start, end in seed_ranges:
        print(f"Processing seed range {start} to {end}")

        # If min_location is still inf, then iterate through the range (fallback)
        if min_location == float('inf'):
            for seed in range(start, end):
                location = seed
                for category_mapping in category_mappings:
                    location = get_mapped_seed(location, category_mapping)
                min_location = min(min_location, location)
    return min_location

def process_file(file_path, is_test=False):
    """Processes the file to find the lowest location number for the seed ranges."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Parsing the seed ranges
            seed_line = lines[0].strip()
            parts = seed_line.split(':')[1].split()
            seed_ranges = [(int(parts[i]), int(parts[i]) + int(parts[i + 1])) 
                           for i in range(0, len(parts), 2)]
            # print(f"Seed Ranges: {seed_ranges}")

            # Preparing category mappings
            category_mappings = [[] for _ in range(7)]  # 7 categories
            current_category = -1
            for line in lines[1:]:
                # print(f"processing line {line}")
                if ':' in line:
                    current_category += 1
                elif line.strip():
                    category_mappings[current_category].append(line.strip())

            # Processing each seed range through categories
            min_location = process_seed_ranges(seed_ranges, category_mappings)

            print(f"Lowest location from {file_path}: {min_location}")
            return min_location

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred processing '{file_path}': {e}")

def test():
    """Run tests using the test.txt file."""
    print("Starting test")
    expected_result = 46  # Updated expected result for the new puzzle
    result = process_file('../test.txt', is_test=True)
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
