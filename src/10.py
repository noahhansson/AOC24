from utils import read_input, timer, setup_args

type PointType = tuple[int, int]
type MapType = dict[PointType, int]

args = setup_args()


def parse_input(test: bool = False) -> MapType:
    inpt = read_input("10", test=test)

    map: MapType = {}

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            map[(x, y)] = int(c)

    return map


def get_neighbours(position: PointType) -> list[PointType]:
    neighbours = []
    for dy, dx in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        neighbours.append((position[0] + dx, position[1] + dy))
    return neighbours


def find_trail(position: PointType, map: MapType) -> list[PointType]:
    next_positions = []

    current_height = map[position]
    if current_height == 9:
        return [position]

    for neighbour in get_neighbours(position):
        if neighbour in map.keys():
            neighbour_height = map[neighbour]

            if neighbour_height == current_height + 1:
                next_positions.append(neighbour)

    trailheads: list[PointType] = []
    for next_position in next_positions:
        trailheads = trailheads + find_trail(next_position, map)

    return trailheads


@timer
def get_first_solution(test: bool = False):
    map = parse_input(test)

    starts = [k for k, v in map.items() if v == 0]

    score = 0

    for start in starts:
        score += len(set(find_trail(start, map)))

    return score


@timer
def get_second_solution(test: bool = False):
    map = parse_input(test)

    starts = [k for k, v in map.items() if v == 0]

    score = 0

    for start in starts:
        score += len(find_trail(start, map))

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
