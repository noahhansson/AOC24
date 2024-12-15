from utils import read_input, timer, setup_args
from classes import Point
from collections.abc import Iterator

args = setup_args()


def parse_input(test: bool = False) -> dict[Point, str]:
    plots = {}
    inpt = read_input("12", test=test)

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            plots[Point(x, y)] = c

    return plots


def get_neighbours(p: Point) -> Iterator[Point]:
    for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        yield p + dir


def flood_fill(p: Point, plant: str, plots: dict[Point, str], seen: set[Point] = set()) -> set[Point]:
    seen.add(p)
    for neighbour in get_neighbours(p):
        if (neighbour in plots.keys()) and (plots[neighbour] == plant) and (neighbour not in seen):
            seen = seen | flood_fill(neighbour, plant, plots, seen)

    return seen


def get_regions(plots: dict[Point, str]) -> list[set[Point]]:
    regions: list[set[Point]] = []
    while len(plots) > 0:
        plot, plant = plots.popitem()
        region = flood_fill(plot, plant, plots, seen=set())

        for p in region:
            _ = plots.pop(p, None)

        regions.append(set(region))

    return regions


@timer
def get_first_solution(test: bool = False):
    plots = parse_input(test)
    regions = get_regions(plots)

    score = 0

    for region in regions:
        size = len(region)
        perimeter = 0
        for plot in region:
            perimeter += len([p for p in get_neighbours(plot) if p not in region])

        score += size * perimeter

    return score


def find_sides(
    region: set[Point],
    starting_point: Point | None = None,
) -> tuple[int, set[Point]]:
    if starting_point is None:
        # Find starting point
        max_x = max([p.x for p in region])
        max_y = max([p.y for p in region if p.x == max_x])
        starting_point = Point(max_x, max_y) + (0, 1)

    # Determine if to start down or right
    # If starting right when it is not a valid move leads to late termination
    starting_direction = (1, 0)
    if (starting_point + starting_direction) in region:
        starting_direction = (0, 1)

    seen: set[tuple[Point, tuple[int, int]]] = set()
    current_point = starting_point
    current_direction = starting_direction
    sides = 0

    while (current_point, current_direction) not in seen:
        seen.add((current_point, current_direction))

        # left (1 rotation),
        # forwards (0 rotations),
        # right (1 rotation),
        # backwards (2 rotations)
        dx, dy = current_direction
        directions = (
            ((dy, -dx), 1),
            ((dx, dy), 0),
            ((-dy, dx), 1),
            ((-dx, -dy), 2),
        )

        for direction, n_rotations in directions:
            if (current_point + direction) not in region:
                sides += n_rotations
                current_point += direction
                current_direction = direction
                break
        else:
            # Edge case, one interior point
            sides += 4
            break

    return sides, {p for p, _ in seen}


@timer
def get_second_solution(test: bool = False):
    plots = parse_input(test)
    regions = get_regions(plots)

    score = 0

    for region in regions:
        size = len(region)
        sides, boundary = find_sides(region)

        # Find and calculate interior points
        interior_points = set()
        for plot in region:
            for neighbour in get_neighbours(plot):
                if (neighbour not in region) and (neighbour not in boundary):
                    interior_points.add(neighbour)

        while interior_points:
            xmin = min(p.x for p in interior_points)
            ymin = min(p.y for p in interior_points if p.x == xmin)
            sides_interior, boundary_interior = find_sides(region, Point(xmin, ymin))
            sides += sides_interior
            boundary |= boundary_interior

            interior_points -= boundary_interior

        score += size * sides

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
