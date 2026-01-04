import multiprocessing


def compute_distances(inputs) -> dict:
    distances = {}
    for i in range(len(inputs)):
        for j in range(i + 1, len(inputs)):
            distances[f"{i}-{j}"] = (
                (abs(inputs[i][0] - inputs[j][0]) + 1) *
                (abs(inputs[i][1] - inputs[j][1]) + 1)
            )
    return distances


def part1(inputs) -> int:
    distances = compute_distances(inputs)
    sorted_tile_pairs_depending_distance = sorted(distances.items(), key=lambda item: item[1])
    most_distant_tiles = [int(value) for value in sorted_tile_pairs_depending_distance[-1][0].split('-')]

    return (
        (abs(inputs[most_distant_tiles[0]][0] - inputs[most_distant_tiles[1]][0]) + 1) *
        (abs(inputs[most_distant_tiles[0]][1] - inputs[most_distant_tiles[1]][1]) + 1)
    )


def compute_perimeter(inputs, only_ranges=False) -> list[list[int]] | list[tuple[int, range] | tuple[range, int]]:
    perimeter = []

    if only_ranges:
        for i in range(len(inputs)):
            next_corner_index = i+1 if i+1 < len(inputs) else 0

            if inputs[i][0] == inputs[next_corner_index][0]:  # vertical perimeter edge
                perimeter.append((
                    inputs[i][0],
                    (
                        range(inputs[i][1], inputs[next_corner_index][1]+1, 1)
                        if inputs[i][1] < inputs[next_corner_index][1] else
                        range(inputs[next_corner_index][1], inputs[i][1]+1, 1)
                    )
                ))

            if inputs[i][1] == inputs[next_corner_index][1]:  # horizontal perimeter edge
                perimeter.append((
                    (
                        range(inputs[i][0], inputs[next_corner_index][0]+1, 1)
                        if inputs[i][0] < inputs[next_corner_index][0]
                        else range(inputs[next_corner_index][0], inputs[i][0]+1, 1)
                    ),
                    inputs[i][1]
                ))
        return perimeter

    for i in range(len(inputs)):
        next_corner_index = i+1 if i+1 < len(inputs) else 0

        if inputs[i][0] == inputs[next_corner_index][0]:  # vertical perimeter edge
            perimeter.extend([
                [inputs[i][0], y] for y in range(
                    inputs[i][1], inputs[next_corner_index][1],
                    (1 if inputs[i][1] < inputs[next_corner_index][1] else -1)
                )
            ])
        if inputs[i][1] == inputs[next_corner_index][1]:  # horizontal perimeter edge
            perimeter.extend([
                [x, inputs[i][1]] for x in range(
                    inputs[i][0], inputs[next_corner_index][0],
                    (1 if inputs[i][0] < inputs[next_corner_index][0] else -1)
                )
            ])

    return perimeter


def check_is_tile_inside_perimeter_along_x_axis(tile, perimeter) -> bool:
    # Checking along x axis
    single_points_along_x_axis = [
        [points[0], tile[1]]
        for points in perimeter
        if isinstance(points[1], range) and tile[1] in points[1]
    ]
    edges_along_x_axis = list(filter(lambda points: isinstance(points[1], int) and tile[1] == points[1], perimeter))

    single_points_to_remove = []
    for point in single_points_along_x_axis:
        for edge in edges_along_x_axis:
            if point[0] in edge[0]:
                single_points_to_remove.append(point)
                break

    for point in single_points_to_remove:
        single_points_along_x_axis.remove(point)

    if tile in single_points_along_x_axis or any(tile[0] in edge[0] for edge in edges_along_x_axis):
        return True  # no need to check this tile as it's on the perimeter

    if (
        all(point[0] < tile[0] for point in single_points_along_x_axis) and
        all(edge[0].stop-1 < tile[0] for edge in edges_along_x_axis) or
        all(point[0] > tile[0] for point in single_points_along_x_axis) and
        all(edge[0].start > tile[0] for edge in edges_along_x_axis)
    ):
        return False  # tile is outside perimeter along x axis

    left_count, right_count = 0, 0
    for point in single_points_along_x_axis:
        if point[0] < tile[0]:
            left_count += 1
        else:
            right_count += 1

    for edge in edges_along_x_axis:
        far_left_point = [edge[0].start, tile[1]]
        far_right_point = [edge[0].stop-1, tile[1]]

        edge_connected_to_far_left_going_down, edge_connected_to_far_right_going_down = None, None
        for points in perimeter:
            if isinstance(points[1], range) and far_left_point[1] in points[1] and far_left_point[0] == points[0]:
                edge_connected_to_far_left_going_down = points[1].start == far_left_point[1]
            if isinstance(points[1], range) and far_right_point[1] in points[1] and far_right_point[0] == points[0]:
                edge_connected_to_far_right_going_down = points[1].start == far_right_point[1]

        if (
            edge_connected_to_far_right_going_down and not edge_connected_to_far_left_going_down or
            not edge_connected_to_far_right_going_down and edge_connected_to_far_left_going_down
        ):  # it is a crossing edge
            if far_right_point[0] < tile[0]:
                left_count += 1
            else:
                right_count += 1
        else:  # this edge is not crossing the y axis, it returns where it from
            if far_right_point[0] < tile[0]:
                left_count += 2
            else:
                right_count += 2

    if left_count % 2 == 0 or right_count % 2 == 0:
        return False  # tile is outside perimeter along x axis


