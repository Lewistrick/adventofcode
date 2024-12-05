from aoc_tools import read_data

lines = read_data(day=5)
pairlines, updatelines = lines.split("\n\n")
pairs = {tuple(map(int, p.split("|"))) for p in pairlines.split()}


def checkline_p1(line: str) -> int:
    update = tuple(map(int, line.split(",")))
    for i, n1 in enumerate(update[:-1]):
        for n2 in update[i + 1 :]:
            if (n2, n1) in pairs:
                return 0

    return update[len(update) // 2]


def find_first_page_index(pages: list[int]) -> int:
    if len(pages) == 1:
        return 0

    first = pages[0]
    first_idx = 0
    for idx, p in enumerate(pages[1:], 1):
        if (p, first) in pairs:
            first = p
            first_idx = idx

    return first_idx


def sort_p2(line: str):
    update = list(map(int, line.split(",")))

    correct = []
    while update:
        idx = find_first_page_index(update)
        correct.append(update.pop(idx))

    return correct[len(correct) // 2]


p1 = 0
p2 = 0
for line in updatelines.split():
    mid = checkline_p1(line)
    if not mid:
        p2 += sort_p2(line)
    p1 += mid

print(p1)
print(p2)
