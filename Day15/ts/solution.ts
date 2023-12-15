import * as fs from 'fs';
import * as path from 'path';

function hashLabel(label: string): number {
    // Compute hash value for a given label
    return [...label].reduce((value, char) => (value + char.charCodeAt(0)) * 17 % 256, 0);
}

function processSteps(steps: string[]): number {
    const boxes: string[][] = Array.from({ length: 256 }, () => []);
    const focalLengths: Map<string, number> = new Map();

    steps.forEach(step => {
        const match = step.match(/([a-z]+)([=-])(\d)?/);
        if (!match) return;

        const [, label, operation, focalLength] = match;
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
            boxPower + (boxNumber + 1) * (i + 1) * (focalLengths.get(label) || 0), 0), 0);
}

function readFileContent(filePath: string): string {
    try {
        return fs.readFileSync(filePath, 'utf-8');
    } catch (error) {
        console.error(`Error reading file at ${filePath}:`, (error as Error).message);
        process.exit(1);
    }
}

function testAlgorithm(): void {
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

function main(): void {
    try {
        testAlgorithm();

        const inputContent = readFileContent(path.join(__dirname, '../input.txt'));
        const inputSteps = inputContent.replace(/\n/g, '').split(',');
        const finalResult = processSteps(inputSteps);

        console.log(`Final Result: ${finalResult}`);
    } catch (error) {
    console.error(`An error occurred in main: ${(error as Error).message}`);
        process.exit(1);
    }
}

main();
