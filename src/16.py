from utils import read_input, timer, setup_args, iter_input
import heapq
from classes import Point
from collections import defaultdict
from collections.abc import Iterator

args = setup_args()


def parse_input(test: bool = False) -> tuple[set[Point], Point, Point]:
    inpt = read_input("16", test=test)

    walls: set[Point] = set()
    start: Point | None = None
    end: Point | None = None

    for x, y, c in iter_input(inpt):
        if c == "#":
            walls.add(Point(x, y))
        elif c == "S":
            start = Point(x, y)
        elif c == "E":
            end = Point(x, y)

    if start is None or end is None:
        raise RuntimeError()

    return walls, start, end


def get_neighbours(
    position: Point, direction: tuple[int, int], walls: set[Point]
) -> Iterator[tuple[int, Point, tuple[int, int]]]:
    current_position = position
    steps = 0
    while True:
        dx, dy = direction
        for next_direction in ((dy, -dx), (-dy, dx)):
            if (current_position + next_direction) not in walls:
                yield (1000 + steps, current_position, next_direction)

        if (current_position + direction) in walls:
            break

        steps += 1
        current_position = current_position + direction

    if steps > 0:
        yield (steps, current_position, direction)


def find_shortest(
    walls: set[Point], start: Point, end: Point
) -> tuple[int, set[Point]]:
    start_node: tuple[int, Point, tuple[int, int]] = (0, start, (1, 0))

    queue = [start_node]
    heapq.heapify(queue)

    seen: dict[tuple[Point, tuple[int, int]], int] = {}
    seen[(start, (1, 0))] = 0

    path_to: dict[Point, set[Point]] = defaultdict(set)

    min_score = -1

    i = 0

    while queue:
        i += 1
        score, position, direction = heapq.heappop(queue)

        if position == end:
            if (min_score < 0) or (score == min_score):
                min_score = score
            else:
                break
        for cost, next_pos, next_dir in get_neighbours(
            position, direction, walls
        ):
            # Strict constraing for being a faster route
            if (
                (next_pos, next_dir) not in seen
                or (seen[(next_pos, next_dir)] > (score + cost))
            ) and ((min_score < 0) or score + cost <= min_score):
                seen[(next_pos, next_dir)] = score + cost
                heapq.heappush(queue, (score + cost, next_pos, next_dir))

            # Relaxed constraint for being an equally fast route
            if (
                ((next_pos, next_dir) in seen)
                and seen[(next_pos, next_dir)] >= (score + cost)
            ) and ((min_score < 0) or (score + cost <= min_score)):
                next_path = [
                    position + (direction[0] * i, direction[1] * i)
                    for i in range(0, (cost % 1000) + 1)
                ]

                path_to[next_pos] |= path_to[position] | set(next_path)

    return min_score, path_to[end]


@timer
def get_first_solution(test: bool = False) -> int:
    walls, start, end = parse_input(test)
    score, _ = find_shortest(walls, start, end)
    return score


@timer
def get_second_solution(test: bool = False) -> int:
    walls, start, end = parse_input(test)
    _, path = find_shortest(walls, start, end)

    return len(path)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
