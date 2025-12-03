from aoc_tools import nums, read_data

registers, program = read_data().split("\n\n")

A, B, C = nums(registers)
ops = tuple(nums(program))


def adv(x, y):
    return int(x / (2**y))


def bxl(x, y):
    return x ^ y


def bxc(x, y):
    return x ^ y


def bst(x):
    return x % 8


def bdv(*args):
    return adv(*args)


def cdv(*args):
    return adv(*args)


output = []

# opcode, operand
ipointer = 0
while ipointer < len(program):
    opcode, operand = ops[ipointer], ops[ipointer + 1]
    ipointer += 2

    match operand:
        case 0 | 1 | 2 | 3:
            value = operand
        case 4:
            value = A
        case 5:
            value = B
        case 6:
            value = C
        case 7:
            raise ValueError("Reserved operand")
        case _:
            raise ValueError(f"Invalid operand: {operand}")

    match opcode:
        case 0:
            A = adv(A, value)
        case 1:
            B = bxl(B, operand)
        case 2:
            B = bst(value)
        case 3:
            if A != 0:
                ipointer = operand
        case 4:
            B = bxc(B, C)
        case 5:
            output.append(value % 8)
        case 6:
            B = bdv(A, value)
        case 7:
            C = bdv(A, value)

print(",".join(map(str, output)))
