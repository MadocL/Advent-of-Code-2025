from functools import reduce
from operator import mul
import numpy as np

def part1(inputs) -> int:
    sum_ = 0

    for i in range(len(inputs[0])):
        if inputs[-1][i] == "*":
            sum_ += reduce(mul, [inputs[j][i] for j in range(len(inputs) - 1)])
        if inputs[-1][i] == "+":
            sum_ += sum([inputs[j][i] for j in range(len(inputs) - 1)])
    return sum_


def part2(inputs) -> int:
    inputs = np.array([list(line[:-1]) for line in inputs])
    
    separated_problems = []
    last_index = 0
    for i in range(1, len(inputs[0])):
        if inputs[-1, i] == "*" or inputs[-1, i] == "+":
            separated_problems.append(inputs[:, last_index:i-1])
            last_index = i
    separated_problems.append(inputs[:, last_index:len(inputs[0])])

    sum_ = 0
    for problem in separated_problems:
        numbers = []
        for i in range(len(problem[0])):
            number = problem[:-1, i:i+1].T.tolist()[0]  # slice number, transpose, then convert to list
            numbers.append(int("".join(number).strip()))  # join list to string, strip spaces, convert to int

        if problem[-1, 0] == "*":
            sum_ += reduce(mul, numbers)
        if problem[-1, 0] == "+":
            sum_ += sum(numbers)

    return sum_


FILENAME = 'day6.txt'
# FILENAME = 'day6_s.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [[value for value in line.strip().split(" ") if value != ""] for line in raw_inputs]
for i in range(len(parsed_inputs) - 1):
    parsed_inputs[i] = [int(value) for value in parsed_inputs[i]]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(raw_inputs))
