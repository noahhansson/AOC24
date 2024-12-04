from utils import read_input, timer, setup_args
import re

args = setup_args()

@timer
def get_first_solution(test: bool = False):
    inpt = read_input("04", test=test)

    all_rows = []

    #Horizontal
    for row in inpt:
        all_rows.append(row)

    #Vertical
    for i in range(len(inpt[0])):
        v_row = "".join([row[i] for row in inpt])
        all_rows.append(v_row)

    #Diagonal
    len_x = len(inpt[0])
    len_y = len(inpt)

    for y_start in range(len_y):
        diag_1: list[str] = []
        diag_2: list[str] = []
        x = 0
        y = y_start
        while x < len_x and y < len_y:
            diag_1 += inpt[y][x]
            diag_2 += inpt[len_y - y - 1][x]
            x+=1
            y+=1
        row_diag_1 = "".join(diag_1)
        row_diag_2 = "".join(diag_2)
        all_rows.append(row_diag_1)
        all_rows.append(row_diag_2)

    for x_start in range(1, len_x):
        diag_1 = []
        diag_2 = []
        x = x_start
        y = 0
        while x < len_x and y < len_y:
            diag_1 += inpt[y][x]
            diag_2 += inpt[len_y - y - 1][x]
            x+=1
            y+=1
        row_diag_1 = "".join(diag_1)
        row_diag_2 = "".join(diag_2)
        all_rows.append(row_diag_1)
        all_rows.append(row_diag_2)

    score = 0
    for row in all_rows:
        score += len(re.findall("XMAS", row))
        score += len(re.findall("XMAS", row[::-1]))

    return score


@timer
def get_second_solution(test: bool = False):
    inpt = read_input("04", test=test)

    score = 0

    for x in range(1, len(inpt[0]) - 1):
        for y in range(1, len(inpt) - 1):
            if (all([
                inpt[y-1][x-1] == "M",
                inpt[y][x] == "A",
                inpt[y + 1][x + 1] == "S"
            ]) or all([
                inpt[y-1][x-1] == "S",
                inpt[y][x] == "A",
                inpt[y + 1][x + 1] == "M"
            ])) and (all([
                inpt[y+1][x-1] == "M",
                inpt[y][x] == "A",
                inpt[y-1][x + 1] == "S"
            ]) or all([
                inpt[y+1][x-1] == "S",
                inpt[y][x] == "A",
                inpt[y-1][x + 1] == "M"
            ])):
                score += 1

    return score


print(f" P1: {get_first_solution(test=args.test)}")
print(f" P2: {get_second_solution(test=args.test)}")
