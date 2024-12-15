from itertools import count

from aoc_tools import NESW, read_data

grid, moves = read_data(day=15, suffix="ex2").split("\n\n")
grid = grid.split("\n")

walls = set()
stones = set()
boxes = set()  # for part 2

for y, row in enumerate(grid):
    for x, val in enumerate(row):
        if val == ".":
            continue
        if val == "#":
            walls.add((x, y))
        if val == "O":
            stones.add((x, y))
        if val == "@":
            rx, ry = x, y

dirs = {ch: dir for dir, ch in zip(NESW, "^>v<")}

doshow = False


def show(rx, ry, override=False):
    if not doshow and not override:
        return
    for y in range(len(grid)):
        print(f"row {y}", end=": ")
        for x in range(len(grid[0])):
            if (x, y) == (rx, ry):
                print("@", end="")
            elif (x, y) in boxes:
                print("[", end="")
            elif (x - 1, y) in boxes:
                print("]", end="")
            elif (x, y) in walls:
                print("#", end="")
            elif (x, y) in stones:
                print("O", end="")
            else:
                print(".", end="")
        print()


def show_new(rx, ry, override=False):
    if not doshow and not override:
        return
    for y in range(len(grid)):
        print(f"row {y:2d}", end=": ")
        for x in range(len(grid[0]) * 2):
            if (x, y) == (rx, ry):
                print("@", end="")
            elif (x, y) in boxes:
                print("[", end="")
            elif (x - 1, y) in boxes:
                print("]", end="")
            elif (x, y) in walls:
                print("#", end="")
            elif (x, y) in stones:
                print("O", end="")
            else:
                print(".", end="")
        print()


for movech in moves:
    if not movech.split():
        continue
    dx, dy = dirs[movech]

    if doshow:
        input(f"Next move: {movech} >> ")

    nx, ny = rx + dx, ry + dy
    if (nx, ny) in walls:
        show(rx, ry)
        continue

    if (nx, ny) not in stones:
        # it's an empty space
        rx, ry = nx, ny
        show(rx, ry)
        continue

    # it's a stone; let's see if we can move it
    can_move = None
    for i in count(2):
        tx, ty = (rx + i * dx), (ry + i * dy)
        if (tx, ty) in stones:
            continue
        elif (tx, ty) in walls:
            can_move = False
            break
        else:
            can_move = True
            break

    if not can_move:
        show(rx, ry)
        continue

    # move the first stone from the row to the back
    stones.remove((nx, ny))
    stones.add((tx, ty))
    rx, ry = nx, ny

    show(rx, ry)

show(rx, ry)

part1 = 0
for sx, sy in sorted(stones):
    part1 += (100 * sy) + sx

print(part1)
print("-" * 150)

# start over for part 2
walls = set()
stones = set()
boxes = set()
empty = set()

R = {".": "..", "#": "##", "O": "[]", "@": "@."}
for y, row in enumerate(grid):
    newrow = "".join(R[x] for x in row)
    for x, val in enumerate(newrow):
        if val == ".":
            empty.add((x, y))
        if val == "#":
            walls.add((x, y))
        if val == "[":
            boxes.add((x, y))
        if val == "@":
            rx, ry = x, y

doshow = True
show_new(rx, ry)
for movech in moves:
    if not movech.split():
        continue
    dx, dy = dirs[movech]

    if doshow:
        input(f"Next move: {movech} >> ")

    nx, ny = rx + dx, ry + dy
    if (nx, ny) in walls:
        if doshow:
            print("Wall in the way")
            show_new(rx, ry)
        continue

    if (nx, ny) in empty:
        rx, ry = nx, ny
        if doshow:
            print("Empty space found, moving")
            show_new(rx, ry)

        continue

    # it's a box
    can_move = True
    move_boxes = set()
    bx, by = (nx, ny) if (nx, ny) in boxes else (nx - 1, ny)
    move_boxes.add((bx, by))
    if dy == 0:
        # horizontal movement (easy)
        for step in count():
            tx, ty = (bx + dx * step, by)
            if (tx, ty) in boxes:
                move_boxes.add((tx, ty))
            elif (tx - 1, ty) in boxes:
                move_boxes.add((tx, ty))
            elif (tx, ty) in walls:
                can_move = False
                break
            elif (tx, ty) in empty:
                can_move = True
                break
        if can_move:
            for bx, by in move_boxes:
                boxes.remove((bx, by))
                boxes.add((bx + dx, by))
                empty.add((rx, ry))
            # move the robot
            rx, ry = nx, ny
        show_new(rx, ry)
    else:
        # vertical movement
        stack = [(bx, by)]
        while stack:
            tx, ty = stack.pop(0)

            # if it's blocked by a wall, stop checking
            if (tx, ty + dy) in walls or (tx + 1, ty + dy) in walls:
                can_move = False
                break

            # if both are empty, keep checking
            if (tx, ty + dy) in empty and (tx + 1, ty + dy) in empty:
                continue

            # oh no, there's a box; add it to the stack
            if (tx, ty + dy) in boxes:
                stack.append((tx, ty + dy))
            else:
                stack.append((tx + 1, ty + dy))
                assert ((tx + 1, ty + dy)) in boxes

        if can_move:
            # first, move the boxes
            for bx, by in move_boxes:
                boxes.remove((bx, by))
                boxes.add((bx, by + dy))
            # then, re-check empty positions (move_boxes now contains old positions)
            for bx, by in move_boxes:
                # left side: (bx, by)
                if (bx, by) not in boxes and (bx - 1, by) not in boxes:
                    empty.add(bx, by)
                # right side: (bx+1, by)
                if (bx + 1, by) not in boxes and (bx, by) not in boxes:
                    empty.add(bx - 1, by)
            # move the robot
            rx, ry = nx, ny

    show_new(rx, ry)
