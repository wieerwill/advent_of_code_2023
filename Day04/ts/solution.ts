import { readFileSync } from "fs";

function main() {
    try {
        console.log("Running tests...");
        runTest("../test.txt");
        console.log("Tests passed.");

        console.log("Processing main input...");
        const result = processInput("../input.txt");
        console.log(`Puzzle result: ${result}`);
    } catch (error) {
        console.error(`Error: ${error}`);
    }
}

function runTest(filename: string) {
    const input = readFile(filename);
    const cards = parse(input);

    const partAResult = partA(cards);
    const partBResult = partB(cards);

    console.assert(partAResult === 13, `Part A Test failed: Expected 13, got ${partAResult}`);
    console.assert(partBResult === 30, `Part B Test failed: Expected 30, got ${partBResult}`);
}

function processInput(filename: string): number {
    const input = readFile(filename);
    const cards = parse(input);

    return partA(cards) + partB(cards);
}

function partA(cards: Card[]): number {
    return cards
        .filter(card => card.wins > 0)
        .map(card => Math.pow(2, card.wins - 1))
        .reduce((a, b) => a + b, 0);
}

function partB(cards: Card[]): number {
    const queue = Array.from(Array(cards.length).keys());
    let visited = 0;

    while (queue.length > 0) {
        const i = queue.pop()!;
        visited++;

        const card = cards[i];
        if (card.wins === 0) continue;

        for (let j = 0; j < card.wins; j++) {
            queue.push(j + i + 1);
        }
    }

    return visited;
}

function readFile(filename: string): string {
    try {
        return readFileSync(filename, 'utf-8');
    } catch (error) {
        throw new Error(`Failed to read file '${filename}': ${error}`);
    }
}

function parse(input: string): Card[] {
    return input.split('\n').map(line => {
        const [winning, scratch] = line.split(': ')[1].split(' | ').map(parseNumbers);
        const wins = scratch.filter(x => winning.includes(x)).length;
        return new Card(wins);
    });
}

function parseNumbers(input: string): number[] {
    return input.split(' ').map(Number);
}

class Card {
    constructor(public wins: number) {}
}

main();
