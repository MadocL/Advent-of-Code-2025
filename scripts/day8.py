from math import dist


def part1(inputs) -> int:
    distances = {}

    for i in range(len(inputs)):
        for j in range(i+1, len(inputs)):
            distances[f"{i}-{j}"] = dist(inputs[i], inputs[j])

    distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    circuits = []

    for boxes, _ in list(distances.items())[:MAX_CONNECTION]:
        box1, box2 = boxes.split("-")
        box1_already_connected_to, box2_already_connected_to = None, None

        for i in range(len(circuits)):
            if box1 in circuits[i]:
                box1_already_connected_to = i
            if box2 in circuits[i]:
                box2_already_connected_to = i

        if box1_already_connected_to is not None and box2_already_connected_to is not None:
            if box1_already_connected_to == box2_already_connected_to:
                continue  # do nothing, already connected
            else:
                first = max(box1_already_connected_to, box2_already_connected_to)
                second = min(box1_already_connected_to, box2_already_connected_to)
                circuits.append(circuits.pop(first) + circuits.pop(second))
        elif box1_already_connected_to is not None:
            circuits[box1_already_connected_to].append(box2)
        elif box2_already_connected_to is not None:
            circuits[box2_already_connected_to].append(box1)
        else:
            circuits.append([box1, box2])

    circuits = sorted(circuits, key=len, reverse=True)

    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])


def part2(inputs) -> int:
    distances = {}

    for i in range(len(inputs)):
        for j in range(i+1, len(inputs)):
            distances[f"{i}-{j}"] = dist(inputs[i], inputs[j])

    distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    ordered_connections = list(distances.keys())
    connection_idx = 0
    circuits = []
    while sum(len(circuit) for circuit in circuits) < len(inputs):
        box1, box2 = ordered_connections[connection_idx].split("-")
        box1_already_connected_to, box2_already_connected_to = None, None

        for i in range(len(circuits)):
            if box1 in circuits[i]:
                box1_already_connected_to = i
            if box2 in circuits[i]:
                box2_already_connected_to = i

        if box1_already_connected_to is not None and box2_already_connected_to is not None:
            if box1_already_connected_to == box2_already_connected_to:
                connection_idx += 1
                continue  # do nothing, already connected
            else:
                first = max(box1_already_connected_to, box2_already_connected_to)
                second = min(box1_already_connected_to, box2_already_connected_to)
                circuits.append(circuits.pop(first) + circuits.pop(second))
        elif box1_already_connected_to is not None:
            circuits[box1_already_connected_to].append(box2)
        elif box2_already_connected_to is not None:
            circuits[box2_already_connected_to].append(box1)
        else:
            circuits.append([box1, box2])
        connection_idx += 1

    circuits = sorted(circuits, key=len)

    return inputs[int(box1)][0] * inputs[int(box2)][0]


# FILENAME, MAX_CONNECTION = 'day8_s.txt', 10
FILENAME, MAX_CONNECTION = 'day8.txt', 1000
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [[int(value) for value in line.strip().split(",")] for line in raw_inputs]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))
