from utils import read_input, timer, setup_args
from collections import defaultdict, deque
import re

args = setup_args()


def parse_input(test: bool = False) -> dict[str, set[str]]:
    inpt = read_input("23", test=test)

    graph: dict[str, set[str]] = defaultdict(set)

    for row in inpt:
        pair = re.findall(r"[a-z]{2}", row)

        graph[pair[0]].add(pair[1])
        graph[pair[1]].add(pair[0])

    return graph


def find_loops(
    graph: dict[str, set[str]], start_value: str, max_depth: int
) -> list[tuple[str, ...]]:
    queue: deque[list[str]] = deque()

    queue.append([start_value])

    loops: list[tuple[str, ...]] = []

    while queue:
        path = queue.popleft()

        if len(path) == max_depth:
            if start_value in graph[path[-1]]:
                loops.append(tuple(sorted(path)))

        else:
            neighbours = graph[path[-1]]
            for neighbour in neighbours:
                queue.append([*path, neighbour])

    return loops


@timer
def get_first_solution(test: bool = False):
    graph = parse_input(test)

    loops: set[tuple[str, ...]] = set()

    for node in graph.keys():
        loops |= set(find_loops(graph, node, 3))

    score = 0

    for loop in loops:
        if any([name.startswith("t") for name in loop]):
            score += 1

    return score


def find_interconnected(
    graph: dict[str, set[str]], start_value: str
) -> tuple[str, ...]:
    queue: deque[tuple[str, ...]] = deque()

    queue.append((start_value,))

    max_size: int = 0
    max_size_cluster: tuple[str, ...] | None = None

    while queue:
        connected = queue.popleft()

        if (size := len(connected)) > max_size:
            max_size = size
            max_size_cluster = connected

        neighbours = set()
        for node in connected:
            neighbours |= graph[node]

        for neighbour in neighbours:
            if all([c in graph[neighbour] for c in connected]):
                queue.append(tuple(sorted([*connected, neighbour])))
                break

    assert max_size_cluster is not None
    return max_size_cluster


@timer
def get_second_solution(test: bool = False) -> str:
    graph = parse_input(test)
    max_size: int = 0
    max_size_cluster: tuple[str, ...] | None = None

    for node in graph.keys():
        cluster = find_interconnected(graph, node)
        if (size := len(cluster)) > max_size:
            max_size_cluster = cluster
            max_size = size

    assert max_size_cluster is not None
    return ",".join(max_size_cluster)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
