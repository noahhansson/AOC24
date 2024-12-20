from utils import read_input, timer, setup_args, iter_input
from classes import Point
from collections import defaultdict
from collections.abc import Iterator
from functools import cache

args = setup_args()


def parse_input(test: bool = False) -> tuple[set[Point], Point, Point]:
    inpt = read_input("20", test=test)

    walls: set[Point] = set()
    start: Point | None = None
    end: Point | None = None

    for x, y, c in iter_input(inpt):
        if c == "#":
            walls.add(Point(x, y))
        if c == "S":
            start = Point(x, y)
        if c == "E":
            end = Point(x, y)

    assert start is not None
    assert end is not None

    return walls, start, end


def get_neighbours(p: Point) -> Iterator[Point]:
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for d in directions:
        yield p + d


def find_distances(
    start: Point, end: Point, walls: set[Point]
) -> dict[Point, int]:
    distances: dict[Point, int] = {}
    position = end
    i = 0
    while position != start:
        distances[position] = i
        neighbours = [
            n
            for n in get_neighbours(position)
            if (n not in distances) and (n not in walls)
        ]

        assert len(neighbours) == 1

        position = neighbours[0]
        i += 1

    distances[start] = i

    return distances


@cache
def find_shortcuts(pos: Point, max_steps: int) -> set[Point]:
    adj: set[Point] = {pos}

    if max_steps == 0:
        return adj

    for neighbour in get_neighbours(pos):
        adj |= find_shortcuts(neighbour, max_steps - 1)

    return adj


def solve(
    cheat_min: int, cheat_max: int, threshold: int, test: bool = False
) -> int:
    walls, start, end = parse_input(test)

    distances = find_distances(start, end, walls)

    # Pre-calculate relative search area to save run time
    shortcuts_rel = find_shortcuts(Point(0, 0), cheat_max)

    cheats: dict[int, int] = defaultdict(int)

    for pos in distances.keys():
        targets = {pos + s for s in shortcuts_rel if (pos + s) in distances}
        for target in targets:
            if distances[pos] - distances[target] >= threshold:
                cheat_length = (target - pos).abs()
                if cheat_min <= cheat_length <= cheat_max:
                    time_gain = (
                        distances[pos] - distances[target] - cheat_length
                    )

                    cheats[time_gain] += 1

    score = 0
    for time_gain, n_cheats in cheats.items():
        if time_gain >= threshold:
            score += n_cheats

    return score


@timer
def get_first_solution(test: bool = False) -> int:
    if test:
        threshold = 1
    else:
        threshold = 100
    return solve(cheat_min=2, cheat_max=2, threshold=threshold, test=test)


@timer
def get_second_solution(test: bool = False) -> int:
    if test:
        threshold = 50
    else:
        threshold = 100
    return solve(cheat_min=2, cheat_max=20, threshold=threshold, test=test)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
