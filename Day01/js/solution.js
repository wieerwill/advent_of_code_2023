const fs = require('fs');

function extractDigits(line) {
    // Mapping of digit words to their numeric values
    const digitMap = {
        zero: 0, one: 1, two: 2, three: 3, four: 4,
        five: 5, six: 6, seven: 7, eight: 8, nine: 9
    };

    // Add single digit mappings
    for (let i = 0; i <= 9; i++) {
        digitMap[i.toString()] = i;
    }

    let digitsFound = [];
    let i = 0;
    while (i < line.length) {
        let matched = false;
        for (const [word, digit] of Object.entries(digitMap)) {
            if (line.startsWith(word, i)) {
                digitsFound.push(digit);
                i += word.length - 1; // Advance the index
                matched = true;
                break;
            }
        }
        i++; // Move to the next character if no match
    }

    return digitsFound;
}

function extractCalibrationValue(line) {
    const digits = extractDigits(line);
    if (digits.length > 0) {
        return parseInt(`${digits[0]}${digits[digits.length - 1]}`, 10);
    }
    return 0;
}

function calculateTotalCalibrationValue(filePath) {
    const lines = fs.readFileSync(filePath, 'utf-8').split('\n');
    return lines.reduce((sum, line) => sum + extractCalibrationValue(line), 0);
}

// Run the test
function test() {
    console.warn("Starting Tests")
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
    console.log("Finished Tests\n")
}

// Run the test function for verification
test();

// Calculate and print the total calibration value
const totalValue = calculateTotalCalibrationValue('../input.txt');
console.log(`Total Calibration Value from input.txt: ${totalValue}`);

