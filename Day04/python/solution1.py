def parse_card_data(line):
    """Parse a single line of card data into card number, winning numbers, and own numbers."""
    try:
        card_info, number_parts = line.split(':')
        winning_part, own_part = number_parts.split('|')

        # Extract card number from card_info
        card_number = ''.join(filter(str.isdigit, card_info))

        # Convert number strings to integer lists
        winning_numbers = set(map(int, winning_part.split()))
        own_numbers = list(map(int, own_part.split()))

        print(f"Card {card_number}: Winning Numbers: {winning_numbers}, Own Numbers: {own_numbers}")
        return winning_numbers, own_numbers
    except ValueError as e:
        raise ValueError(f"Error parsing line '{line}': {e}")

def calculate_card_points(winning_numbers, own_numbers):
    """Calculate the points for a single card."""
    points = 0
    for number in own_numbers:
        if number in winning_numbers:
            points = 1 if points == 0 else points * 2
    return points

def process_cards(file_path):
    """Process all cards in the given file and return the total points."""
    total_points = 0
    with open(file_path, 'r') as file:
        for line in file:
            winning_numbers, own_numbers = parse_card_data(line.strip())
            total_points += calculate_card_points(winning_numbers, own_numbers)
    return total_points

def test():
    """Run tests using the test.txt file."""
    expected_result = 13  # Based on the given example
    result = process_cards('../test.txt')
    assert result == expected_result, f"Test failed: Expected {expected_result}, got {result}"
    print(f"Test passed: {result} points")

def main():
    """Main function to process the input file and display results."""
    try:
        # Run tests first
        test()

        # Process actual input
        total_points = process_cards('../input.txt')
        print(f"Total points from input.txt: {total_points}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
