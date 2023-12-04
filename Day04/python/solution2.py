def parse_card_data(line):
    """Parse a single line of card data into card number, winning numbers, and own numbers."""
    try:
        card_info, number_parts = line.split(':')
        winning_part, own_part = number_parts.split('|')
        card_number = ''.join(filter(str.isdigit, card_info))
        winning_numbers = set(map(int, winning_part.split()))
        own_numbers = list(map(int, own_part.split()))
        return int(card_number), winning_numbers, own_numbers
    except ValueError as e:
        raise ValueError(f"Error parsing line '{line}': {e}")

def calculate_matches(winning_numbers, own_numbers):
    """Calculate the number of matches for a single card."""
    return sum(1 for number in own_numbers if number in winning_numbers)

def process_cards(file_path):
    """Process all cards in the given file and return the total number of cards."""
    with open(file_path, 'r') as file:
        cards = [parse_card_data(line.strip()) for line in file]
    
    total_cards = len(cards)  # Start with original cards
    i = 0
    while i < len(cards):
        card_number, winning_numbers, own_numbers = cards[i]
        matches = calculate_matches(winning_numbers, own_numbers)
        for _ in range(matches):
            if card_number + 1 < len(cards):
                cards.append(cards[card_number])
            card_number += 1
        i += 1

    return len(cards)

def test():
    """Run tests using the test.txt file."""
    expected_result = 30  # Based on the given example
    result = process_cards('../test.txt')
    assert result == expected_result, f"Test failed: Expected {expected_result}, got {result}"
    print(f"Test passed: {result} cards")

def main():
    """Main function to process the input file and display results."""
    try:
        # Run tests first
        test()

        # Process actual input
        total_cards = process_cards('../input.txt')
        print(f"Total cards from input.txt: {total_cards}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
