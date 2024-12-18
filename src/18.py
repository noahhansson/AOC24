from utils import read_input, timer, setup_args
from classes import Point
from collections import deque
from collections.abc import Iterator
import re

args = setup_args()


def parse_input(test: bool = False) -> list[Point]:
    inpt = read_input("18", test=test)

    points: list[Point] = []
    for row in inpt:
        x, y = map(int, re.findall(r"\d+", row))
        points.append(Point(x, y))
    return points


def get_neighbours(p: Point) -> Iterator[Point]:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yield p + (dx, dy)


def in_bounds(p: Point, xmax: int, ymax: int) -> bool:
    return (0 <= p.x <= xmax) and (0 <= p.y <= ymax)


def bfs(start: Point, end: Point, obstacles: set[Point]) -> int:
    seen: set[Point] = set()
    queue: deque[tuple[int, Point]] = deque()

    xmax = end.x
    ymax = end.y

    queue.append((0, start))
    seen.add(start)

    while queue:
        step, point = queue.popleft()

        if point == end:
            return step

        for neighbour in get_neighbours(point):
            if (
                (neighbour not in seen)
                and (neighbour not in obstacles)
                and in_bounds(neighbour, xmax, ymax)
            ):
                queue.append((step + 1, neighbour))
                seen.add(neighbour)

    return -1


def binary_search(
    pmin: int, pmax: int, start: Point, end: Point, points: list[Point]
) -> int:
    if pmin == pmax:
        return pmin

    pmid = pmin + (pmax - pmin) // 2 + 1

    if bfs(start, end, set(points[:pmid])) > 0:
        return binary_search(pmid, pmax, start, end, points)
    else:
        return binary_search(pmin, pmid - 1, start, end, points)


@timer
def get_first_solution(test: bool = False) -> int:
    if test:
        xmax, ymax = (6, 6)
        n_points = 12
    else:
        xmax, ymax = (70, 70)
        n_points = 1024

    points = parse_input(test)
    corrupted = set(points[:n_points])

    return bfs(Point(0, 0), Point(xmax, ymax), corrupted)


@timer
def get_second_solution(test: bool = False) -> str:
    if test:
        xmax, ymax = (6, 6)
    else:
        xmax, ymax = (70, 70)

    points = parse_input(test)

    idx = binary_search(0, len(points), Point(0, 0), Point(xmax, ymax), points)

    assert bfs(Point(0, 0), Point(xmax, ymax), set(points[:idx])) != -1
    assert bfs(Point(0, 0), Point(xmax, ymax), set(points[: idx + 1])) == -1

    p = points[idx]

    return f"{p.x},{p.y}"


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
