const fs = require('fs');

function readHands(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf-8');
        console.log(`Reading hands from ${filePath}...`);
        return data.trim().split('\n').map(line => line.split(' '));
    } catch (err) {
        console.error(`Error reading file ${filePath}: ${err}`);
        throw err;
    }
}

function replaceFaceCards(hand) {
    return hand.replace(/T/g, 'a')
               .replace(/J/g, '1')
               .replace(/Q/g, 'c')
               .replace(/K/g, 'd')
               .replace(/A/g, 'e');
}

function calculateStrength(hand) {
    hand = replaceFaceCards(hand);
    const counts = hand.split('').reduce((acc, card) => {
        acc[card] = (acc[card] || 0) + 1;
        return acc;
    }, {});

    if ('1' in counts) {
        let maxCount = Math.max(...Object.values(counts));
        let maxCard = Object.keys(counts).find(card => counts[card] === maxCount && card !== '1');
        
        if (maxCard) {
            counts[maxCard] += counts['1'];
            delete counts['1'];
        }
    }

    const sortedCounts = Object.values(counts).sort((a, b) => b - a);
    
    console.log(`Hand: ${hand}, Counts: ${sortedCounts}`);

    if (sortedCounts.toString() === '5') return 10;
    if (sortedCounts.toString() === '1,4') return 9;
    if (sortedCounts.toString() === '2,3') return 8;
    if (sortedCounts.toString() === '1,1,3') return 7;
    if (sortedCounts.toString() === '1,2,2') return 6;
    if (sortedCounts.toString() === '1,1,1,2') return 5;
    if (sortedCounts.toString() === '1,1,1,1,1') return 4;
    
    throw new Error(`Invalid hand: ${hand}, Counts: ${sortedCounts}`);
}

function handKey(hand) {
    return calculateStrength(hand[0]);
}

function calculateTotalWinnings(filePath) {
    try {
        const hands = readHands(filePath);
        console.log("Sorting hands based on strength...");
        hands.sort((a, b) => handKey(b) - handKey(a));
        
        console.log("Calculating total winnings...");
        return hands.reduce((acc, [hand, bid], index) => {
            const winnings = (index + 1) * parseInt(bid, 10);
            console.log(`Hand: ${hand}, Rank: ${index + 1}, Bid: ${bid}, Winnings: ${winnings}`);
            return acc + winnings;
        }, 0);
    } catch (err) {
        console.error(`Error calculating winnings: ${err}`);
        throw err;
    }
}

function runTest(filePath, expected) {
    console.log(`Running test with ${filePath}...`);
    try {
        const totalWinnings = calculateTotalWinnings(filePath);
        console.assert(totalWinnings === expected, `Test failed, expected ${expected} but got ${totalWinnings}`);
        console.log(`Test passed: ${totalWinnings}`);
    } catch (err) {
        console.error(`Test failed: ${err}`);
    }
}

function main() {
    try {
        runTest("../test.txt", 5905);
        const result = calculateTotalWinnings("../input.txt");
        console.log(`Total result from input.txt: ${result}`);
    } catch (err) {
        console.error(`An error occurred: ${err}`);
    }
}

main();
