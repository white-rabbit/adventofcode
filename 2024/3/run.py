import argparse
import re


def solve(f):
    line = f.read()
    enabled = True
    match_str = "(mul\([0-9]{1,3},[0-9]{1,3}\))|(do\(\))|(don't\(\))"

    all_multiplications = 0
    enabled_multiplications = 0

    for match in re.findall(match_str, line):
        mul_exp, do_exp, dont_exp = match

        assert mul_exp or do_exp or dont_exp

        if do_exp:
            enabled = True
            assert not mul_exp and not dont_exp
        elif dont_exp:
            enabled = False
            assert not mul_exp and not do_exp
        else:
            assert not dont_exp and not do_exp

            strip_exp = ''.join(
                    s for s in mul_exp
                    if s.isdigit() or s == ',')

            x, y = (int(x) for x in strip_exp.split(','))
            cur_mul = x * y

            all_multiplications += cur_mul

            if enabled:
                enabled_multiplications += cur_mul

    print('All multiplications', all_multiplications)
    print('Enabled multiplications', enabled_multiplications)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')
    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
