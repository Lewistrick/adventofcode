from loguru import logger

from aoc_tools import nums, product, read_data, rotate_grid_ccw


def solve_part1(data):
    num_rows = []
    for line in data[:-1]:
        num_rows.append(list(nums(line)))

    # rotate so that rows become columns
    num_cols = rotate_grid_ccw(num_rows)[::-1]
    operators = [ch for ch in data[-1] if ch != " "]

    part1 = 0
    for op, col in zip(operators, num_cols):
        if op == "+":
            sub = sum(col)
        elif op == "*":
            sub = product(col)
        else:
            continue

        part1 += sub

    logger.success(f"{part1=}")


def solve_part2(data):
    # read right-to-left
    rows = [row[::-1] for row in data]
    problem = []
    part2 = 0

    # iterate over every row simultaneously
    for col in zip(*rows):
        if all(x == " " for x in col):
            continue

        num = int("".join(x for x in col[:-1] if x != " "))
        problem.append(num)

        match col[-1]:
            case "+":
                sub = sum(problem)
                problem = []
            case "*":
                sub = product(problem)
                problem = []
            case _:
                continue
        
        part2 += sub
    logger.success(f"{part2=}")


def solve():
    data = read_data(suffix="in").split("\n")
    solve_part1(data)
    solve_part2(data)
