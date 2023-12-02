#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <cassert>

std::vector<int> extractDigits(const std::string& line) {
    std::map<std::string, int> digitMap = {
        {"zero", 0}, {"one", 1}, {"two", 2}, {"three", 3}, {"four", 4},
        {"five", 5}, {"six", 6}, {"seven", 7}, {"eight", 8}, {"nine", 9}
    };
    for (int i = 0; i <= 9; ++i) {
        digitMap[std::to_string(i)] = i;
    }

    std::vector<int> digitsFound;
    size_t i = 0;
    while (i < line.length()) {
        bool matched = false;
        for (const auto& pair : digitMap) {
            if (line.substr(i, pair.first.length()) == pair.first) {
                digitsFound.push_back(pair.second);
                i += pair.first.length() - 1;
                matched = true;
                break;
            }
        }
        i++;
    }

    return digitsFound;
}

int extractCalibrationValue(const std::string& line) {
    std::vector<int> digits = extractDigits(line);
    if (!digits.empty()) {
        return digits.front() * 10 + digits.back();
    }
    return 0;
}

int calculateTotalCalibrationValue(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file: " + filePath);
    }

    std::string line;
    int totalValue = 0;
    while (std::getline(file, line)) {
        totalValue += extractCalibrationValue(line);
    }

    return totalValue;
}

void test() {
    std::cout << "Starting Tests" << std::endl;
    std::vector<std::string> testLines = {
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen"
    };
    std::vector<int> expectedResults = {29, 83, 13, 24, 42, 14, 76};

    for (size_t i = 0; i < testLines.size(); ++i) {
        int result = extractCalibrationValue(testLines[i]);
        assert(result == expectedResults[i]);
        std::cout << "Line: '" << testLines[i] << "', Calibration Value: " << result << std::endl;
    }
    std::cout << "Finished Tests" << std::endl << std::endl;
}

int main() {
    try {
        test();
        int totalValue = calculateTotalCalibrationValue("../input.txt");
        std::cout << "Total Calibration Value from input.txt: " << totalValue << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
