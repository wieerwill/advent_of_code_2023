import sys
from math import gcd

def parse_file(file_path):
    print(f"Parsing file: {file_path}")
    with open(file_path, 'r') as file:
        D = file.read().strip()
    steps, rule = D.split('\n\n')
    GO = {'L': {}, 'R': {}}
    for line in rule.split('\n'):
        st, lr = line.split('=')
        left, right = lr.split(',')
        GO['L'][st.strip()] = left.strip()[1:].strip()
        GO['R'][st.strip()] = right[:-1].strip()
    return [0 if char == 'L' else 1 for char in steps], GO

def lcm(xs):
    ans = 1
    for x in xs:
        ans = (x * ans) // gcd(x, ans)
    return ans

def navigate_network_simultaneously(steps, GO):
    print("Starting navigation of network.")
    POS = [s for s in GO['L'] if s.endswith('A')]
    T = {}
    t = 0
    while True:
        NP = []
        for i, p in enumerate(POS):
            p = GO['L' if steps[t % len(steps)] == 0 else 'R'][p]
            if p.endswith('Z'):
                T[i] = t + 1
                if len(T) == len(POS):
                    print(f"All paths reached 'Z' nodes at step {t + 1}.")
                    return lcm(T.values())
            NP.append(p)
        POS = NP
        t += 1
        print(f"Step {t}: Current nodes - {POS}")
    assert False

def run_test():
    print("Running test...")
    expected_result = 6
    steps, GO = parse_file("../test2.txt")
    result = navigate_network_simultaneously(steps, GO)
    assert result == expected_result, f"Test failed, expected {expected_result} but got {result}"
    print(f"Test passed with {result} steps.")

def main():
    run_test()
    steps, GO = parse_file("../input.txt")
    result = navigate_network_simultaneously(steps, GO)
    print(f"All paths reached 'Z' nodes simultaneously in {result} steps.")

if __name__ == "__main__":
    main()
