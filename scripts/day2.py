def part1(inputs) -> int:
    sum_ = 0
    for range_ in inputs:
        for id_ in range(range_[0], range_[1] + 1):
            id_str = str(id_)
            id_str_len = len(id_str)
            sum_ += id_ if id_str[0:id_str_len // 2] == id_str[id_str_len // 2:id_str_len] else 0
    return sum_


def part2(inputs) -> int:
    sum_ = 0
    for range_ in inputs:
        for id_ in range(range_[0], range_[1] + 1):
            id_str = str(id_)
            id_str_len = len(id_str)

            if id_str_len > 1 and all(id_str[0] == char for char in id_str):
                sum_ += id_
                print(id_)
            else:
                for i in range(2, (id_str_len // 2) + 1):
                    if id_str_len % i == 0 and all(
                        id_str[0:id_str_len // i] == id_str[((j * id_str_len) // i):((j + 1) * id_str_len) // i]
                        for j in range(1, i)
                    ):
                        sum_ += id_
                        print(id_)
                        break
    return sum_


FILENAME = 'day2.txt'
# FILENAME = 'day2_s.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [[int(value) for value in line.split('-')] for line in raw_inputs[0].split(',')]

print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
