import os
from collections import Counter

def read_hands(file_path):
    """
    Reads hands and their bids from the file.
    Returns a list of tuples (hand, bid).
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip().split() for line in file]
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise

def replace_face_cards(hand):
    """
    Replaces face cards with characters that maintain the card order.
    """
    replacements = {'T': 'a', 'J': 'b', 'Q': 'c', 'K': 'd', 'A': 'e'}
    return ''.join(replacements.get(card, card) for card in hand)

def categorize_hand(hand):
    """
    Categorizes the hand into its type and returns a tuple of (category, hand).
    """
    hand = replace_face_cards(hand)
    card_count = Counter(hand)

    if 5 in card_count.values():
        category = 7
    elif 4 in card_count.values():
        category = 6
    elif 3 in card_count.values() and 2 in card_count.values():
        category = 5
    elif 3 in card_count.values():
        category = 4
    elif list(card_count.values()).count(2) == 2:
        category = 3
    elif 2 in card_count.values():
        category = 2
    else:
        category = 1

    return (category, hand)

def hand_key(hand):
    """
    Key function for sorting hands.
    Converts the hand into a format that can be compared directly.
    """
    return categorize_hand(hand[0])

def calculate_total_winnings(file_path):
    """
    Calculates the total winnings from the hands in the file.
    """
    hands = read_hands(file_path)
    sorted_hands = sorted(hands, key=hand_key, reverse=True)
    total_winnings = sum(int(bid) * (len(hands) - index) for index, (_, bid) in enumerate(sorted_hands))
    return total_winnings

def test():
    print(f"Running test...")
    try:
        expected_result = 6440
        total_winnings = calculate_total_winnings("../test.txt")
        assert total_winnings == expected_result, f"Test failed, expected {expected_result} but got {total_winnings}"
        print(f"Test passed: {total_winnings}")
    except Exception as e:
        print(f"Test failed: {e}")

def main():
    try:
        test()

        result = calculate_total_winnings("../input.txt")
        print(f"Total result from input.txt: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
