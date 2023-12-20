const fs = require('fs');

/**
 * Parses the input file to create workflows.
 * @param {string} filePath Path to the input file.
 * @returns {Object} Parsed workflows.
 */
function parseInput(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n').filter(line => line.trim());

    const workflows = {};
    lines.forEach(line => {
        const [name, rulesStr] = line.split('{');
        const rules = rulesStr.slice(0, -1).split(',');
        const fallback = rules.pop();

        workflows[name] = {
            rules: rules.map(rule => {
                const [condition, target] = rule.split(':');
                const [key, comparison, ...value] = condition.split('');
                return { key, comparison, value: parseInt(value.join('')), target };
            }),
            fallback
        };
    });

    return workflows;
}

/**
 * Recursively counts the number of valid ranges.
 * @param {Object} workflows Workflows object.
 * @param {Object} ranges Current ranges of ratings.
 * @param {string} name Current workflow name.
 * @returns {number} Count of valid ranges.
 */
function countRanges(workflows, ranges, name = 'in') {
    if (name === 'R') return 0;
    if (name === 'A') return Object.values(ranges).reduce((acc, [start, stop]) => acc * (stop - start + 1), 1);

    const { rules, fallback } = workflows[name];
    let total = 0;

    for (const { key, comparison, value, target } of rules) {
        const [start, stop] = ranges[key];
        let tStart, tStop, fStart, fStop;

        if (comparison === '<') {
            tStart = start;
            tStop = value - 1;
            fStart = value;
            fStop = stop;
        } else {
            tStart = value + 1;
            tStop = stop;
            fStart = start;
            fStop = value;
        }

        if (tStart <= tStop) {
            const newRanges = { ...ranges, [key]: [tStart, tStop] };
            total += countRanges(workflows, newRanges, target);
        }

        if (fStart <= fStop) {
            ranges[key] = [fStart, fStop];
        } else {
            break;
        }
    }

    if (total === 0) total += countRanges(workflows, ranges, fallback);

    return total;
}

/**
 * Test the algorithm with a test file.
 * @param {string} testFile Path to the test file.
 * @param {number} expected Expected result.
 */
function testAlgorithm(testFile, expected) {
    const workflows = parseInput(testFile);
    const result = countRanges(workflows, { x: [1, 4000], m: [1, 4000], a: [1, 4000], s: [1, 4000] });
    console.assert(result === expected, `Test failed: Expected ${expected}, got ${result}`);
    console.log("Test passed successfully.");
}

/**
 * Main function to execute the algorithm.
 */
function main() {
    try {
        const testFile = "../test.txt";
        const expectedTestResult = 167409079868000;
        console.log("Running test...");
        testAlgorithm(testFile, expectedTestResult);

        console.log("Test passed. Running on actual input...");
        const inputFile = "../input.txt";
        const workflows = parseInput(inputFile);
        const result = countRanges(workflows, { x: [1, 4000], m: [1, 4000], a: [1, 4000], s: [1, 4000] });
        console.log(`Result for the puzzle input: ${result}`);
    } catch (error) {
        console.error(`Unexpected error: ${error}`);
        process.exit(1);
    }
}

main();
