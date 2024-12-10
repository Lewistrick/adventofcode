from aoc_tools import NESW, read_data

data = read_data(suffix="in").split("\n")
vals = {}
starts = []
for y, col in enumerate(data):
    for x, val in enumerate(col):
        if val == ".":
            continue
        vals[(x, y)] = int(val)
        if int(val) == 0:
            starts.append((x, y))


def get_score(x, y, use_seen=True):
    stack = [(x, y)]
    seen = {(x, y)}
    score = 0
    while stack:
        x, y = stack.pop()
        for dx, dy in NESW:
            new = x + dx, y + dy
            if new in seen and use_seen:
                continue
            if (newval := vals.get((new))) == vals[(x, y)] + 1:
                if newval == 9:
                    score += 1
                else:
                    stack.append((new))
                seen.add((new))
    return score


p1 = p2 = 0
for start in starts:
    p1 += get_score(*start)
    p2 += get_score(*start, use_seen=False)

print(p1)
print(p2)
