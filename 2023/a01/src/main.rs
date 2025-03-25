use aho_corasick::AhoCorasick;
use std::collections::HashMap;
use std::env;
use std::fs::read_to_string;

struct Solver {
    engine: AhoCorasick,
    pattern_values: Vec<u32>,
}

impl Solver {
    pub fn new(patterns: &HashMap<String, u32>) -> Self {
        let mut patterns_list: Vec<String> = Vec::new();
        let mut pattern_values: Vec<u32> = Vec::new();

        for (pattern, value) in patterns {
            patterns_list.push(pattern.clone());
            pattern_values.push(*value);
        }

        Solver {
            engine: AhoCorasick::new(patterns_list).expect("Unable to create AH parser"),
            pattern_values,
        }
    }

    fn get_calibration_value(&self, s: &str) -> u32 {
        let mut first = 0;
        let mut last = 0;

        for (index, mat) in self.engine.find_overlapping_iter(s).enumerate() {
            if index == 0 {
                first = self.pattern_values[mat.pattern()];
                last = first;
            } else {
                last = self.pattern_values[mat.pattern()];
            }
        }

        first * 10 + last
    }

    fn compute_calibration_values_sum(&self, filename: &str) -> u32 {
        let mut result = 0;

        for line in read_to_string(filename)
            .unwrap_or_else(|_| panic!("File not found {filename}"))
            .lines()
        {
            result += self.get_calibration_value(line);
        }

        result
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let input_file_name = &args[1];
    let part = &args[2];

    assert!(part == "part1" || part == "part2");

    let mut digits_map = HashMap::from([
        ("0".to_string(), 0),
        ("1".to_string(), 1),
        ("2".to_string(), 2),
        ("3".to_string(), 3),
        ("4".to_string(), 4),
        ("5".to_string(), 5),
        ("6".to_string(), 6),
        ("7".to_string(), 7),
        ("8".to_string(), 8),
        ("9".to_string(), 9),
    ]);

    if part == "part2" {
        digits_map.extend(HashMap::from([
            ("one".to_string(), 1),
            ("two".to_string(), 2),
            ("three".to_string(), 3),
            ("four".to_string(), 4),
            ("five".to_string(), 5),
            ("six".to_string(), 6),
            ("seven".to_string(), 7),
            ("eight".to_string(), 8),
            ("nine".to_string(), 9),
        ]));
    }

    let solver = Solver::new(&digits_map);

    println!("{}", solver.compute_calibration_values_sum(input_file_name));
}
