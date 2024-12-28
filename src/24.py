from utils import read_input, timer, setup_args
import re

args = setup_args()

type GatesType = dict[str, tuple[str, str, str]]
type WiresType = dict[str, int]


def parse_input(
    test: bool = False,
) -> tuple[GatesType, WiresType]:
    inpt = read_input("24", test=test)

    wires: WiresType = {}
    gates: GatesType = {}

    for row in inpt:
        if ":" in row:
            wire, value = re.findall(r"[x|y]\d{2}|[1|0]", row)
            wires[wire] = int(value)

        elif "->" in row:
            wire_1, gate, wire_2, target = re.findall(
                r"[a-z]{3}|[x|y|z]\d{2}|OR|AND|XOR", row
            )
            gates[target] = (wire_1, gate, wire_2)

    return gates, wires


def eval_gate(wire_1, op, wire_2, wires: WiresType, gates: GatesType):
    if wire_1 in wires:
        value_1 = wires[wire_1]
    else:
        value_1 = eval_gate(*gates[wire_1], wires, gates)
        wires[wire_1] = value_1

    if wire_2 in wires:
        value_2 = wires[wire_2]
    else:
        value_2 = eval_gate(*gates[wire_2], wires, gates)
        wires[wire_2] = value_2

    if op == "AND":
        return value_1 & value_2
    elif op == "XOR":
        return value_1 ^ value_2
    elif op == "OR":
        return value_1 | value_2


def eval_device(gates: GatesType, wires: WiresType) -> str:
    z_wires = sorted(
        [
            wire
            for wire in set(wires.keys()) | set(gates.keys())
            if wire.startswith("z")
        ],
        key=lambda x: int(x.replace("z", "")),
        reverse=True,
    )

    final_value = ""

    for wire in z_wires:
        if wire in wires:
            value = wires[wire]
        elif wire in gates:
            value = eval_gate(*gates[wire], wires, gates)
            wires[wire] = value

        final_value += str(value)

    return final_value


@timer
def get_first_solution(test: bool = False):
    gates, wires = parse_input(test)
    final_value = eval_device(gates, wires)

    return int(final_value, 2)


def test_device(x_input: int, y_input: int, gates: GatesType) -> int:
    wires: WiresType = {}
    for i, x_val in enumerate(f"{x_input :045b}"[::-1]):
        wires[f"x{i :02d}"] = int(x_val)

    for i, y_val in enumerate(f"{y_input :045b}"[::-1]):
        wires[f"y{i :02d}"] = int(y_val)

    value = int(eval_device(gates, wires), 2)

    if (x_input + y_input) != value:
        print(f"   {x_input :045b}")
        print(f"+  {y_input :045b}")
        print(f"= {value :046b}")
        print(f"  Bit {i} has an error")
        print()
        return False

    return True


def swap_gates(key_1, key_2, gates: GatesType) -> GatesType:
    gate_temp_1 = gates[key_1]
    gate_temp_2 = gates[key_2]
    gates[key_1] = gate_temp_2
    gates[key_2] = gate_temp_1

    return gates


@timer
def get_second_solution(test: bool = False):
    gates, _ = parse_input(test)

    "Solved with pen and paper, studying input and trial and error"

    fixed = True
    for i in range(45):
        if not test_device(2**i, 2**i, gates):
            fixed = False

    if fixed:
        print("Device repaired")

    """
    First finding:
        z-output must be from a XOR gate, else the carry bit will not work. 
        For example: "y09 AND x09 -> z09".
        Last bit (z45) is excepted from this rule

        Identified outputs: 
        1. jnh OR njq -> z24
            z24 should be replaced with the gate XORd by x25 XOR y25
            Swap z24 with vcg
        2. qkq AND stj -> z20
            - Both are involved in another gate using XOR. Swap them?
            - Swap with "stj XOR qkq -> jgb"
        3. y09 AND x09 -> z09
            This is be the carry bit, which should be involved in the next
            bit output.
            Using z02 as example: we have 
                "x01 AND y01 -> mkr"
                "mkr OR tqp -> fhf"
                "fht XOR fhf -> z02"
            Examining z10 we find:
                "jnn XOR wpr -> rkf"
                "rkf OR hvk -> tcs"
                "tcs XOR hwg -> z10"

            Replace z09 with rkf

    """

    print("___________________________________________________")
    gates = swap_gates("z20", "jgb", gates)
    gates = swap_gates("z09", "rkf", gates)
    gates = swap_gates("z24", "vcg", gates)

    fixed = True
    for i in range(45):
        if not test_device(2**i, 2**i, gates):
            fixed = False

    if fixed:
        print("Device repaired")

    """
    Only one error remains
    Error is somewhere around bit 31
    Switch output of "x31 AND y31 -> rrs" with "x31 XOR y31 -> rvc"
    """
    print("___________________________________________________")
    gates = swap_gates("rrs", "rvc", gates)

    fixed = True
    for i in range(45):
        if not test_device(2**i, 2**i, gates):
            fixed = False

    if fixed:
        print("Device repaired")

    swaps = ",".join(
        sorted(["z20", "jgb", "z09", "rkf", "z24", "vcg", "rrs", "rvc"])
    )

    return swaps


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
