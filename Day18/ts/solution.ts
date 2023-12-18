import * as fs from 'fs';

function parseInstructions(filePath: string): string[] {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const lines = fileContent.trim().split('\n');
        console.log(`Parsed ${lines.length} instructions from ${filePath}`);
        return lines;
    } catch (error) {
        console.error(`Error reading file ${filePath}: ${error}`);
        throw error;
    }
}

function calculateArea(lines: string[]): number {
    const DIRECTIONS: [number, number][] = [[0, 1], [1, 0], [0, -1], [-1, 0]];
    let points: [number, number][] = [[0, 0]];
    let boundary: number = 0;

    for (const line of lines) {
        if (!line) continue;

        const color: string = line.split(' ').pop() as string;
        const instructions: string = color.slice(2, -1);
        const directionIndex: number = parseInt(instructions.slice(-1), 16);
        const [dr, dc] = DIRECTIONS[directionIndex];
        const steps: number = parseInt(instructions.slice(0, -1), 16);
        boundary += steps;
        const [row, column] = points[points.length - 1];
        points.push([row + dr * steps, column + dc * steps]);
    }

    let area: number = 0;
    for (let i = 0; i < points.length; i++) {
        const [x1, y1] = points[i];
        const [x2, y2] = points[(i + 1) % points.length];
        area += x1 * y2 - x2 * y1;
    }

    return Math.abs(area) / 2 + Math.floor(boundary / 2) + 1;
}

function runTest(testFile: string, expectedResult: number): void {
    const lines: string[] = parseInstructions(testFile);
    const calculatedArea: number = calculateArea(lines);
    if (calculatedArea !== expectedResult) {
        throw new Error(`Test failed, expected ${expectedResult}, got ${calculatedArea}`);
    }
    console.log(`Test passed, area: ${calculatedArea}`);
}

function main(): void {
    const testFile: string = "../test.txt";
    const inputFile: string = "../input.txt";
    const expectedTestArea: number = 952408144115; // Replace with the correct expected area for the test

    try {
        runTest(testFile, expectedTestArea);

        // Process actual puzzle input
        const lines: string[] = parseInstructions(inputFile);
        const area: number = calculateArea(lines);
        console.log(`Puzzle result (area): ${area}`);
    } catch (error) {
        console.error(`Execution halted due to error: ${error}`);
    }
}

main();
