use std::collections::HashMap;
use std::env;
use std::fs::read_to_string;

struct Color {
    red: u32,
    green: u32,
    blue: u32,
}

impl Color {
    fn valid(&self, cap_color: &Color) -> bool {
        self.red <= cap_color.red && self.green <= cap_color.green && self.blue <= cap_color.blue
    }

    fn recap(&mut self, cap_color: &Color) {
        self.red = self.red.max(cap_color.red);
        self.green = self.green.max(cap_color.green);
        self.blue = self.blue.max(cap_color.blue);
    }

    fn power(&self) -> u32 {
        self.red * self.green * self.blue
    }
}

fn parse_input(filename: &str) -> HashMap<u32, Vec<Color>> {
    let mut result: HashMap<u32, Vec<Color>> = HashMap::new();
    for line in read_to_string(filename)
        .unwrap_or_else(|_| panic!("File not found {filename}"))
        .lines()
    {
        let (game, groups) = line.split_once(':').expect("Invalid input format");

        let (_, game_number) = game.split_once(' ').expect("Invalid input format");
        let game_number: u32 = game_number.parse().expect("Invalid game number");
        result.insert(game_number, Vec::new());
        let cur_set = result.get_mut(&game_number).unwrap();

        for color_set in groups.split(";") {
            let mut red = 0;
            let mut green = 0;
            let mut blue = 0;
            for color in color_set.split(",") {
                let (count, color) = color.trim().split_once(" ").expect("Invalid entry format");
                match color {
                    "red" => red = count.parse().expect("Invalid count"),
                    "green" => green = count.parse().expect("Invalid count"),
                    "blue" => blue = count.parse().expect("Invalid count"),
                    _ => panic!("Invalid color {color}"),
                }
            }

            cur_set.push(Color { red, green, blue });
        }
    }

    result
}

fn part1(input: HashMap<u32, Vec<Color>>) -> u32 {
    let mut count_valid = 0;
    let cap_color = Color {
        red: 12,
        green: 13,
        blue: 14,
    };
    for (game_number, color_set) in input {
        let mut valid = true;
        for color in color_set.iter() {
            if !color.valid(&cap_color) {
                valid = false;
                break;
            }
        }
        if valid {
            count_valid += game_number;
        }
    }
    count_valid
}

fn part2(input: HashMap<u32, Vec<Color>>) -> u32 {
    let mut total_power = 0;

    for (_, color_set) in input {
        let mut cap_color = Color {
            red: 0,
            green: 0,
            blue: 0,
        };
        for color in color_set.iter() {
            cap_color.recap(color);
        }

        total_power += cap_color.power();
    }
    total_power
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let input_file_name = &args[1];
    let part = &args[2];

    let input = parse_input(input_file_name);

    match part.as_str() {
        "part1" => println!("{}", part1(input)),
        "part2" => println!("{}", part2(input)),
        _ => panic!("Invalid part"),
    }
}
