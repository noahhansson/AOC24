from utils import read_input, timer, setup_parser
import re

parser = setup_parser()
args = parser.parse_args()

@timer
def get_first_solution(test: bool = args.test):
    inpt = read_input("03", test=test)
    score = 0
    for row in inpt:
        muls = re.findall("mul\(\d{1,3},\d{1,3}\)", row)
        for mul in muls:
            digits = [int(x) for x in re.findall("\d{1,3}", mul)]
            score += digits[0] * digits[1]

    return score

@timer
def get_second_solution(test: bool = args.test):
    inpt = read_input("03", test=test)
    score = 0
    do = True
    for row in inpt:
        instructions = re.findall("(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", row)
        for instruction in instructions:
            if instruction.startswith("mul") and do:
                digits = [int(x) for x in re.findall("\d{1,3}", instruction)]
                score += digits[0] * digits[1]
            if instruction == "do()":
                do = True
            if instruction == "don't()":
                do = False
    return score

print(f" P1: {get_first_solution()}")
print(f" P2: {get_second_solution()}")