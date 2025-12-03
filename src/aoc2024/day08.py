from collections import defaultdict
from itertools import count, permutations
from aoc_tools import read_data

data = read_data(day=8).split("\n")
antennas = {}
values = defaultdict(list)
for y, line in enumerate(data):
    for x, value in enumerate(line):
        if value == ".":
            continue
        antennas[(x, y)] = value
        values[value].append((x, y))

antinodes = set()
antinodes2 = set()
for value, antennas in values.items():
    for antenna in antennas:
        antinodes2.add(antenna)

    # itertools.combinations would only check one side;
    # for permutations, only one dx/dy needs to be calculated
    for (x1, y1), (x2, y2) in permutations(antennas, 2):
        # note that dx and dy can be negative
        # when antenna 1 is to the north and/or east of antenna 2
        dx = x2 - x1
        dy = y2 - y1

        # (x3, y3) is the interference point
        x3, y3 = x1 - dx, y1 - dy

        for multiplier in count(1):
            x3, y3 = x1 - dx * multiplier, y1 - dy * multiplier

            # stop when going outside the field
            if x3 not in range(len(data[0])) or y3 not in range(len(data)):
                break

            # part 1 does only one position
            if multiplier == 1:
                antinodes.add((x3, y3))

            antinodes2.add((x3, y3))

part1 = len(antinodes)
print(f"{part1=}")

part2 = len(antinodes2)
print(f"{part2=}")
