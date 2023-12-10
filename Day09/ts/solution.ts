import fs from 'fs';

function generateDifferenceTable(history: number[]): number[][] {
    // Generates a difference table for a given history
    let table: number[][] = [history];
    while (!table[table.length - 1].every(value => value === 0)) {
        let nextRow: number[] = [];
        for (let i = 0; i < table[table.length - 1].length - 1; i++) {
            nextRow.push(table[table.length - 1][i + 1] - table[table.length - 1][i]);
        }
        table.push(nextRow);
    }
    return table;
}

function extrapolatePreviousValue(table: number[][]): number {
    // Extrapolates the previous value from the difference table
    try {
        for (let i = table.length - 2; i >= 0; i--) {
            table[i].unshift(table[i][0] - table[i + 1][0]);
        }
        return table[0][0];
    } catch (error) {
        console.error(`Error in extrapolatePreviousValue: ${error}`);
        throw error;
    }
}

function solvePuzzle(filename: string): number {
    // Solves the puzzle by reading histories from the file and summing their extrapolated previous values
    try {
        const data = fs.readFileSync(filename, 'utf8');
        const lines = data.split('\n');
        let total = 0;

        for (const line of lines) {
            if (line.trim() === '') continue;
            const history = line.split(' ').map(Number);
            const diffTable = generateDifferenceTable(history);
            const prevValue = extrapolatePreviousValue(diffTable);
            total += prevValue;
        }

        return total;
    } catch (error) {
        console.error(`Error processing file ${filename}: ${error}`);
        throw error;
    }
}

function test(): void {
    // Runs the test using the test.txt file and asserts the expected outcome
    const expected = 2; // Expected result from the test data for the second part
    try {
        const result = solvePuzzle('../test.txt');
        console.assert(result === expected, `Test failed: Expected ${expected}, got ${result}`);
        console.log('Test passed successfully.');
    } catch (error) {
        console.error(`Test failed: ${error}`);
        process.exit(1);
    }
}

function main(): void {
    // Main function to run the test and then solve the puzzle
    console.log('Running test for the second part...');
    test();
    console.log('Test completed. Solving the puzzle for the second part...');
    try {
        const result = solvePuzzle('../input.txt');
        console.log(`Puzzle result for the second part: ${result}`);
    } catch (error) {
        console.error(`Error solving puzzle: ${error}`);
        process.exit(1);
    }
}

main();
