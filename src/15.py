from utils import read_input, timer, setup_args
from classes import Point
from dataclasses import dataclass
from typing import Self

args = setup_args()


@dataclass(frozen=True)
class BoxP2:
    x: tuple[int, int]
    y: int

    def move(self, direction: tuple[int, int]) -> Self:
        x = (self.x[0] + direction[0], self.x[1] + direction[0])
        y = self.y + direction[1]

        return self.__class__(x, y)

    def overlaps(self, other: Self) -> bool:
        return (self.y == other.y) and (
            (self.x[0] == other.x[0]) or (self.x[0] == other.x[1]) or (self.x[1] == other.x[0])
        )


def parse_input(test: bool = False) -> tuple[set[Point], set[Point], Point, list[str]]:
    inpt = read_input("15", test=test)

    walls: set[Point] = set()
    boxes: set[Point] = set()
    robot_pos: Point | None = None
    instructions: list[str] = []

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                walls.add(Point(x, y))
            elif c == "O":
                boxes.add(Point(x, y))
            elif c == "@":
                robot_pos = Point(x, y)
            elif c in (">", "^", "<", "v"):
                instructions.append(c)

    if robot_pos is None:
        raise RuntimeError("No robot found")

    return walls, boxes, robot_pos, instructions


def parse_input_p2(test: bool = False) -> tuple[set[Point], set[BoxP2], Point, list[str]]:
    inpt = read_input("15", test=test)

    walls: set[Point] = set()
    boxes: set[BoxP2] = set()
    robot_pos: Point | None = None
    instructions: list[str] = []

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                walls.add(Point(2 * x, y))
                walls.add(Point(2 * x + 1, y))
            elif c == "O":
                boxes.add(BoxP2((2 * x, 2 * x + 1), y))
            elif c == "@":
                robot_pos = Point(2 * x, y)
            elif c in (">", "^", "<", "v"):
                instructions.append(c)

    if robot_pos is None:
        raise RuntimeError("No robot found")

    return walls, boxes, robot_pos, instructions


def push(box_pos: Point, direction: tuple[int, int], boxes: set[Point], walls: set[Point]) -> bool:
    next_box_pos = box_pos + direction
    if next_box_pos in walls:
        return False
    elif next_box_pos not in boxes:
        boxes.add(next_box_pos)
        boxes.remove(box_pos)
        return True
    elif next_box_pos in boxes:
        if push(next_box_pos, direction, boxes, walls):
            boxes.add(next_box_pos)
            boxes.remove(box_pos)
            return True
        else:
            return False

    return False


def can_push_p2(box: BoxP2, direction: tuple[int, int], boxes: set[BoxP2], walls: set[Point]) -> bool:
    moved_box = box.move(direction)
    if (Point(moved_box.x[0], moved_box.y) in walls) or (Point(moved_box.x[1], moved_box.y) in walls):
        return False
    collisions = [b for b in boxes if moved_box.overlaps(b) and b != box]
    if collisions:
        return all([can_push_p2(b, direction, boxes, walls) for b in collisions])
    return True


def push_p2(box: BoxP2, direction: tuple[int, int], boxes: set[BoxP2]) -> None:
    moved_box = box.move(direction)
    collisions = [b for b in boxes if moved_box.overlaps(b) and b != box]
    for b in collisions:
        push_p2(b, direction, boxes)
    boxes.remove(box)
    boxes.add(moved_box)


@timer
def get_first_solution(test: bool = False):
    walls, boxes, robot_pos, instructions = parse_input(test)

    instruction_map = {"v": (0, 1), "<": (-1, 0), "^": (0, -1), ">": (1, 0)}

    for instruction in instructions:
        move = instruction_map[instruction]
        next_pos = robot_pos + move
        if next_pos in boxes:
            if push(next_pos, move, boxes, walls):
                robot_pos = next_pos
        elif next_pos not in walls:
            robot_pos = next_pos
        else:
            pass

    score = 0
    for box in boxes:
        score += 100 * box.y + box.x

    return score


@timer
def get_second_solution(test: bool = False):
    walls, boxes, robot_pos, instructions = parse_input_p2(test)

    instruction_map = {"v": (0, 1), "<": (-1, 0), "^": (0, -1), ">": (1, 0)}

    for instruction in instructions:
        move = instruction_map[instruction]
        next_pos = robot_pos + move
        blocked = False
        for box in boxes:
            if (next_pos == Point(box.x[0], box.y)) or (next_pos == Point(box.x[1], box.y)):
                if can_push_p2(box, move, boxes, walls):
                    push_p2(box, move, boxes)
                else:
                    blocked = True
                break

        if next_pos in walls:
            blocked = True

        if not blocked:
            robot_pos = next_pos

    score = 0
    for box in boxes:
        score += 100 * box.y + box.x[0]

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
