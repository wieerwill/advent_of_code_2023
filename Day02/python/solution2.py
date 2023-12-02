def parse_game_data(line):
    """
    Parses a line of game data to extract the game ID and the counts of each color.

    Args:
    line (str): A line of game data.

    Returns:
    int, dict: Game ID and a dictionary with color counts.
    """
    parts = line.split(': ')
    game_id = int(parts[0].split(' ')[1])
    color_counts = {'red': 0, 'green': 0, 'blue': 0}
    
    subsets = parts[1].split('; ')
    for subset in subsets:
        colors = subset.split(', ')
        for color in colors:
            count, color_name = color.split(' ')
            color_name = color_name.strip()  # Remove any trailing whitespace or newline characters
            color_counts[color_name] = max(color_counts[color_name], int(count))
    
    return game_id, color_counts

def calculate_power_of_set(game_data):
    """
    Calculates the power of the cube set.

    Args:
    game_data (dict): The minimum number of cubes of each color.

    Returns:
    int: The power of the cube set.
    """
    return game_data['red'] * game_data['green'] * game_data['blue']

def process_games(file_path):
    """
    Processes the games from a file and finds the sum of the power of the minimum sets.

    Args:
    file_path (str): Path to the file containing game data.

    Returns:
    int: Sum of the power of the minimum cube sets.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sum_of_powers = 0
    for line in lines:
        _, game_data = parse_game_data(line)
        power = calculate_power_of_set(game_data)
        sum_of_powers += power

    return sum_of_powers

def test():
    print("start testing")
    sum_of_powers = process_games('../test.txt')

    # Assertion for testing
    assert sum_of_powers == 2286, f"Expected sum of powers to be 2286, but got {sum_of_powers}"

    print(f"Test Passed: Sum of powers for the minimum cube sets is {sum_of_powers}\n")

# Run the test
test()

# Process the actual input file
sum_of_powers = process_games('../input.txt')
print(f"From input.txt: Sum of powers for the minimum cube sets is {sum_of_powers}")
