from utils import read_input, timer, setup_args

args = setup_args()

type Point = tuple[int, int]
type Direction = tuple[int, int]

def parse_input(test:bool = False) -> tuple[set[Point], Point, int, int]:

    inpt = read_input('06', test=test)

    obstacles: set[Point] = set()
    start_pos: Point

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                obstacles.add((x, y))
            if c == "^":
                start_pos = (x, y)

    xmax = len(inpt[0])
    ymax = len(inpt)

    return obstacles, start_pos, xmax, ymax

def rotate_90(d: Direction) -> Direction:
    return (-d[1], d[0])


def is_in_bounds(p: Point, xlim: tuple[int, int], ylim: tuple[int, int]) -> bool:
    return all([xlim[0] <= p[0] < xlim[1], ylim[0] <= p[1] < ylim[1]])


def simulate_path(
    pos: Point, direction: Direction, obstacles: set[Point], xlim: tuple[int, int], ylim: tuple[int, int]
) -> set[Point]:
    seen: set[Point] = set()

    while is_in_bounds(pos, xlim, ylim):
        seen.add(pos)
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos not in obstacles:
            pos = next_pos
        else:
            direction = rotate_90(direction)

    return seen


def will_loop(
    pos: Point, direction: Direction, obstacles: set[Point], xlim: tuple[int, int], ylim: tuple[int, int]
) -> bool:

    seen: set[tuple[Point, Direction]] = set()

    while is_in_bounds(p=pos, xlim=xlim, ylim=ylim):
        if (pos, direction) in seen:
            return True
        else:
            seen.add((pos, direction))

        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos not in obstacles:
            pos = next_pos
        else:
            direction = rotate_90(direction)
    return False


@timer
def get_first_solution(test: bool = False):
    obstacles, start_pos, xmax, ymax = parse_input(test=test)
    return len(simulate_path(start_pos, (0, -1), obstacles, (0, xmax), (0, ymax)))


@timer
def get_second_solution(test: bool = False):
    obstacles, start_pos, xmax, ymax = parse_input(test=test)
    score = 0
    for p in simulate_path(start_pos, (0, -1), obstacles, (0, xmax), (0, ymax)):
        if p != start_pos and will_loop(start_pos, (0, -1), obstacles | {p}, (0, xmax), (0, ymax)):
            score += 1
    return score


print(f" P1: {get_first_solution(test=args.test)}")
print(f" P2: {get_second_solution(test=args.test)}")
