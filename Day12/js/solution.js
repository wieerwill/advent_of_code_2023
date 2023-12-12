const fs = require('fs');
const path = require('path');

function readData(filePath) {
    try {
        return fs.readFileSync(filePath, 'utf8').trim().split('\n');
    } catch (error) {
        console.error(`Error reading file '${filePath}': ${error.message}`);
        process.exit(1);
    }
}

function unfoldRecord(record) {
    let [dots, blocks] = record.split(' ');
    dots = Array(5).fill(dots).join('?');
    blocks = Array(5).fill(blocks).join(',').split(',').map(Number);
    return [dots, blocks];
}

function countArrangements(dots, blocks, i = 0, bi = 0, current = 0, memo = {}) {
    const key = `${i},${bi},${current}`;
    if (key in memo) {
        return memo[key];
    }

    if (i === dots.length) {
        if (bi === blocks.length && current === 0) {
            return 1;
        } else if (bi === blocks.length - 1 && blocks[bi] === current) {
            return 1;
        } else {
            return 0;
        }
    }

    let ans = 0;
    for (let c of ['.', '#']) {
        if (dots[i] === c || dots[i] === '?') {
            if (c === '.') {
                if (current === 0) {
                    ans += countArrangements(dots, blocks, i + 1, bi, 0, memo);
                } else if (current > 0 && bi < blocks.length && blocks[bi] === current) {
                    ans += countArrangements(dots, blocks, i + 1, bi + 1, 0, memo);
                }
            } else if (c === '#') {
                ans += countArrangements(dots, blocks, i + 1, bi, current + 1, memo);
            }
        }
    }

    memo[key] = ans;
    return ans;
}

function solvePuzzle(lines) {
    let total = 0;
    for (let line of lines) {
        console.log(`Processing: ${line}`);
        let [dots, blocks] = unfoldRecord(line);
        total += countArrangements(dots, blocks);
    }
    return total;
}

function testPuzzle() {
    console.log("Running tests...");
    const testLines = readData(path.join(__dirname, '../test.txt'));
    const testResult = solvePuzzle(testLines);
    console.log(`Test result: ${testResult}`);
    if (testResult !== 525152) {
        throw new Error("Test failed!");
    }
    console.log("Test passed.");
}

function main() {
    try {
        testPuzzle();
        const inputLines = readData(path.join(__dirname, '../input.txt'));
        console.log("Processing input data...");
        const result = solvePuzzle(inputLines);
        console.log(`Final result: ${result}`);
    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
    }
}

main();
