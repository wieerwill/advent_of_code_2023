import { readFileSync } from 'fs';
import { resolve } from 'path';

function parseSchematic(filePath: string): string[] {
    try {
        const data = readFileSync(filePath, 'utf8');
        return data.split('\n').map(line => line.trim());
    } catch (err) {
        throw new Error(`Error reading file: ${filePath}, ${(err as Error).message}`);
    }
}

function getAdjacentPositions(rows: number, cols: number, row: number, col: number): [number, number][] {
    const positions: [number, number][] = [];
    for (let i = Math.max(0, row - 1); i <= Math.min(rows - 1, row + 1); i++) {
        for (let j = Math.max(0, col - 1); j <= Math.min(cols - 1, col + 1); j++) {
            if (i !== row || j !== col) {
                positions.push([i, j]);
            }
        }
    }
    return positions;
}

function findStartOfNumber(schematic: string[], row: number, col: number): number {
    while (col > 0 && /\d/.test(schematic[row][col - 1])) {
        col--;
    }
    return col;
}

function extractFullNumber(schematic: string[], startRow: number, startCol: number): number {
    let col = findStartOfNumber(schematic, startRow, startCol);
    let number = '';
    
    while (col < schematic[startRow].length && /\d/.test(schematic[startRow][col])) {
        number += schematic[startRow][col];
        schematic[startRow] = schematic[startRow].substring(0, col) + '.' + schematic[startRow].substring(col + 1);
        col++;
    }

    return parseInt(number, 10);
}

function findGearsAndCalculateRatios(schematic: string[]): number {
    const rows = schematic.length;
    const cols = schematic[0].length;
    let totalRatioSum = 0;

    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            if (schematic[row][col] === '*') {
                const partNumbers: number[] = [];
                for (const [i, j] of getAdjacentPositions(rows, cols, row, col)) {
                    if (/\d/.test(schematic[i][j])) {
                        const partNumber = extractFullNumber(schematic, i, j);
                        if (!partNumbers.includes(partNumber)) {
                            partNumbers.push(partNumber);
                        }
                    }
                }

                if (partNumbers.length === 2) {
                    const gearRatio = partNumbers[0] * partNumbers[1];
                    totalRatioSum += gearRatio;
                    console.log(`Found gear at line ${row + 1} with ratio ${gearRatio}`);
                }
            }
        }
    }

    return totalRatioSum;
}

function runTest() {
    const testFilePath = resolve(__dirname, '../test.txt');
    const testSchematic = parseSchematic(testFilePath);
    const testResult = findGearsAndCalculateRatios(testSchematic);
    console.log(`Test Result: ${testResult}`);
    console.assert(testResult === 467835, `Test failed: Expected 467835, got ${testResult}`);
}

function main() {
    try {
        runTest();
        console.log("Test passed successfully.");

        const inputFilePath = resolve(__dirname, '../input.txt');
        const inputSchematic = parseSchematic(inputFilePath);
        const totalRatioSum = findGearsAndCalculateRatios(inputSchematic);
        console.log(`Total sum of gear ratios: ${totalRatioSum}`);
    } catch (error) {
        console.error((error as Error).message);
    }
}

main();