def check_is_tile_inside_perimeter_along_y_axis(tile, perimeter) -> bool:
    # Checking along y axis
    single_points_along_y_axis = [
        [tile[0], points[1]]
        for points in perimeter
        if isinstance(points[0], range) and tile[0] in points[0]
    ]
    edges_along_y_axis = list(filter(lambda points: isinstance(points[0], int) and tile[0] == points[0], perimeter))

    single_points_to_remove = []
    for point in single_points_along_y_axis:
        for edge in edges_along_y_axis:
            if point[1] in edge[1]:
                single_points_to_remove.append(point)
                break

    for point in single_points_to_remove:
        single_points_along_y_axis.remove(point)

    if tile in single_points_along_y_axis or any(tile[1] in edge[1] for edge in edges_along_y_axis):
        return True  # no need to check this tile as it's on the perimeter

    if (
        all(point[1] < tile[1] for point in single_points_along_y_axis) and
        all(edge[1].stop-1 < tile[1] for edge in edges_along_y_axis) or
        all(point[1] > tile[1] for point in single_points_along_y_axis) and
        all(edge[1].start > tile[1] for edge in edges_along_y_axis)
    ):
        return False  # tile is outside perimeter along y axis

    up_count, bottom_count = 0, 0
    for point in single_points_along_y_axis:
        if point[1] < tile[1]:
            up_count += 1
        else:
            bottom_count += 1

    for edge in edges_along_y_axis:
        top_point = [tile[0], edge[1].start]
        bottom_point = [tile[0], edge[1].stop-1]

        edge_connected_to_up_point_going_right, edge_connected_to_bottom_point_going_right = None, None
        for points in perimeter:
            if isinstance(points[0], range) and top_point[0] in points[0] and top_point[1] == points[1]:
                edge_connected_to_up_point_going_right = points[0].start == top_point[0]
            if isinstance(points[0], range) and bottom_point[0] in points[0] and bottom_point[1] == points[1]:
                edge_connected_to_bottom_point_going_right = points[0].start == bottom_point[0]

        if (
            edge_connected_to_bottom_point_going_right and not edge_connected_to_up_point_going_right or
            not edge_connected_to_bottom_point_going_right and edge_connected_to_up_point_going_right
        ):  # it is a crossing edge
            if bottom_point[1] < tile[1]:
                up_count += 1
            else:
                bottom_count += 1
        else:  # this edge is not crossing the y axis, it returns where it from
            if bottom_point[1] < tile[1]:
                up_count += 2
            else:
                bottom_count += 2

    if up_count % 2 == 0 or bottom_count % 2 == 0:
        return False  # tile is outside perimeter along x axis

    return True


def check_is_valid_rectangle(tiles, perimeter) -> bool:
    other_corner1 = [tiles[0][0], tiles[1][1]]
    other_corner2 = [tiles[1][0], tiles[0][1]]
    rectangle_perimeter = compute_perimeter([tiles[0], other_corner1, tiles[1], other_corner2])

    for i in range(len(rectangle_perimeter)):
        if (
            not check_is_tile_inside_perimeter_along_x_axis(rectangle_perimeter[i], perimeter) and
            not check_is_tile_inside_perimeter_along_y_axis(rectangle_perimeter[i], perimeter)
        ):
            return False
    return True


def part2(inputs) -> int:
    global global_perimeter
    global global_inputs
    global_perimeter = compute_perimeter(inputs, only_ranges=True)
    global_inputs = inputs

    distances = compute_distances(inputs)
    sorted_tile_pairs_depending_distance = sorted(distances.items(), key=lambda item: item[1], reverse=True)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(parallelize, sorted_tile_pairs_depending_distance)


def parallelize(tile_pair):
    tile_indexes = [int(value) for value in tile_pair[0].split('-')]
    tiles = [global_inputs[tile_indexes[0]], global_inputs[tile_indexes[1]]]

    if check_is_valid_rectangle(tiles, global_perimeter):
        result = (abs(tiles[0][0] - tiles[1][0]) + 1) * (abs(tiles[0][1] - tiles[1][1]) + 1)
        message = f"\nFound valid rectangle {tiles} with area {result}\n"
        with open("outputs.txt", mode='a', encoding='utf-8') as file_:
            file_.write(message)
        print(message)

    print(f"{tiles}", end='\r')


FILENAME = 'day9.txt'
# FILENAME = 'day9_s.txt'
# FILENAME = 'day9_s2.txt'
with open(f'inputs/{FILENAME}', mode='r', encoding='utf-8') as file:
    raw_inputs = file.readlines()

parsed_inputs = [[int(value) for value in line.strip().split(',')] for line in raw_inputs]

# print(parsed_inputs)
print(part1(parsed_inputs))
print(part2(parsed_inputs))  # around 48000 : Found valid rectangle [[5359, 67580], [94880, 50218]] with area 1554370486
