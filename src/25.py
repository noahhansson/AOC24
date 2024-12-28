from utils import read_input, timer, setup_args, iter_input
from classes import Point
from itertools import product

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("25", test=test)

    inpt_items: list[list[str]] = []
    buffer: list[str] = []
    for row in inpt:
        if row == "":
            inpt_items.append(buffer)
            buffer = []
        else:
            buffer.append(row)
    inpt_items.append(buffer)

    keys: set[frozenset[Point]] = set()
    locks: set[frozenset[Point]] = set()

    for item in inpt_items:
        item_points = set()
        is_key = item[0][0] == "#"
        for x, y, c in iter_input(item):
            if c == "#":
                item_points.add(Point(x, y))

        if is_key:
            keys.add(frozenset(item_points))
        else:
            locks.add(frozenset(item_points))

    return keys, locks


@timer
def get_first_solution(test: bool = False):
    keys, locks = parse_input(test)

    score = 0

    for key, lock in product(keys, locks):
        if not key.intersection(lock):
            score += 1

    return score


print(f"P1: {get_first_solution(test=args.test)}")
