import re

with open("data/03.in") as f:
    data = f.read()

all_re = re.compile("mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)")
go = True
part1 = 0
part2 = 0
for cap in all_re.findall(data):
    if cap == "do()":
        go = True
    elif cap == "don't()":
        go = False
    else:
        a, b = map(int, re.findall("\\d+", cap))
        part1 += a * b
        if go:
            part2 += a * b

print(part1)
print(part2)
