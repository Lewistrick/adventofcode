from functools import cache
from aoc_tools import read_data

data = tuple(map(int, read_data().split()))
print(data)


@cache
def nstones(start, blinks):
    if blinks == 0:
        return 1

    if start == 0:
        return nstones(1, blinks - 1)
    elif len((s := str(start))) % 2 == 0:
        half = len(s) // 2
        left, right = int(s[:half]), int(s[half:])
        return nstones(left, blinks - 1) + nstones(right, blinks - 1)
    else:
        return nstones(2024 * start, blinks - 1)


part1 = sum(nstones(i, 25) for i in data)
print(part1)

part2 = sum(nstones(i, 75) for i in data)
print(part2)
