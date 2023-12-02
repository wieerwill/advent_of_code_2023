const fs = require('fs');
const path = require('path');

/**
 * Parses a line from the game data file.
 *
 * @param {string} line - A line from the game data file.
 * @returns {object} - An object containing the game ID and the max counts of each color.
 */
function parseGameData(line) {
    const parts = line.split(': ');
    const gameID = parseInt(parts[0].split(' ')[1]);
    const colorCounts = { red: 0, green: 0, blue: 0 };

    const subsets = parts[1].split('; ');
    subsets.forEach(subset => {
        subset.split(', ').forEach(color => {
            const [count, colorName] = color.split(' ');
            colorCounts[colorName] = Math.max(colorCounts[colorName], parseInt(count));
        });
    });

    return { gameID, colorCounts };
}

/**
 * Calculates the power of a cube set.
 *
 * @param {object} colorCounts - The counts of each color.
 * @returns {number} - The power of the cube set.
 */
function calculatePower(colorCounts) {
    return colorCounts.red * colorCounts.green * colorCounts.blue;
}

/**
 * Processes the game data from a file.
 *
 * @param {string} filePath - The path to the file.
 * @returns {number} - The sum of the powers of the minimum cube sets.
 */
function processGames(filePath) {
    const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(line => line);
    let sumOfPowers = 0;

    lines.forEach(line => {
        const { colorCounts } = parseGameData(line);
        sumOfPowers += calculatePower(colorCounts);
    });

    return sumOfPowers;
}

// Run tests
const testResult = processGames(path.join(__dirname, '../test.txt'));
console.assert(testResult === 2286, `Test failed: Expected 2286, got ${testResult}`);
console.log(`Test Passed: Sum of powers for the minimum cube sets is ${testResult}`);

// Process the actual input file
const result = processGames(path.join(__dirname, '../input.txt'));
console.log(`From input.txt: Sum of powers for the minimum cube sets is ${result}`);
