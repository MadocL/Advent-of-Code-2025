def part1(inputs) -> int:
    return 0


def part2(inputs) -> int:
    return 0


FILENAME = 'day.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [line for line in raw_inputs]

print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
