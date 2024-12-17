from utils import read_input, timer, setup_args
from collections import defaultdict
from itertools import chain

args = setup_args()


def parse_input(test: bool) -> tuple[dict[int, list[int]], list[list[int]]]:
    inpt = read_input("09", test=test)

    blocks: dict[int, list[int]] = defaultdict(list)
    spaces: list[list[int]] = []

    id_val = 0
    idx = 0
    for i, c in enumerate(inpt[0]):
        if i % 2 == 0:
            # Assign blocks
            blocks[id_val] += list(range(idx, idx + int(c)))
            id_val += 1
        elif (i % 2 == 1) and int(c) > 0:
            # Empty space
            spaces.append(list(range(idx, idx + int(c))))
        idx += int(c)

    return blocks, spaces


def calc_checksum(blocks: dict[int, list[int]]) -> int:
    score = 0
    for file_id, positions in blocks.items():
        for pos in positions:
            score += file_id * pos

    return score


@timer
def get_first_solution(test: bool = False):
    blocks, spaces = parse_input(test)

    spaces_lst: list[int] = list(chain(*spaces))

    max_id = max(blocks.keys())

    for block_id in range(max_id, 0, -1):
        max_pos = max(blocks[block_id])
        spaces_lst = [x for x in spaces_lst if x < max_pos]
        n_blocks = len(blocks[block_id])
        if len(spaces_lst) >= n_blocks:
            blocks[block_id] = spaces_lst[:n_blocks]
            spaces_lst = spaces_lst[n_blocks:]
        elif (n_spaces := len(spaces_lst)) > 0:
            blocks[block_id][-n_spaces:] = spaces_lst
            spaces_lst = []

    return calc_checksum(blocks)


@timer
def get_second_solution(test: bool = False):
    blocks, spaces = parse_input(test)

    max_id = max(blocks.keys())

    for block_id in range(max_id, 0, -1):
        block_size = len(blocks[block_id])

        space_idx = 0
        while space_idx < len(spaces) and (
            max(spaces[space_idx]) < max(blocks[block_id])
        ):
            if len(spaces[space_idx]) >= block_size:
                space = spaces[space_idx]
                if len(space) == block_size:
                    blocks[block_id] = space
                    del spaces[space_idx]
                elif len(space) > block_size:
                    spaces[space_idx] = space[block_size:]
                    blocks[block_id] = space[:block_size]
                break
            space_idx += 1

    return calc_checksum(blocks)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
