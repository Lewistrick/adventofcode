from collections import defaultdict
from itertools import count, permutations
from aoc_tools import read_data

data = read_data(day=8, suffix="in").split("\n")
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
    for (x1, y1), (x2, y2) in permutations(antennas, 2):
        dx = x2 - x1
        dy = y2 - y1
        x3, y3 = x1 - dx, y1 - dy
        if x3 not in range(len(data[0])) or y3 not in range(len(data)):
            continue

        antinodes.add((x3, y3))
        for multiplier in count(1):
            x3, y3 = x1 - dx * multiplier, y1 - dy * multiplier
            if x3 not in range(len(data[0])) or y3 not in range(len(data)):
                break
            print(f"{x1=} {y1=} {x2=} {y2=} {multiplier=} {x3=} {y3=}")
            antinodes2.add((x3, y3))
for y, line in enumerate(data):
    for x, value in enumerate(line):
        if data[y][x] != ".":
            if (x, y) in antinodes2:
                print("?", end="")
            else:
                print(data[y][x], end="")
        elif (x, y) in antinodes2:
            print("#", end="")
        else:
            print(".", end="")
    print()


part1 = len(antinodes)
print(f"{part1=}")

part2 = len(antinodes2)
print(f"{part2=}")  # 1212 too low, 1334 too low
