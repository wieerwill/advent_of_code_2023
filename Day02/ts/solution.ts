import * as fs from 'fs';
import * as path from 'path';

interface ColorCounts {
    red: number;
    green: number;
    blue: number;
}

/**
 * Parses a line from the game data file.
 *
 * @param {string} line - A line from the game data file.
 * @returns {ColorCounts} - An object containing the max counts of each color.
 */
function parseGameData(line: string): ColorCounts {
    const colorCounts: ColorCounts = { red: 0, green: 0, blue: 0 };

    const subsets = line.split(': ')[1].split('; ');
    subsets.forEach(subset => {
        subset.split(', ').forEach(color => {
            const [count, colorName] = color.split(' ');
            colorCounts[colorName as keyof ColorCounts] = Math.max(colorCounts[colorName as keyof ColorCounts], parseInt(count));
        });
    });

    return colorCounts;
}

/**
 * Calculates the power of a cube set.
 *
 * @param {ColorCounts} colorCounts - The counts of each color.
 * @returns {number} - The power of the cube set.
 */
function calculatePower(colorCounts: ColorCounts): number {
    return colorCounts.red * colorCounts.green * colorCounts.blue;
}

/**
 * Processes the game data from a file.
 *
 * @param {string} filePath - The path to the file.
 * @returns {number} - The sum of the powers of the minimum cube sets.
 */
function processGames(filePath: string): number {
    try {
        const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(line => line);
        return lines.reduce((sum, line) => sum + calculatePower(parseGameData(line)), 0);
    } catch (error) {
        throw new Error(`Failed to process file: ${filePath}. Error: ${error}`);
    }
}

// Test the functionality
function runTest(): void {
    const testFilePath = path.join(__dirname, '../test.txt');
    const testResult = processGames(testFilePath);
    console.assert(testResult === 2286, `Test failed: Expected 2286, got ${testResult}`);
    console.log(`Test Passed: Sum of powers for the minimum cube sets is ${testResult}`);
}

// Main execution
function main(): void {
    try {
        runTest();
        const inputFilePath = path.join(__dirname, '../input.txt');
        const result = processGames(inputFilePath);
        console.log(`From input.txt: Sum of powers for the minimum cube sets is ${result}`);
    } catch (error) {
        console.error(error);
    }
}

main();
