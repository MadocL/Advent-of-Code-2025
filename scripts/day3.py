def part1(inputs) -> int:
    sum_ = 0

    for bank in inputs:
        first_battery_idx = bank.index(max(bank[:len(bank)-1]))
        second_battery = max(bank[first_battery_idx + 1:])
        sum_ += int(str(bank[first_battery_idx]) + str(second_battery))

    return sum_


def part2(inputs) -> int:
    sum_ = 0

    for bank in inputs:
        batteries_idx = []
        for i in range(12):
            previous_idx = batteries_idx[-1] if batteries_idx else -1
            sub_bank = bank[previous_idx + 1:(len(bank) - 12 + 1 + i)]
            max_battery_sub_bank_idx = sub_bank.index(max(sub_bank))
            batteries_idx.append(max_battery_sub_bank_idx + previous_idx + 1)

        sum_ += int(''.join([str(bank[idx]) for idx in batteries_idx]))

    return sum_


FILENAME = 'day3.txt'
# FILENAME = 'day3_s.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [[int(value) for value in line.strip()] for line in raw_inputs]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
