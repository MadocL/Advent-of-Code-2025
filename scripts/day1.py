def part1(inputs) -> int:
    pos = 50
    point_to_zero_count = 0

    for direction, value in inputs:
        pos = pos + value if direction == 'R' else pos - value
        while pos < 0:
            pos = 100 + pos
        while pos >= 100:
            pos = pos - 100
        if pos == 0:
            point_to_zero_count += 1
    return point_to_zero_count


def part2(inputs) -> int:
    pos = 50
    point_to_zero_count = 0

    for direction, value in inputs:
        for _ in range(value):
            pos = pos + 1 if direction == 'R' else pos - 1
            if pos < 0:
                pos = 99
            if pos > 99:
                pos = 0
            if pos == 0:
                point_to_zero_count += 1
    return point_to_zero_count


FILENAME = 'day1.txt'
# FILENAME = 'day1_s.txt'
# FILENAME = 'day1_xs.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [(line[0], int(line[1:])) for line in raw_inputs]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
