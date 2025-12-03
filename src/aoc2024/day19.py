from functools import cache
from aoc_tools import read_data

a, p = read_data(suffix="in").split("\n\n")

available = set(a.split(", "))


def is_possible(pattern: str, left: set[str]) -> bool:
    if not pattern:
        return True

    for towel in left:
        if not pattern.startswith(towel):
            continue
        rest_pattern = pattern[len(towel) :]
        new_left = left - {towel}
        if is_possible(rest_pattern, new_left):
            return True

    return False


@cache
def n_arrangements(pattern: str) -> int:
    n = 0

    if not pattern:
        n += 1

    for towel in available:
        if not pattern.startswith(towel):
            continue
        rest_pattern = pattern[len(towel) :]
        n += n_arrangements(rest_pattern)

    return n


part1 = 0
part2 = 0
for pattern in p.split():
    poss = is_possible(pattern, available)
    if poss:
        part1 += 1
    narr = n_arrangements(pattern)
    part2 += narr

print(part1)
print(part2)
