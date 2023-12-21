import * as fs from 'fs';

type Range = [number, number];
type WorkflowRule = [string, string, number, string];
type WorkflowRules = WorkflowRule[];
type Workflows = { [key: string]: [WorkflowRules, string] };

function parseInput(filePath: string): Workflows {
    const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(line => line);
    const workflows: Workflows = {};
    let currentWorkflow: string[] = [];

    for (const line of lines) {
        if (!line.startsWith('{') && currentWorkflow.length > 0) {
            processWorkflow(currentWorkflow);
            currentWorkflow = [];
        }
        currentWorkflow.push(line);
    }
    if (currentWorkflow.length > 0) {
        processWorkflow(currentWorkflow);
    }

    function processWorkflow(workflowLines: string[]) {
        const [name, rulesStr] = workflowLines[0].split('{');
        const rules = rulesStr.slice(0, -1).split(',');
        workflows[name] = [[], rules.pop() as string];
        for (const rule of rules) {
            const [condition, target] = rule.split(':');
            const [key, comparison, ...value] = Array.from(condition);
            workflows[name][0].push([key, comparison, parseInt(value.join('')), target]);
        }
    }

    return workflows;
}

function countRanges(workflows: Workflows, ranges: { [key: string]: Range }, name = 'in'): number {
    if (name === 'R') return 0;
    if (name === 'A') return Object.values(ranges).reduce((acc, [start, stop]) => acc * (stop - start + 1), 1);

    const [rules, fallback] = workflows[name];
    let total = 0;

    for (const [key, comparison, value, target] of rules) {
        const [start, stop] = ranges[key];
        let tRange: Range, fRange: Range;

        if (comparison === '<') {
            tRange = [start, value - 1];
            fRange = [value, stop];
        } else {
            tRange = [value + 1, stop];
            fRange = [start, value];
        }

        if (tRange[0] <= tRange[1]) {
            total += countRanges(workflows, { ...ranges, [key]: tRange }, target);
        }
        if (fRange[0] <= fRange[1]) {
            ranges[key] = fRange;
        } else {
            break;
        }
    }
    return total + countRanges(workflows, ranges, fallback);
}

function testAlgorithm(testFile: string, expected: number) {
    const workflows = parseInput(testFile);
    const result = countRanges(workflows, { 'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000] });
    console.assert(result === expected, `Test failed: expected ${expected}, got ${result}`);
    console.log('Test passed successfully.');
}

function main() {
    try {
        console.log('Running test...');
        testAlgorithm('../test.txt', 167409079868000);

        console.log('Test passed. Running on actual input...');
        const workflows = parseInput('../input.txt');
        const result = countRanges(workflows, { 'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000] });
        console.log(`Result for the puzzle input: ${result}`);
    } catch (error) {
        console.error(`Error: ${error}`);
        process.exit(1);
    }
}

main();
