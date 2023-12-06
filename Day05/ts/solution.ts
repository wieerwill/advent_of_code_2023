import * as fs from 'fs';

function parseInput(filePath: string): { seedsNumbers: number[][], categories: number[][][] } {
    console.log(`Parsing input from ${filePath}`);
    const data: string[] = fs.readFileSync(filePath, 'utf8').trim().split('\n\n');
    
    const firstLine = data.shift();
    if (!firstLine) {
        throw new Error('Input file is not in the expected format');
    }

    const seedsLine: string = firstLine.split(':')[1].trim();
    const seedsRanges: number[] = seedsLine.split(/\s+/).map(Number);
    const seedsNumbers: number[][] = [];

    for (let i = 0; i < seedsRanges.length; i += 2) {
        seedsNumbers.push([seedsRanges[i], seedsRanges[i] + seedsRanges[i + 1]]);
    }

    const categories: number[][][] = data.map(category => {
        return category.split('\n').slice(1).map(line => line.split(/\s+/).map(Number));
    });

    console.log(`Parsed ${seedsNumbers.length} seed ranges and ${categories.length} categories`);
    return { seedsNumbers, categories };
}

function processCategories(seedsNumbers: number[][], categories: number[][][]): number[][] {
    console.log('Processing categories');
    categories.forEach((category, index) => {
        console.log(`Processing category ${index + 1}`);
        let sources: number[][] = [];
        while (seedsNumbers.length) {
            const seedPair = seedsNumbers.pop();
            if (!seedPair) {
                throw new Error('Unexpected empty seed range');
            }
            const [start, end] = seedPair;
            let found = false;

            for (const [destination, source, length] of category) {
                const overlapStart: number = Math.max(start, source);
                const overlapEnd: number = Math.min(end, source + length);
                if (overlapStart < overlapEnd) {
                    found = true;
                    sources.push([overlapStart - source + destination, overlapEnd - source + destination]);
                    if (overlapStart > start) {
                        seedsNumbers.push([start, overlapStart]);
                    }
                    if (end > overlapEnd) {
                        seedsNumbers.push([overlapEnd, end]);
                    }
                    break;
                }
            }

            if (!found) {
                sources.push([start, end]);
            }
        }
        seedsNumbers.push(...sources);
    });

    console.log('Completed processing categories');
    return seedsNumbers;
}

function findLowestLocation(filePath: string): number {
    try {
        console.log(`Finding lowest location for file: ${filePath}`);
        const { seedsNumbers, categories } = parseInput(filePath);
        const processedSeeds = processCategories(seedsNumbers, categories);
        const lowestLocation = Math.min(...processedSeeds.flat());
        console.log(`Lowest location found: ${lowestLocation}`);
        return lowestLocation;
    } catch (error) {
        console.error(`An error occurred processing '${filePath}': ${(error as Error).message}`);
        throw error;
    }
}

function test() {
    console.log('Starting test');
    const expected = 46;
    try {
        const result = findLowestLocation('../test.txt');
        if (result !== expected) {
            throw new Error(`Test failed, expected ${expected} but got ${result}`);
        }
        console.log('Test passed.');
    } catch (error) {
        console.error(`Test error: ${(error as Error).message}`);
        throw error;
    }
}

function main() {
    try {
        test();
        const result = findLowestLocation('../input.txt');
        console.log(`Total result from input.txt: ${result}`);
    } catch (error) {
        console.error(`An error occurred in main: ${(error as Error).message}`);
    }
}

main();
