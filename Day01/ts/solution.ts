import * as fs from 'fs';
import * as path from 'path';

function extractDigits(line: string): number[] {
    const digitMap: { [key: string]: number } = {
        zero: 0, one: 1, two: 2, three: 3, four: 4,
        five: 5, six: 6, seven: 7, eight: 8, nine: 9
    };

    for (let i = 0; i <= 9; i++) {
        digitMap[i.toString()] = i;
    }

    const digitsFound: number[] = [];
    let i = 0;
    while (i < line.length) {
        for (const [word, digit] of Object.entries(digitMap)) {
            if (line.startsWith(word, i)) {
                digitsFound.push(digit);
                i += word.length - 1;
                break;
            }
        }
        i++;
    }

    return digitsFound;
}

function extractCalibrationValue(line: string): number {
    const digits = extractDigits(line);
    return digits.length > 0 ? parseInt(`${digits[0]}${digits[digits.length - 1]}`, 10) : 0;
}

function calculateTotalCalibrationValue(filePath: string): number {
    try {
        const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(line => line);
        return lines.reduce((sum, line) => sum + extractCalibrationValue(line), 0);
    } catch (error) {
        throw new Error(`Failed to process file: ${filePath}. Error: ${error}`);
    }
}

function test(): void {
    console.warn("Starting Tests");
    const testLines = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen"
    ];
    const expectedResults = [29, 83, 13, 24, 42, 14, 76];

    testLines.forEach((line, index) => {
        const result = extractCalibrationValue(line);
        console.assert(result === expectedResults[index], `Error in line '${line}': Expected ${expectedResults[index]}, got ${result}`);
        console.log(`Line: '${line}', Calibration Value: ${result}`);
    });
    console.log("Finished Tests\n");
}

function main(): void {
    try {
        test();
        const totalValue = calculateTotalCalibrationValue(path.join(__dirname, '../input.txt'));
        console.log(`Total Calibration Value from input.txt: ${totalValue}`);
    } catch (error) {
        console.error(error);
    }
}

main();
