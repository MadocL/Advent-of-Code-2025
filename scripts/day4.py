def part1(inputs) -> int:
    relative_adjacent_pos = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
    accessible_paper_rolls_count = 0

    for x in range(len(inputs)):
        for y in range(len(inputs[0])):
            adjacent_paper_rolls_count = len(
                [
                    (x+pos[0], y+pos[1])
                    for pos in relative_adjacent_pos
                    if (
                        0 <= x+pos[0] < len(inputs)
                        and 0 <= y+pos[1] < len(inputs[0])
                        and inputs[x+pos[0]][y+pos[1]] == '@'
                    )
                ]
            )
            if adjacent_paper_rolls_count < 4 and inputs[x][y] == '@':
                accessible_paper_rolls_count += 1

    return accessible_paper_rolls_count


def part2(inputs) -> int:
    relative_adjacent_pos = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
    removed_paper_rolls_count = 0
    accessible_paper_rolls = []
    iteration_count = 0

    while accessible_paper_rolls or iteration_count == 0:
        accessible_paper_rolls = []

        for x in range(len(inputs)):
            for y in range(len(inputs[0])):
                adjacent_paper_rolls_count = len(
                    [
                        (x+pos[0], y+pos[1])
                        for pos in relative_adjacent_pos
                        if (
                            0 <= x+pos[0] < len(inputs)
                            and 0 <= y+pos[1] < len(inputs[0])
                            and inputs[x+pos[0]][y+pos[1]] == '@'
                        )
                    ]
                )
                if adjacent_paper_rolls_count < 4 and inputs[x][y] == '@':
                    accessible_paper_rolls.append((x, y))

        for roll in accessible_paper_rolls:
            inputs[roll[0]][roll[1]] = 'x'

        removed_paper_rolls_count += len(accessible_paper_rolls)
        iteration_count += 1

    return removed_paper_rolls_count


FILENAME = 'day4.txt'
# FILENAME = 'day4_s.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [list(line.strip()) for line in raw_inputs]

print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
