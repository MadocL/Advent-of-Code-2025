def part1(inputs) -> int:
    beam_set = set([inputs[0].index('S')])
    split_count = 0

    for line in inputs[1:]:
        new_beam_set = set()
        for beam in beam_set:
            if line[beam] == "^":
                new_beam_set.add(beam - 1)
                new_beam_set.add(beam + 1)
                split_count += 1
            else:
                new_beam_set.add(beam)
        beam_set = new_beam_set

    return split_count


def part2(inputs) -> int:
    beam_dict = {inputs[0].index('S'): 1}

    for line in inputs[1:]:
        new_beam_dict = {}
        for pos, timeline_count in beam_dict.items():
            if line[pos] == "^":
                if new_beam_dict.get(pos-1):
                    new_beam_dict[pos-1] += timeline_count
                else:
                    new_beam_dict[pos-1] = timeline_count
                if new_beam_dict.get(pos+1):
                    new_beam_dict[pos+1] += timeline_count
                else:
                    new_beam_dict[pos+1] = timeline_count
            else:
                if new_beam_dict.get(pos):
                    new_beam_dict[pos] += timeline_count
                else:
                    new_beam_dict[pos] = timeline_count
        beam_dict = new_beam_dict

    return sum(beam_dict.values())


# FILENAME = 'day7_xs.txt'
# FILENAME = 'day7_s.txt'
FILENAME = 'day7.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [line.strip() for line in raw_inputs]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
