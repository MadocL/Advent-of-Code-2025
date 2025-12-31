def part1(inputs) -> int:
    ranges = inputs[0]
    available_ids = inputs[1]
    fresh_ids_count = 0

    for id_ in available_ids:
        for r in ranges:
            if r[0] <= id_ <= r[1]:
                fresh_ids_count += 1
                break

    return fresh_ids_count


def merge_ranges(ranges, with_offset=False):
    merged_ranges = []

    if not with_offset:
        start = 0
        stop = len(ranges) if len(ranges) % 2 == 0 else len(ranges) - 1
    else:
        start = 1
        stop = len(ranges) - 1 if len(ranges) % 2 == 0 else len(ranges)

    for i in range(start, stop, 2):
        if ranges[i][0] <= ranges[i+1][0] <= ranges[i][1] and ranges[i][0] <= ranges[i+1][1] <= ranges[i][1]:
            merged_ranges.append([ranges[i][0], ranges[i][1]])
        elif ranges[i+1][0] <= ranges[i][1] <= ranges[i+1][1]:
            merged_ranges.append([ranges[i][0], ranges[i+1][1]])
        else:
            merged_ranges.append(ranges[i])
            merged_ranges.append(ranges[i+1])

    if not with_offset:
        if len(ranges) % 2 != 0:
            merged_ranges.append(ranges[-1])
    else:
        merged_ranges.append(ranges[0])
        if len(ranges) % 2 == 0:
            merged_ranges.append(ranges[-1])

    return merged_ranges


def part2(inputs) -> int:
    ranges = inputs[0]
    ranges = sorted(ranges, key=lambda x: x[0])

    merged_ranges = []
    previous_ranges = []
    while len(ranges) > 1 and (ranges != previous_ranges or not merged_ranges):
        previous_ranges = ranges
        merged_ranges = sorted(merge_ranges(ranges), key=lambda x: x[0])
        merged_ranges = sorted(merge_ranges(merged_ranges, with_offset=True), key=lambda x: x[0])
        ranges = merged_ranges

    fresh_ids_count = 0
    for r in merged_ranges:
        fresh_ids_count += r[1] - r[0] + 1

    return fresh_ids_count


# FILENAME = 'day5_s.txt'
FILENAME = 'day5.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = (
    [[int(value) for value in line.strip().split('-')] for line in raw_inputs[:raw_inputs.index('\n')]],
    [int(line.strip()) for line in raw_inputs[raw_inputs.index('\n') + 1:]]
)

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
