import * as fs from 'fs';

interface Card {
    cardNumber: number;
    winningNumbers: Set<number>;
    ownNumbers: number[];
}

// Parses a line of card data and returns the card number, winning numbers, and own numbers
function parseCardData(line: string): Card {
    const [cardInfo, numberParts] = line.split(':');
    const [winningPart, ownPart] = numberParts.split('|');
    const cardNumber = parseInt(cardInfo.match(/\d+/)![0], 10);
    const winningNumbers = new Set(winningPart.trim().split(/\s+/).map(Number));
    const ownNumbers = ownPart.trim().split(/\s+/).map(Number);
    return { cardNumber, winningNumbers, ownNumbers };
}

// Calculates the number of matches for a card
function calculateMatches(winningNumbers: Set<number>, ownNumbers: number[]): number {
    return ownNumbers.reduce((count, number) => count + (winningNumbers.has(number) ? 1 : 0), 0);
}

// Processes the cards and returns the total number of cards including copies
function processCards(cards: Card[]): number {
    let totalCards = cards.length;
    const queue: Card[] = cards.slice(); // Clone the original array to avoid modifying it

    while (queue.length > 0) {
        const currentCard = queue.shift()!;
        const matches = calculateMatches(currentCard.winningNumbers, currentCard.ownNumbers);
        for (let i = 1; i <= matches; i++) {
            if (currentCard.cardNumber + i < cards.length) {
                totalCards++;
                queue.push(cards[currentCard.cardNumber + i - 1]);
            }
        }
    }

    return totalCards;
}

// Reads the file and processes the cards
function processFile(filePath: string): number | null {
    try {
        const data = fs.readFileSync(filePath, 'utf-8');
        const lines = data.trim().split('\n');
        const cards = lines.map(parseCardData);
        return processCards(cards);
    } catch (error) {
        if (error instanceof Error) {
            console.error(`Error processing file ${filePath}: ${error.message}`);
            return null;
        } else {
            console.error(`An unknown error occurred`);
        }
    }
}

// Test function
function test() {
    const expectedResult = 30;
    const result = processFile('../test.txt');
    console.assert(result === expectedResult, `Test failed: Expected ${expectedResult}, got ${result}`);
    console.log(`Test passed: ${result} cards`);
}

// Main function
function main() {
    try {
        test();
        const totalCards = processFile('../input.txt');
        console.log(`Total cards from input.txt: ${totalCards}`);
    } catch (error) {
        if (error instanceof Error) {
            console.error(`An error occurred: ${error.message}`);
        } else {
            console.error(`An unknown error occurred`);
        }
    }
}

main();
