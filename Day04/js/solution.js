const fs = require('fs');
const path = require('path');

function main() {
    try {
        // Run tests
        const testCards = parseInput(path.join(__dirname, '../test.txt'));
        assert(partA(testCards) === 13, 'Part A test failed');
        assert(partB(testCards) === 30, 'Part B test failed');
        console.log('All tests passed.');

        // Process main input
        const mainCards = parseInput(path.join(__dirname, '../input.txt'));
        const result = partA(mainCards) + partB(mainCards);
        console.log(`Puzzle result: ${result}`);
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

function partA(cards) {
    // Calculate the sum of scores for each card in part A
    return cards.reduce((sum, card) => {
        return sum + (card.wins > 0 ? Math.pow(2, card.wins - 1) : 0);
    }, 0);
}

function partB(cards) {
    // Calculate the count for part B logic
    let queue = [...Array(cards.length).keys()];
    let visited = 0;

    while (queue.length) {
        const i = queue.pop();
        visited++;

        const card = cards[i];
        if (card.wins === 0) continue;

        for (let j = 0; j < card.wins; j++) {
            if (j + i + 1 < cards.length) {
                queue.push(j + i + 1);
            }
        }
    }

    return visited;
}

function parseInput(filePath) {
    // Read and parse input file into an array of card objects
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return data.trim().split('\n').map(parseCard);
    } catch (error) {
        throw new Error(`Failed to read file at ${filePath}: ${error.message}`);
    }
}

function parseCard(line) {
    // Parse a single line into a card object
    const [, cardInfo] = line.split(': ');
    const [winning, scratch] = cardInfo.split(' | ').map(s => s.split(' ').map(Number));
    const winningSet = new Set(winning);
    const wins = scratch.reduce((count, num) => count + (winningSet.has(num) ? 1 : 0), 0);

    return { wins };
}

function assert(condition, message) {
    // Simple assertion function
    if (!condition) {
        throw new Error(message);
    }
}

main();
