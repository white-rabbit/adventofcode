use assert_cmd::Command;
use std::fs;

fn should_skip(path: &std::path::Path) -> bool {
    path.file_name()
        .unwrap()
        .to_str()
        .expect("Unable to convert path to string")
        .contains("skip")
}

#[test]
fn test_fixtures_are_correct() {
    let _ = env_logger::try_init();
    log::info!("Fixture tests");

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

    log::info!("Fixture tests finished.");
}

#[test]
fn test_part1() {
    let _ = env_logger::try_init();
    log::info!("Part 1 tests");

    let paths = fs::read_dir("./input/tests").unwrap();

    for path in paths {
        let path = path.unwrap().path();
        assert!(path.is_dir());

        if should_skip(&path) {
            log::warn!("Skipping test: {:?}", path);
            continue;
        }

        // input file must exist for any test case
        let input_file = path.join("input.txt");
        let output_file = path.join("output_part1.txt");

        if output_file.exists() {
            log::info!("Test: {:?}", path);
            assert!(output_file.is_file());

            let mut cmd = Command::cargo_bin("a03").unwrap();
            let assert = cmd.arg(input_file).arg("part1");

            let expected_output: String =
                fs::read_to_string(output_file).expect("Unable to find output file");
            assert.assert().success().stdout(expected_output);

            log::info!("Test {:?} succeeded!", path);
        }
    }

    log::info!("Part 1 tests finished.");
}

#[test]
fn test_part2() {
    let _ = env_logger::try_init();
    log::info!("Part 2 tests");

    let paths = fs::read_dir("./input/tests").unwrap();

    for path in paths {
        let path = path.unwrap().path();
        assert!(path.is_dir());

        if should_skip(&path) {
            log::warn!("Skipping test: {:?}", path);
            continue;
        }
        // input file must exist for any test case
        let input_file = path.join("input.txt");
        let output_file = path.join("output_part2.txt");

        if output_file.exists() {
            log::info!("Test: {:?}", path);

            let mut cmd = Command::cargo_bin("a03").unwrap();
            let assert = cmd.arg(input_file).arg("part2");

            let expected_output: String =
                fs::read_to_string(output_file).expect("Unable to find output file");

            assert.assert().success().stdout(expected_output);

            log::info!("Test {:?} succeeded!", path);
        }
    }

    log::info!("Part 2 tests finished.");
}
