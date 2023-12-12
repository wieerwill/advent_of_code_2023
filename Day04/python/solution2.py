def main():
    try:
        # Run tests
        test_cards = parse_input("../test.txt")
        assert part_a(test_cards) == 13, "Part A test failed"
        assert part_b(test_cards) == 30, "Part B test failed"
        print("All tests passed.")

        # Process main input
        main_cards = parse_input("../input.txt")
        result = part_a(main_cards) + part_b(main_cards)
        print(f"Puzzle result: {result}")

    except Exception as e:
        print(f"Error: {e}")


def part_a(cards):
    """Calculate the sum of scores for each card in part A"""
    return sum(2 ** (card["wins"] - 1) for card in cards if card["wins"] > 0)


def part_b(cards):
    """Calculate the count for part B logic"""
    queue = list(range(len(cards)))
    visited = 0

    while queue:
        i = queue.pop()
        visited += 1

        card = cards[i]
        if card["wins"] == 0:
            continue

        for j in range(card["wins"]):
            queue.append(j + i + 1)

    return visited


def parse_input(filename):
    """Read and parse input file into a list of card dictionaries"""
    try:
        with open(filename, "r") as file:
            return [parse_card(line.strip()) for line in file]
    except FileNotFoundError:
        raise Exception(f"File not found: {filename}")
    except Exception as e:
        raise Exception(f"Error reading file {filename}: {e}")


def parse_card(line):
    """Parse a single line into a card dictionary"""
    _, card_info = line.split(": ")
    winning, scratch = card_info.split(" | ")
    winning = set(map(int, winning.split()))
    scratch = list(map(int, scratch.split()))

    wins = sum(1 for num in scratch if num in winning)
    return {"wins": wins}


if __name__ == "__main__":
    main()
