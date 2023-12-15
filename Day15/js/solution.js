const fs = require('fs');
const path = require('path');

function hashLabel(label) {
    // Compute hash value for a given label
    return [...label].reduce((value, char) => (value + char.charCodeAt(0)) * 17 % 256, 0);
}

function processSteps(steps) {
    const boxes = Array.from({ length: 256 }, () => []);
    const focalLengths = new Map();

    steps.forEach(step => {
        const [_, label, operation, focalLength] = step.match(/([a-z]+)([=-])(\d)?/);
        const hashed = hashLabel(label);
        const destination = boxes[hashed];

        console.log(`Processing step: ${label}${operation}${focalLength}, Box: ${hashed}`);

        if (operation === "=") {
            if (!destination.includes(label)) {
                destination.push(label);
            }
            focalLengths.set(label, parseInt(focalLength));
        } else {
            const index = destination.indexOf(label);
            if (index !== -1) {
                destination.splice(index, 1);
            }
            focalLengths.delete(label);
        }
    });

    return boxes.reduce((totalPower, box, boxNumber) =>
        totalPower + box.reduce((boxPower, label, i) =>
            boxPower + (boxNumber + 1) * (i + 1) * focalLengths.get(label), 0), 0);
}

function readFileContent(filePath) {
    try {
        return fs.readFileSync(filePath, 'utf-8');
    } catch (error) {
        console.error(`Error reading file at ${filePath}:`, error.message);
        process.exit(1);
    }
}

function testAlgorithm() {
    const testContent = readFileContent(path.join(__dirname, '../test.txt'));
    const testSteps = testContent.replace(/\n/g, '').split(',');
    const testResult = processSteps(testSteps);

    console.log(`Test Result: ${testResult}`);
    if (testResult !== 145) {
        console.error(`Test failed. Expected result is 145, got ${testResult}.`);
        process.exit(1);
    } else {
        console.log('Test passed.');
    }
}

function main() {
    try {
        testAlgorithm();

        const inputContent = readFileContent(path.join(__dirname, '../input.txt'));
        const inputSteps = inputContent.replace(/\n/g, '').split(',');
        const finalResult = processSteps(inputSteps);

        console.log(`Final Result: ${finalResult}`);
    } catch (error) {
        console.error(`An error occurred in main: ${error.message}`);
        process.exit(1);
    }
}

main();
