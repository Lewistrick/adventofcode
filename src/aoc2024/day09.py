from aoc_tools import read_data


def show_mem(memory):
    for val in memory:
        if val is None:
            print(".", end="")
        else:
            print(val, end="")
    print()


data = read_data(day=9).strip()

cursor = 0  # position on the input string
fileidx = 0  # index number of the file
memory: list[int | None] = []
part1 = 0
is_file = True
for idx, block_size in enumerate(data):
    if idx % 2 == 0:
        # it's a file, start adding memory
        for _ in range(int(block_size)):
            memory.append(fileidx)
        fileidx += 1
    else:
        # it's a free space
        for _ in range(int(block_size)):
            memory.append(None)

# show_mem(memory)

cursor = 0
while cursor < len(memory):
    mem_value = memory[cursor]
    if mem_value is None:
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

part1 = sum(i * v for i, v in enumerate(memory) if v)
print(part1)

# find blocks of data and free spaces
data_blocks: dict[int, tuple[int, int]] = {}  # {value: (start, length)}
free_spaces: list[tuple[int, int]] = []  # [(start, length)]
curr_fileno = 0
curr_memidx = 0
for idx, val in enumerate(data):
    n = int(val)
    if n == 0:
        # zero spaces, don't process this
        continue
    elif idx % 2 == 0:
        # this is a data block
        data_blocks[curr_fileno] = (curr_memidx, n)
        curr_fileno += 1
    else:
        # this is a free space block
        free_spaces.append((curr_memidx, n))

    curr_memidx += n


rev_values: list[int] = sorted(data_blocks.keys(), reverse=True)
for data_value in rev_values:
    start, length = data_blocks[data_value]

    try:
        # find all free spaces that this data block fits in;
        # make sure it's to the left of the data;
        # then find the space with the lowest idx
        first_space_idx = min(
            (
                ii
                for ii, (idx, size) in enumerate(free_spaces)
                if length <= size and idx < start
            ),  # finds all free spaces with enoug space to the left
            key=lambda ii: free_spaces[ii][0],
        )
    except ValueError:
        # print(f"{data_value} can't be moved left")        # this data block doesn't fit anywhere
        continue

    new_start, space_size = free_spaces.pop(first_space_idx)
    # print(f"Moving {data_value} to index {new_start}")

    data_blocks[data_value] = (new_start, length)
    if space_size - length:
        free_spaces.append((new_start + length, space_size - length))

part2 = 0
for data_value, (start, length) in data_blocks.items():
    for i in range(start, start + length):
        part2 += data_value * i

print(part2)
