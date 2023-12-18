const fs = require('fs');

function parseInstructions(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const lines = fileContent.trim().split('\n'); // Trim to remove extra newlines
        console.log(`Parsed ${lines.length} instructions from ${filePath}`);
        return lines;
    } catch (error) {
        console.error(`Error reading file ${filePath}: ${error}`);
        throw error;
    }
}

function calculateArea(lines) {
    const DIRECTIONS = [[0, 1], [1, 0], [0, -1], [-1, 0]];
    let points = [[0, 0]];
    let boundary = 0;

    for (const line of lines) {
        if (!line) continue; // Skip empty lines

        const color = line.split(' ').pop();
        const instructions = color.slice(2, -1);
        const directionIndex = parseInt(instructions.slice(-1), 16);
        const [dr, dc] = DIRECTIONS[directionIndex];
        const steps = parseInt(instructions.slice(0, -1), 16);
        boundary += steps;
        const [row, column] = points[points.length - 1];
        points.push([row + dr * steps, column + dc * steps]);
    }

    let area = 0;
    for (let i = 0; i < points.length; i++) {
        const [x1, y1] = points[i];
        const [x2, y2] = points[(i + 1) % points.length];
        area += x1 * y2 - x2 * y1;
    }

    return Math.abs(area) / 2 + Math.floor(boundary / 2) + 1;
}

function runTest(testFile, expectedResult) {
    const lines = parseInstructions(testFile);
    const calculatedArea = calculateArea(lines);
    if (calculatedArea !== expectedResult) {
        throw new Error(`Test failed, expected ${expectedResult}, got ${calculatedArea}`);
    }
    console.log(`Test passed, area: ${calculatedArea}`);
}

function main() {
    const testFile = "../test.txt";
    const inputFile = "../input.txt";
    const expectedTestArea = 952408144115; // Replace with the correct expected area for the test

    try {
        runTest(testFile, expectedTestArea);

        // Process actual puzzle input
        const lines = parseInstructions(inputFile);
        const area = calculateArea(lines);
        console.log(`Puzzle result (area): ${area}`);
    } catch (error) {
        console.error(`Execution halted due to error: ${error}`);
    }
}

main();
