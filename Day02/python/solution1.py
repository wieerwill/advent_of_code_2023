def parse_game_data(line):
    """
    Parses a line of game data to extract the game ID and the counts of each color.

    Args:
    line (str): A line of game data.

    Returns:
    int, dict: Game ID and a dictionary with color counts.
    """
    parts = line.split(": ")
    game_id = int(parts[0].split(" ")[1])
    color_counts = {"red": 0, "green": 0, "blue": 0}

    subsets = parts[1].split("; ")
    for subset in subsets:
        colors = subset.split(", ")
        for color in colors:
            count, color_name = color.split(" ")
            color_name = (
                color_name.strip()
            )  # Remove any trailing whitespace or newline characters
            color_counts[color_name] = max(color_counts[color_name], int(count))

    return game_id, color_counts


def is_game_possible(game_data, red_cubes, green_cubes, blue_cubes):
    """
    Determines if a game is possible given the number of each color of cubes.

    Args:
    game_data (dict): Color counts for a game.
    red_cubes (int): Number of red cubes.
    green_cubes (int): Number of green cubes.
    blue_cubes (int): Number of blue cubes.

    Returns:
    bool: True if the game is possible, False otherwise.
    """
    return (
        game_data["red"] <= red_cubes
        and game_data["green"] <= green_cubes
        and game_data["blue"] <= blue_cubes
    )


def process_games(file_path, red_cubes, green_cubes, blue_cubes):
    """
    Processes the games from a file and finds the sum of IDs of possible games.

    Args:
    file_path (str): Path to the file containing game data.
    red_cubes (int): Number of red cubes.
    green_cubes (int): Number of green cubes.
    blue_cubes (int): Number of blue cubes.

    Returns:
    int: Sum of IDs of possible games.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    sum_of_ids = 0
    for line in lines:
        game_id, game_data = parse_game_data(line)
        if is_game_possible(game_data, red_cubes, green_cubes, blue_cubes):
            sum_of_ids += game_id

    return sum_of_ids


def test():
    print("start testing")
    # Test the function
    result = process_games("../test.txt", 12, 13, 14)
    # Assertion for testing
    assert result == 8, f"Expected sum of IDs to be 8, but got {result}"
    print(f"Test Passed: Sum of IDs for possible games is {result}\n")


# Run the test
test()

# Process the actual input file
result = process_games("../input.txt", 12, 13, 14)
print(f"From input.txt: Sum of IDs for possible games is {result}")
