use assert_cmd::Command;
use std::fs;

#[test]
fn test_fixtures_are_correct() {
    let paths = fs::read_dir("./input/tests").unwrap();

    for path in paths {
        let path = path.unwrap().path();
        assert!(path.is_dir());

        // input file must exist for any test case
        let input_file = path.join("input.txt");
        assert!(input_file.exists());
        assert!(input_file.is_file());

        // output should exist at least for one of the parts
        let output_part1 = path.join("output_part1.txt");
        if output_part1.exists() {
            assert!(output_part1.is_file());
        }
        let output_part2 = path.join("output_part2.txt");
        if output_part2.exists() {
            assert!(output_part2.is_file());
        }
    }
}

#[test]
fn test_part1() {
    let mut cmd = Command::cargo_bin("a02").unwrap();
    let paths = fs::read_dir("./input/tests").unwrap();

    for path in paths {
        let path = path.unwrap().path();
        assert!(path.is_dir());

        // input file must exist for any test case
        let input_file = path.join("input.txt");
        let output_file = path.join("output_part1.txt");

        if output_file.exists() {
            println!("Test: {:?}", path);
            assert!(output_file.is_file());

            let assert = cmd.arg(input_file).arg("part1");

            let expected_output: String =
                fs::read_to_string(output_file).expect("Unable to find output file");
            assert.assert().success().stdout(expected_output);

            println!("Success!");
        }
    }
}

#[test]
fn test_part2() {
    let mut cmd = Command::cargo_bin("a02").unwrap();
    let paths = fs::read_dir("./input/tests").unwrap();

    for path in paths {
        let path = path.unwrap().path();
        assert!(path.is_dir());

        // input file must exist for any test case
        let input_file = path.join("input.txt");
        let output_file = path.join("output_part2.txt");

        if output_file.exists() {
            println!("Test: {:?}", path);

            let assert = cmd.arg(input_file).arg("part2");

            let expected_output: String =
                fs::read_to_string(output_file).expect("Unable to find output file");

            println!("Expected output: {}", expected_output);
            assert.assert().success().stdout(expected_output);

            println!("Success!");
        }
    }
}
