import re

with open("data/03.in") as f:
    data = f.read()


def debug(*msg):
    with open("day03.log", "a") as h:
        h.write(" ".join(str(m) for m in msg))
        h.write("\n")


# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
#                           xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

mul_re = re.compile("mul\\((\\d{1,3}),(\\d{1,3})\\)")

muls = mul_re.finditer(data)

# this won't work:
# - when using (.+) between don't() and do(),
#   sometimes the groups are too long, missing do() and resulting in too few skips

# - when using (.+?) between don't() an do(),
#   sometimes the groups are too short, missing don't() and resulting in too many skips
skip_re = re.compile("don't\\(\\)(.+)do\\(\\)")
skip_parts = skip_re.finditer(data)
skip_ranges = [range(*s.span()) for s in skip_parts]

last_dont = data.find("don't()", skip_ranges[-1].stop)
if last_dont > skip_ranges[-1].stop:
    skip_ranges.append(range(last_dont, len(data)))


def in_skip_range(mulx, muly, skip_ranges):
    for sr in skip_ranges:
        if mulx > sr.start and muly < sr.stop:
            # debug(f"Found in skip range: {data[sr.start:sr.stop]}")
            return True

    return False


part1 = 0
part2 = 0
for mul in muls:
    a, b = map(int, mul.groups())
    part1 += a * b
    mulx, muly = mul.span()

    if in_skip_range(mulx, muly, skip_ranges):
        debug(f"Skipping mul({a},{b})")
        # debug(f"Skipping {a}*{b}, it's in a skip range")
        # debug("-" * 80)
        continue

    debug(f"Adding mul({a},{b})")
    part2 += a * b


print(part1)  # correct: 185797128
print(part2)  # too high: 108356586

debug("-" * 80)

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
            debug(f"Adding mul({a},{b})")
            part2 += a * b
        else:
            debug(f"Skipping mul({a},{b})")

print(part1)  # correct: 185797128
print(part2)  # correct: 89798695
