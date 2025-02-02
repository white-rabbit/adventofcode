import argparse
from collections import defaultdict, deque


class ChronospatialComputer:
    def __init__(self, code, register_a, register_b, register_c):
        self.code = code
        self.register_b_initial = register_b
        self.register_c_initial = register_c

        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c

        self.instruction_pointer = 0
        self.output = []
        self.instruction_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def get_output(self):
        return ",".join([str(x) for x in self.output])

    def is_halt(self):
        return self.instruction_pointer >= len(self.code)

    def do_next(self):
        instruction_pointer = self.instruction_pointer
        opcode, operand_code = (
            self.code[instruction_pointer],
            self.code[instruction_pointer + 1],
        )
        self.do_instruction(opcode, operand_code)
        # be sure there is no infinite loop
        assert instruction_pointer != self.instruction_pointer

    def execute(self):
        while not self.is_halt():
            self.do_next()

    def reset(self, register_a):
        self.register_a = register_a
        self.register_b = self.register_b_initial
        self.register_c = self.register_c_initial
        self.output_index = 0
        self.output = []
        self.instruction_pointer = 0

    def search(self, min_a, max_a, expected_output):
        register_a = None

        for a in range(min_a, max_a):
            self.reset(a)
            output_index = 0
            while not self.is_halt():
                self.do_next()

                if len(self.output) > output_index:
                    assert output_index < len(
                        expected_output
                    ), "Specify search interval more precisely"

                    if self.output[output_index] != expected_output[output_index]:
                        break

                    output_index += 1

            if output_index == len(expected_output):
                assert self.output == expected_output
                assert self.is_halt()
                register_a = a
                break

        return register_a

    def do_instruction(self, opcode, operand):
        assert opcode in self.instruction_map
        instruction_pointer = self.instruction_pointer
        self.instruction_map[opcode](operand)
        # print(f'Instruction: {opcode} {operand_code} {operand}')
        # print(f'Registers: {self.register_a} {self.register_b} {self.register_c}')
        # some of the instructions change the pointer
        if self.instruction_pointer == instruction_pointer:
            self.instruction_pointer += 2

    def combo_operand(self, operand_code):
        if operand_code == 4:
            return self.register_a
        elif operand_code == 5:
            return self.register_b
        elif operand_code == 6:
            return self.register_c
        else:
            return operand_code

    def adv(self, operand):
        operand = self.combo_operand(operand)
        self.register_a = self.register_a // (2**operand)

    def bdv(self, operand):
        operand = self.combo_operand(operand)
        self.register_b = self.register_a // (2**operand)

    def cdv(self, operand):
        operand = self.combo_operand(operand)
        self.register_c = self.register_a // (2**operand)

    def bxl(self, operand):
        self.register_b = self.register_b ^ operand

    def bst(self, operand):
        operand = self.combo_operand(operand)
        self.register_b = operand % 8

    def jnz(self, operand):
        if self.register_a != 0:
            self.instruction_pointer = operand

    def bxc(self, _):
        self.register_b = self.register_b ^ self.register_c

    def out(self, operand):
        operand = self.combo_operand(operand)
        self.output.append(operand % 8)


def solve(f):
    # IMPORTANT: This solution is not fast, consider to run it via pypy

    code = []
    lines = list(f)
    register_a = int(lines[0].split()[2])
    register_b = int(lines[1].split()[2])
    register_c = int(lines[2].split()[2])
    raw_code = lines[4].split()[1]
    code = [int(x) for x in raw_code.split(",")]

    program = ChronospatialComputer(code, register_a, register_b, register_c)
    program.execute()

    print("Answer 1: ", program.get_output())

    n = len(code)

    # Divide and Conquer
    # WARNING: this could not work in general case!
    center = n // 2
    brute_force_area = 1

    result = None

    for split_index in range(center - brute_force_area, center + brute_force_area + 1):
        left_side, right_side = code[:split_index], code[split_index:]
        print("Checking split", left_side, right_side)

        # otherwise the output is shorter than desired
        left_min_a = 8 ** (split_index - 1)
        # otherwise the output is larger than desired
        left_max_a = 8**split_index

        right_min_a = 8 ** (n - split_index - 1)
        right_max_a = 8 ** (n - split_index)

        left_a = None
        right_a = None

        # try to find the register value
        # for a smaller part first
        if left_min_a <= right_min_a:
            left_a = program.search(left_min_a, left_max_a, left_side)
            if not left_a:
                print("No register for this side. Ignore.")
        else:
            right_a = program.search(right_min_a, right_max_a, right_side)
            if not right_a:
                print("No register for this side. Ignore.")

        # only if for the smaller part the result is found
        # try to find result for the larger one
        if left_a is not None:
            right_a = program.search(right_min_a, right_max_a, right_side)

        if right_a is not None:
            left_a = program.search(left_min_a, left_max_a, left_side)

        if left_a is not None and right_a is not None:
            print("Found register values for both sides:", left_side, right_side)

            right_a_shifted = 8**split_index * right_a
            area_min = right_a_shifted - left_a
            area_max = right_a_shifted + left_a

            # search values around the found right side
            print("Brute force around the largest part", area_min, area_max)

            register_a = program.search(area_min, area_max, code)
            if register_a is not None:
                result = min(result, register_a) if result is not None else register_a

    print("Answer 2: ", result)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input", type=str, default="input.txt")

    input_file = arg_parser.parse_args().input

    with open(input_file, "r") as f:
        solve(f)
