from functools import cache
from itertools import product

from aoc_tools import read_data
from tqdm import tqdm

data = read_data(day=7, suffix="in").split("\n")

@cache
def concat_values(a, b):
    return int(f"{a}{b}")


def part1(index, values, poss_ops: tuple[str, ...] = ("+", "*")):
    n_ops = len(values) - 1
    for ops in product(poss_ops, repeat=n_ops):
        val = values[0]

        for val2, op in zip(values[1:], ops):
            if op == "+":
                val += val2
            if op == "*":
                val *= val2
            if op == "||":
                val = concat_values(val, val2)

            if val > index:
                break

        if val == index:
            return True

    return False


p1 = 0
p2 = 0
for line in tqdm(data, "calculating", ascii=".#"):
    a, b = line.split(":")
    index = int(a)
    values = [int(n) for n in b.split()]
    if part1(index, values):
        p1 += index
        p2 += index
    elif part1(index, values, poss_ops=("||", "+", "*")):
        p2 += index

# 38798369315 too low
# 932137732557 correct
print(p1)

# 661823605105500 correct
print(p2)
