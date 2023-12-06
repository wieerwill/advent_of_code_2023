const fs = require('fs');
const assert = require('assert');

/**
 * Parses the input file to extract the race time and record distance.
 * @param {string} file_path - Path to the input file.
 * @returns {Object} - An object containing time and record distance.
 */
function parseInput(file_path) {
    try {
        const lines = fs.readFileSync(file_path, 'utf-8').trim().split('\n');
        const time = parseInt(lines[0].replace(/\D/g, ''), 10);
        const distance = parseInt(lines[1].replace(/\D/g, ''), 10);
        console.log(`Parsed input from ${file_path} - Time: ${time}, Distance: ${distance}`);
        return { time, distance };
    } catch (error) {
        throw new Error(`Error parsing input file: ${error.message}`);
    }
}

/**
 * Calculates the number of ways to beat the record for the race.
 * @param {number} time - Total time for the race.
 * @param {number} record - Record distance to beat.
 * @returns {number} - Number of ways to win the race.
 */
function calculateWinningWays(time, record) {
    console.log(`Calculating winning ways for Time: ${time}, Record: ${record}`);
    let minHoldTime = 0;
    while (minHoldTime * (time - minHoldTime) <= record && minHoldTime < time) {
        minHoldTime++;
    }
    let maxHoldTime = time - 1;
    while (maxHoldTime * (time - maxHoldTime) <= record && maxHoldTime >= 0) {
        maxHoldTime--;
    }
    const winningWays = Math.max(0, maxHoldTime - minHoldTime + 1);
    console.log(`Winning ways calculated: ${winningWays} (Min: ${minHoldTime}, Max: ${maxHoldTime})`);
    return winningWays;
}

/**
 * Runs a test with the given file and compares the result to the expected result.
 * @param {string} file_path - Path to the test file.
 * @param {number} expected_result - Expected result for the test.
 */
function runTest(file_path, expected_result) {
    console.log(`Running test with file: ${file_path}`);
    const { time, distance } = parseInput(file_path);
    const result = calculateWinningWays(time, distance);
    assert.strictEqual(result, expected_result, `Test failed! Expected ${expected_result}, got ${result}`);
    console.log("Test passed successfully.");
}

function main() {
    try {
        // Run the test
        const testFilePath = "../test.txt";
        const expectedTestResult = 71503; // Expected result from the test file
        runTest(testFilePath, expectedTestResult);

        // Process the actual input
        const inputFilePath = "../input.txt";
        console.log(`\nProcessing input file: ${inputFilePath}`);
        const { time, distance } = parseInput(inputFilePath);
        const result = calculateWinningWays(time, distance);
        console.log(`Final result from input file: ${result}`);

    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
    }
}

main();
