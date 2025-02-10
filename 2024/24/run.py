from collections import defaultdict, namedtuple


def has_loop(var, variables, expressions, used):
    var1, op, var2 = expressions[var]

    if var1 in used or var2 in used:
        return True

    if var1 not in variables:
        if has_loop(var1, variables, expressions, used | {var1}):
            return True

    if var2 not in variables:
        if has_loop(var2, variables, expressions, used | {var2}):
            return True

    return False


def calc(var, variables, expressions, exp_results):
    if var in exp_results:
        return exp_results[var]

    var1, op, var2 = expressions[var]

    var1val = variables.get(var1, None)
    if var1val is None:
        assert var1 in expressions, var1
        var1val = calc(var1, variables, expressions, exp_results)

    var2val = variables.get(var2, None)
    if var2val is None:
        assert var2 in expressions, var2
        var2val = calc(var2, variables, expressions, exp_results)

    result = None

    if op == "AND":
        result = var1val and var2val
    elif op == "OR":
        result = var1val or var2val
    else:
        assert op == "XOR"
        result = var1val ^ var2val

    exp_results[var] = result
    return result


def to_value(bitmap, prefix):
    bitnames = [x for x in bitmap if x.startswith(prefix)]
    bits = []

    for key in sorted(bitnames):
        bits.append("1" if bitmap[key] else "0")

    bit_str = "".join(bits[::-1])

    return int(bit_str, 2)


def check_sum_works(cur_z, prev_z, expressions, z_variables, show=False):
    if prev_z == "fake":
        return True

    if show:
        print("CHECKING", cur_z, prev_z)
    # set all variablesl to False
    variables = {}

    for var in z_variables:
        for v in ["x", "y"]:
            variables[v + var[1:]] = False

    cur_x = "x" + cur_z[1:]
    cur_y = "y" + cur_z[1:]
    prev_x = "x" + prev_z[1:]
    prev_y = "y" + prev_z[1:]

    for xv in [False, True]:
        for yv in [False, True]:
            for prev_xv, prev_yv in [(False, True), (True, True)]:
                variables.update(
                    {
                        cur_x: xv,
                        cur_y: yv,
                        prev_x: prev_xv,
                        prev_y: prev_yv,
                    }
                )

                res = calc(cur_z, variables, expressions, {})
                expected = (not (xv ^ yv)) if prev_xv and prev_yv else (xv ^ yv)

                if show:
                    print(xv, yv, prev_xv, prev_yv, "=>", res, "expected", expected)
                if expected != res:
                    return False

    return True


def calc_number(expressions, variables, prefix):
    bitmap = {}

    exp_results = {}

    for var in expressions:
        needed = isinstance(prefix, str) and var.startswith(prefix)
        if needed:
            value = calc(var, variables, expressions, exp_results)
            bitmap[var] = value

    return to_value(bitmap, prefix)


def swap_search(
    bit_index, expressions, variables, z_variables, fixed_variables, swapped_gates
):
    if bit_index == len(z_variables) - 1:
        return swapped_gates

    cur_z = z_variables[bit_index]

    # determine variables used to compute current z
    cur_variables = {}
    calc(cur_z, variables, expressions, cur_variables)

    prev_z = z_variables[bit_index - 1] if bit_index > 0 else "fake"

    if not check_sum_works(cur_z, prev_z, expressions, z_variables):
        tmp = expressions.copy()

        # try to swap the available variables
        swap1_candidates = sorted(set(cur_variables) - fixed_variables)
        swap2_candidates = sorted(set(expressions) - fixed_variables)

        for swp1 in swap1_candidates:
            for swp2 in swap2_candidates:
                # the swap!
                tmp[swp1], tmp[swp2] = tmp[swp2], tmp[swp1]

                # it is possible the swap introduces loop
                # then skip
                if has_loop(cur_z, variables, tmp, set()):
                    tmp[swp1], tmp[swp2] = tmp[swp2], tmp[swp1]
                    continue

                # if sum works with the current swap check if it
                # gives solution for all the variables
                if check_sum_works(cur_z, prev_z, tmp, z_variables):
                    solution = swap_search(
                        bit_index + 1,
                        tmp,
                        variables,
                        z_variables,
                        fixed_variables,
                        swapped_gates | {swp1, swp2},
                    )
                    if solution is not None:
                        return solution

                tmp[swp1], tmp[swp2] = tmp[swp2], tmp[swp1]

        # if the current bit cannot be fixed, return None
        return None
    else:
        return swap_search(
            bit_index + 1,
            expressions,
            variables,
            z_variables,
            fixed_variables | set(cur_variables),
            swapped_gates,
        )


def solve(f):
    variables = {}
    for l in f:
        if not l.strip():
            break
        var, rawval = l.split(":")
        variables[var] = bool(int(rawval.strip()))

    expressions = {}

    for l in f:
        expr, var = l.split("->")
        var = var.strip()
        expr = expr.strip()
        expr = expr.split()
        expressions[var] = expr

    initial_z = calc_number(expressions, variables, "z")

    print("Answer 1:", initial_z)

    z_vars = sorted([s for s in expressions if s.startswith("z")])

    gates_to_swap = swap_search(0, expressions, variables, z_vars, set(), set())

    sorted_gates = sorted(gates_to_swap)
    print("Answer 2", ",".join(sorted_gates))


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        solve(f)
