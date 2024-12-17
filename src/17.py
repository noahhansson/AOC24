from utils import read_input, timer, setup_args
from collections.abc import Iterator
import re

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("17", test=test)
    a, b, c, *program = map(int, re.findall(r"\d+", "\n".join(inpt)))
    return a, b, c, program


class Computer:
    registry_a: int
    registry_b: int
    registry_c: int
    output: int | None
    pointer: int

    def __init__(self, a: int, b: int, c: int) -> None:
        self.registry_a = a
        self.registry_b = b
        self.registry_c = c

        self.output = None
        self.pointer = 0

    def get_value(self, combo: int) -> int:
        combo_map = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.registry_a,
            5: self.registry_b,
            6: self.registry_c,
        }
        return combo_map[combo]

    def adv(self, combo: int) -> None:
        value = self.get_value(combo)
        self.registry_a = self.registry_a >> value
        self.pointer += 2

    def bxl(self, combo: int) -> None:
        self.registry_b = self.registry_b ^ combo
        self.pointer += 2

    def bst(self, combo: int) -> None:
        value = self.get_value(combo)
        self.registry_b = value & 7
        self.pointer += 2

    def jnz(self, combo: int) -> None:
        if self.registry_a != 0:
            self.pointer = combo
        else:
            self.pointer += 2

    def bxc(self, combo: int) -> None:
        self.registry_b = self.registry_b ^ self.registry_c
        self.pointer += 2

    def out(self, combo: int) -> None:
        value = self.get_value(combo)
        self.output = value & 7
        self.pointer += 2

    def bdv(self, combo: int) -> None:
        value = self.get_value(combo)
        self.registry_b = self.registry_a >> value
        self.pointer += 2

    def cdv(self, combo: int) -> None:
        value = self.get_value(combo)
        self.registry_c = self.registry_a >> value
        self.pointer += 2

    def run_program(self, program: list[int]) -> Iterator[int]:
        while self.pointer < len(program) - 1:
            opcode = program[self.pointer]
            combo = program[self.pointer + 1]

            opcode_map = {
                0: self.adv,
                1: self.bxl,
                2: self.bst,
                3: self.jnz,
                4: self.bxc,
                5: self.out,
                6: self.bdv,
                7: self.cdv,
            }

            opcode_map[opcode](combo)
            if self.output is not None:
                yield self.output
                self.output = None


def run_test_cases() -> None:
    comp = Computer(0, 0, 9)
    _ = list(comp.run_program([2, 6]))
    assert comp.registry_b == 1

    comp = Computer(10, 0, 0)
    assert ",".join(map(str, comp.run_program([5, 0, 5, 1, 5, 4]))) == "0,1,2"

    comp = Computer(2024, 0, 0)
    assert (
        ",".join(map(str, comp.run_program([0, 1, 5, 4, 3, 0])))
        == "4,2,5,6,7,7,7,7,3,1,0"
    )
    assert comp.registry_a == 0

    comp = Computer(0, 29, 0)
    _ = list(comp.run_program([1, 7]))
    assert comp.registry_b == 26

    comp = Computer(0, 2024, 43690)
    _ = list(comp.run_program([4, 0]))
    assert comp.registry_b == 44354


@timer
def get_first_solution(test: bool = False) -> str:
    a, b, c, program = parse_input(test)

    comp = Computer(a, b, c)
    return ",".join(map(str, comp.run_program(program)))


def find_register(program: list[int], index: int, current_register: str) -> str:
    if index < 0:
        return current_register
    for x in range(0, 8):
        try_register = int(f"{current_register}{x}", 8)
        comp = Computer(try_register, 0, 0)
        res = next(comp.run_program(program))
        if res == program[index]:
            if (
                reg := find_register(program, index - 1, f"{oct(try_register)}")
            ) != "":
                return reg
    return ""


@timer
def get_second_solution(test: bool = False) -> int:
    _, b, c, program = parse_input(test)

    res = find_register(program, len(program) - 1, "")

    a = int(res, 8)
    comp = Computer(a, b, c)
    output = list(comp.run_program(program))
    assert output == program

    return a


run_test_cases()
print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
