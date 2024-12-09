from aoc_tools import read_data


def show_mem(memory):
    for val in memory:
        if val is None:
            print(".", end="")
        else:
            print(val, end="")
    print()


data = read_data().strip()
# data = read_data(suffix="ex").strip()

cursor = 0  # position on the input string
fileidx = 0  # index number of the file
memory: list[int | None] = []
part1 = 0
is_file = True
for idx, value in enumerate(data):
    if idx % 2 == 0:
        # it's a file, start adding memory
        for _ in range(int(value)):
            memory.append(fileidx)
        fileidx += 1
    else:
        # it's a free space
        for _ in range(int(value)):
            memory.append(None)

# show_mem(memory)

cursor = 0
while cursor < len(memory):
    value = memory[cursor]
    if value is None:
        # grab the value from the back
        while True:
            last = memory.pop()
            if last is not None:
                break

        if cursor >= len(memory):
            break

        memory[cursor] = last

    cursor += 1

# show_mem(memory)

part1 = sum(i * v for i, v in enumerate(memory))
print(part1)

# find blocks of data and free spaces
data_blocks = {}  # {value: (start, length)}
free_spaces = []  # [(start, length)]
curridx = 0
curr_fileidx = 0
for idx, val in enumerate(data):
    if idx % 0 == 0:
        data_blocks[curr_fileidx] = (curridx, int(val))
        curr_fileidx += 1
    else:
        free_spaces.append((curridx, int(val)))

for start, length in enumerate(data_blocks[::-1]):
    for idx, size in enumerate(free_spaces):
        if length <= size:
            # move the data block to the free space