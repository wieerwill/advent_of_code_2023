from collections import Counter


def read_hands(file_path):
    try:
        with open(file_path, "r") as file:
            print("Reading hands...")
            return [line.strip().split() for line in file]
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise


def replace_face_cards(hand):
    replacements = {"T": "a", "J": "1", "Q": "c", "K": "d", "A": "e"}
    return "".join(replacements.get(card, card) for card in hand)


def strength(hand):
    hand = replace_face_cards(hand)
    C = Counter(hand)
    target = max(
        C, key=lambda k: (C[k], k != "1")
    )  # Find the target card, excluding joker

    if "1" in C and target != "1":
        C[target] += C["1"]
        del C["1"]

    if sorted(C.values()) == [5]:
        category = 10
    elif sorted(C.values()) == [1, 4]:
        category = 9
    elif sorted(C.values()) == [2, 3]:
        category = 8
    elif sorted(C.values()) == [1, 1, 3]:
        category = 7
    elif sorted(C.values()) == [1, 2, 2]:
        category = 6
    elif sorted(C.values()) == [1, 1, 1, 2]:
        category = 5
    elif sorted(C.values()) == [1, 1, 1, 1, 1]:
        category = 4
    else:
        raise ValueError(f"Invalid hand: {C} {hand}")

    print(f"Hand: {hand}, Category: {category}")
    return (category, hand)


def hand_key(hand):
    return strength(hand[0])


def calculate_total_winnings(file_path):
    hands = read_hands(file_path)
    print("Sorting hands based on strength...")
    sorted_hands = sorted(hands, key=hand_key, reverse=True)
    total_winnings = sum(
        int(bid) * (len(hands) - index) for index, (_, bid) in enumerate(sorted_hands)
    )
    print("Calculating total winnings...")
    return total_winnings


def test(file_path):
    print(f"Running test with {file_path}...")
    try:
        expected_result = 5905
        total_winnings = calculate_total_winnings(file_path)
        assert (
            total_winnings == expected_result
        ), f"Test failed, expected {expected_result} but got {total_winnings}"
        print(f"Test passed: {total_winnings}")
    except Exception as e:
        print(f"Test failed: {e}")


def main():
    try:
        test("../test.txt")
        result = calculate_total_winnings("../input.txt")
        print(f"Total result from input.txt: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
