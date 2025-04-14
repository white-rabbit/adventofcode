use std::collections::HashSet;
use std::env;
use std::fs::read_to_string;

#[derive(Hash, Eq, PartialEq)]
struct MatrixNumber {
    x: usize,
    y: usize,
    number: u32,
}

fn parse_input(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename)
        .unwrap_or_else(|_| panic!("File not found {filename}"))
        .lines()
    {
        result.push(line.to_string());
    }

    result
}

fn get_symbol(input: &[String], pos: (usize, usize)) -> char {
    input[pos.0]
        .chars()
        .nth(pos.1)
        .expect("Incorrect second index")
}

fn has_symbol_nearby(input: &[String], pos: (i32, i32)) -> bool {
    for i in -1..=1 {
        for j in -1..=1 {
            if i == 0 && j == 0 {
                continue;
            }
            let new_pos = (pos.0 + i, pos.1 + j);
            if new_pos.0 < 0 || new_pos.1 < 0 {
                continue;
            }
            if new_pos.0 >= input.len() as i32 || new_pos.1 >= input[0].len() as i32 {
                continue;
            }

            let symbol = input[new_pos.0 as usize]
                .chars()
                .nth(new_pos.1 as usize)
                .unwrap();

            if !symbol.is_ascii_digit() && symbol != '.' {
                return true;
            }
        }
    }

    false
}

fn part1(input: &[String]) -> u32 {
    let mut sum_part_number = 0;

    for (i, line) in input.iter().enumerate() {
        let mut cur_number = 0;
        let mut is_number = false;
        let mut is_part_number = false;

        for (j, c) in line.chars().enumerate() {
            if c.is_ascii_digit() {
                is_number = true;
                cur_number = cur_number * 10 + c.to_digit(10).unwrap();
                is_part_number |= has_symbol_nearby(input, (i as i32, j as i32));
            } else if is_number {
                if is_part_number {
                    log::debug!("Found part number: {}", cur_number);
                    sum_part_number += cur_number;
                }
                is_number = false;
                is_part_number = false;
                cur_number = 0;
            }
        }

        if is_number && is_part_number {
            log::debug!("Found part number: {}", cur_number);
            sum_part_number += cur_number;
        }
    }

    sum_part_number
}

fn find_number(input: &[String], pos: (usize, usize)) -> MatrixNumber {
    assert!(get_symbol(input, pos).is_ascii_digit());

    // find leftmost position of the number
    let mut left = pos;
    while left.1 > 0 && get_symbol(input, (left.0, left.1 - 1)).is_ascii_digit() {
        left.1 -= 1;
    }

    let line_len = input[left.0].len();

    let mut cur = left;
    let mut number = 0;

    while cur.1 < line_len && get_symbol(input, cur).is_ascii_digit() {
        number = number * 10 + get_symbol(input, cur).to_digit(10).unwrap();
        cur.1 += 1;
    }

    MatrixNumber {
        x: left.0,
        y: left.1,
        number,
    }
}

fn compute_gear_sum(input: &[String], pos: (usize, usize)) -> u32 {
    let mut gear_sum = 0;
    let mut numbers = HashSet::new();

    for i in -1..=1 {
        for j in -1..=1 {
            if i == 0 && j == 0 {
                continue;
            }
            let next_x = pos.0 as i32 + i;
            let next_y = pos.1 as i32 + j;

            if next_x < 0 || next_y < 0 {
                continue;
            }

            if next_x >= input.len() as i32 || next_y >= input[0].len() as i32 {
                continue;
            }

            let new_pos = (next_x as usize, next_y as usize);

            if get_symbol(input, new_pos).is_ascii_digit() {
                numbers.insert(find_number(input, new_pos));
            }
        }
    }

    log::info!("Gear numbers: {}", numbers.len());
    // if the count of contacted number is not 2
    // this gear should not be accounted
    if numbers.len() == 2 {
        let mut gear_ratio = 1;
        for number in numbers {
            gear_ratio *= number.number;
            log::info!("Gear numb: {}", number.number);
        }
        log::info!("Gear ratio: {}", gear_ratio);

        gear_sum += gear_ratio;
    }

    gear_sum
}

fn part2(input: &[String]) -> u32 {
    let mut gear_sum = 0;

    for (i, line) in input.iter().enumerate() {
        for (j, c) in line.chars().enumerate() {
            if c == '*' {
                gear_sum += compute_gear_sum(input, (i, j));
            }
        }
    }

    gear_sum
}

fn main() {
    env_logger::init();

    let args: Vec<String> = env::args().collect();
    let input_file_name = &args[1];
    let part = &args[2];

    let input = parse_input(input_file_name);

    match part.as_str() {
        "part1" => println!("{}", part1(&input)),
        "part2" => println!("{}", part2(&input)),
        _ => panic!("Invalid part"),
    }
}
