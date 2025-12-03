from functools import cache
from aoc_tools import read_data


@cache
def nstones(v, b):
    """Get the number of stones after `b` blinks for stone value `v`"""
    if b == 0:
        return 1
    if v == 0:
        return nstones(1, b - 1)
    if (x := len((s := str(v)))) % 2 == 0:
        l, r = int(s[: x // 2]), int(s[x // 2 :])
        return nstones(l, b - 1) + nstones(r, b - 1)
    return nstones(2024 * v, b - 1)


data = tuple(map(int, read_data().split()))
for part, n in enumerate((25, 75), 1):
    print(f"part {part}:", sum(nstones(i, n) for i in data))
