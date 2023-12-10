const fs = require('fs');
const path = require('path');

function gcd(a, b) {
    while (b !== 0) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function lcm(a, b) {
    return (a * b) / gcd(a, b);
}

function parseFile(filePath) {
    console.log(`Parsing file: ${filePath}`);
    const data = fs.readFileSync(filePath, 'utf8').trim();
    const [stepsSection, rulesSection] = data.split('\n\n');
    const steps = stepsSection.split('').map(char => char === 'L' ? 0 : 1);
    const rules = rulesSection.split('\n').reduce((acc, line) => {
        const [state, directions] = line.split('=').map(s => s.trim());
        const [left, right] = directions.split(',').map(s => s.trim());
        acc['L'][state] = left.slice(1);
        acc['R'][state] = right.slice(0, -1);
        return acc;
    }, { 'L': {}, 'R': {} });

    return { steps, rules };
}

function navigateNetworkSimultaneously(steps, rules) {
    console.log("Starting navigation of network.");
    const startNodes = Object.keys(rules['L']).filter(node => node.endsWith('A'));
    let currentNodes = startNodes;
    let stepCount = 0;
    const timeToZ = {};

    while (Object.keys(timeToZ).length < startNodes.length) {
        currentNodes.forEach((node, index) => {
            const direction = steps[stepCount % steps.length] === 0 ? 'L' : 'R';
            const nextNode = rules[direction][node];
            currentNodes[index] = nextNode;
            if (nextNode.endsWith('Z') && !(index in timeToZ)) {
                timeToZ[index] = stepCount + 1;
            }
        });
        stepCount++;
        console.log(`Step ${stepCount}: Current nodes - ${currentNodes}`);
    }

    return Object.values(timeToZ).reduce((acc, val) => lcm(acc, val), 1);
}

function runTest() {
    console.log("Running test...");
    const testPath = path.join(__dirname, '../test.txt');
    const { steps, rules } = parseFile(testPath);
    const expected = 6;
    const result = navigateNetworkSimultaneously(steps, rules);

    if (result !== expected) {
        throw new Error(`Test failed: expected ${expected}, got ${result}`);
    }

    console.log(`Test passed with ${result} steps.`);
}

function main() {
    try {
        runTest();
        const inputPath = path.join(__dirname, '../input.txt');
        const { steps, rules } = parseFile(inputPath);
        const result = navigateNetworkSimultaneously(steps, rules);
        console.log(`All paths reached 'Z' nodes simultaneously in ${result} steps.`);
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

main();
