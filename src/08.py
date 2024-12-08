from utils import read_input, timer, setup_args
from collections import defaultdict
from itertools import combinations

args = setup_args()

type Coord = tuple[int, int]


def parse_inpt(test: bool = False) -> tuple[dict[str, set[Coord]], int, int]:
    inpt = read_input("08", test=test)

    all_antennas: dict[str, set[Coord]] = defaultdict(set)

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c != ".":
                all_antennas[c].add((x, y))

    ymax = len(inpt)
    xmax = len(inpt[0])

    return all_antennas, xmax, ymax


def solve(p2: bool = False, test: bool = False) -> int:
    all_antennas, xmax, ymax = parse_inpt(test)

    nodes: set[Coord] = set()

    for antennas in all_antennas.values():
        for a1, a2 in combinations(antennas, 2):
            distance_x = a1[0] - a2[0]
            distance_y = a1[1] - a2[1]

            if not p2:
                next_node = (a1[0] + distance_x, a1[1] + distance_y)
                if (0 <= next_node[0] < xmax) and (0 <= next_node[1] < ymax):
                    nodes.add(next_node)

                next_node = (a2[0] - distance_x, a2[1] - distance_y)
                if (0 <= next_node[0] < xmax) and (0 <= next_node[1] < ymax):
                    nodes.add(next_node)

            else:
                next_node = a1
                while (0 <= next_node[0] < xmax) and (0 <= next_node[1] < ymax):
                    nodes.add(next_node)
                    next_node = (next_node[0] + distance_x, next_node[1] + distance_y)

                next_node = a2
                while (0 <= next_node[0] < xmax) and (0 <= next_node[1] < ymax):
                    nodes.add(next_node)
                    next_node = (next_node[0] - distance_x, next_node[1] - distance_y)

    return len(nodes)


@timer
def get_first_solution(test: bool = False):
    return solve(test=test)


@timer
def get_second_solution(test: bool = False):
    return solve(p2=True, test=test)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
