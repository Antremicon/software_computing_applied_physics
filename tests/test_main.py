import argparse
import sys
import pytest

import main as main_module
from utils import SimulationResult


def test_parse_float_list_valid_input():
    """Comma-separated floats should be parsed into a list of floats."""
    result = main_module.parse_float_list("0.2,0.5,0.1")

    assert result == [0.2, 0.5, 0.1]


def test_parse_float_list_valid_input_with_spaces():
    """Float lists should allow spaces around values."""
    result = main_module.parse_float_list("0.2, 0.5, 0.1")

    assert result == [0.2, 0.5, 0.1]


def test_parse_float_list_empty_string_raises_error():
    """An empty float list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_float_list("")


def test_parse_float_list_empty_value_raises_error():
    """An empty value inside a float list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_float_list("0.2,,0.1")


def test_parse_float_list_invalid_number_raises_error():
    """A non-numeric value inside a float list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_float_list("0.2,abc,0.1")


def test_parse_int_list_valid_input():
    """Comma-separated integers should be parsed into a list of integers."""
    result = main_module.parse_int_list("10,20,5")

    assert result == [10, 20, 5]


def test_parse_int_list_valid_input_with_spaces():
    """Integer lists should allow spaces around values."""
    result = main_module.parse_int_list("10, 20, 5")

    assert result == [10, 20, 5]


def test_parse_int_list_empty_string_raises_error():
    """An empty integer list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_int_list("")


def test_parse_int_list_empty_value_raises_error():
    """An empty value inside an integer list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_int_list("10,,5")


def test_parse_int_list_invalid_integer_raises_error():
    """A non-integer value inside an integer list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_int_list("10,2.5,5")


def test_parse_str_list_valid_input():
    """Comma-separated strings should be parsed into a list of strings."""
    result = main_module.parse_str_list("young,adult,elder")

    assert result == ["young", "adult", "elder"]


def test_parse_str_list_valid_input_with_spaces():
    """String lists should strip spaces around values."""
    result = main_module.parse_str_list("young, adult, elder")

    assert result == ["young", "adult", "elder"]


def test_parse_str_list_empty_string_raises_error():
    """An empty string list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_str_list("")


def test_parse_str_list_empty_value_raises_error():
    """An empty value inside a string list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_str_list("young,,elder")


def test_parse_str_list_blank_value_raises_error():
    """A blank value inside a string list should raise ValueError."""
    with pytest.raises(ValueError):
        main_module.parse_str_list("young, ,elder")


def test_ask_float_returns_valid_float(monkeypatch):
    """ask_float should return a valid float from user input."""
    monkeypatch.setattr("builtins.input", lambda _: "0.5")

    result = main_module.ask_float("Enter float: ")

    assert result == 0.5


def test_ask_float_retries_until_valid(monkeypatch):
    """ask_float should retry after invalid input."""
    inputs = iter(["abc", "0.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_float("Enter float: ")

    assert result == 0.5


def test_ask_int_returns_valid_integer(monkeypatch):
    """ask_int should return a valid integer from user input."""
    monkeypatch.setattr("builtins.input", lambda _: "10")

    result = main_module.ask_int("Enter integer: ")

    assert result == 10


def test_ask_int_retries_until_valid(monkeypatch):
    """ask_int should retry after invalid input."""
    inputs = iter(["abc", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_int("Enter integer: ")

    assert result == 10


def test_ask_probability_returns_valid_probability(monkeypatch):
    """ask_probability should return a value in the interval (0, 1]."""
    monkeypatch.setattr("builtins.input", lambda _: "0.4")

    result = main_module.ask_probability("Enter probability: ")

    assert result == 0.4


def test_ask_probability_rejects_zero(monkeypatch):
    """ask_probability should reject zero and retry."""
    inputs = iter(["0", "0.4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_probability("Enter probability: ")

    assert result == 0.4


def test_ask_probability_rejects_value_above_one(monkeypatch):
    """ask_probability should reject values greater than one and retry."""
    inputs = iter(["1.5", "0.4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_probability("Enter probability: ")

    assert result == 0.4


def test_ask_positive_int_returns_positive_integer(monkeypatch):
    """ask_positive_int should return an integer greater than zero."""
    monkeypatch.setattr("builtins.input", lambda _: "5")

    result = main_module.ask_positive_int("Enter positive integer: ")

    assert result == 5


def test_ask_positive_int_rejects_zero(monkeypatch):
    """ask_positive_int should reject zero and retry."""
    inputs = iter(["0", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_positive_int("Enter positive integer: ")

    assert result == 5


def test_ask_positive_int_rejects_negative_value(monkeypatch):
    """ask_positive_int should reject negative integers and retry."""
    inputs = iter(["-3", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_positive_int("Enter positive integer: ")

    assert result == 5


def test_ask_positive_float_returns_positive_float(monkeypatch):
    """ask_positive_float should return a value greater than zero."""
    monkeypatch.setattr("builtins.input", lambda _: "10.5")

    result = main_module.ask_positive_float("Enter positive float: ")

    assert result == 10.5


def test_ask_positive_float_rejects_zero(monkeypatch):
    """ask_positive_float should reject zero and retry."""
    inputs = iter(["0", "10.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_positive_float("Enter positive float: ")

    assert result == 10.5


def test_ask_positive_float_rejects_negative_value(monkeypatch):
    """ask_positive_float should reject negative values and retry."""
    inputs = iter(["-1.2", "10.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_positive_float("Enter positive float: ")

    assert result == 10.5


def test_ask_non_negative_float_returns_zero(monkeypatch):
    """ask_non_negative_float should accept zero."""
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = main_module.ask_non_negative_float("Enter non-negative float: ")

    assert result == 0.0


def test_ask_non_negative_float_returns_positive_value(monkeypatch):
    """ask_non_negative_float should accept positive values."""
    monkeypatch.setattr("builtins.input", lambda _: "2.5")

    result = main_module.ask_non_negative_float("Enter non-negative float: ")

    assert result == 2.5


def test_ask_non_negative_float_rejects_negative_value(monkeypatch):
    """ask_non_negative_float should reject negative values and retry."""
    inputs = iter(["-0.1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_non_negative_float("Enter non-negative float: ")

    assert result == 0.0


def test_ask_optional_int_returns_none_for_empty_input(monkeypatch):
    """ask_optional_int should return None when input is empty."""
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = main_module.ask_optional_int("Enter optional integer: ")

    assert result is None


def test_ask_optional_int_returns_integer(monkeypatch):
    """ask_optional_int should return an integer when input is valid."""
    monkeypatch.setattr("builtins.input", lambda _: "42")

    result = main_module.ask_optional_int("Enter optional integer: ")

    assert result == 42


def test_ask_optional_int_retries_until_valid(monkeypatch):
    """ask_optional_int should retry after invalid non-empty input."""
    inputs = iter(["abc", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_optional_int("Enter optional integer: ")

    assert result == 42


def test_ask_float_list_returns_valid_float_list(monkeypatch):
    """ask_float_list should return a valid list of floats."""
    monkeypatch.setattr("builtins.input", lambda _: "0.2,0.5,0.1")

    result = main_module.ask_float_list("Enter float list: ")

    assert result == [0.2, 0.5, 0.1]


def test_ask_float_list_retries_until_valid(monkeypatch):
    """ask_float_list should retry after invalid list input."""
    inputs = iter(["0.2,,0.1", "0.2,0.5,0.1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_float_list("Enter float list: ")

    assert result == [0.2, 0.5, 0.1]


def test_ask_int_list_returns_valid_int_list(monkeypatch):
    """ask_int_list should return a valid list of integers."""
    monkeypatch.setattr("builtins.input", lambda _: "10,20,5")

    result = main_module.ask_int_list("Enter integer list: ")

    assert result == [10, 20, 5]


def test_ask_int_list_retries_until_valid(monkeypatch):
    """ask_int_list should retry after invalid list input."""
    inputs = iter(["10,,5", "10,20,5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_int_list("Enter integer list: ")

    assert result == [10, 20, 5]


def test_ask_optional_str_list_returns_none_for_empty_input(monkeypatch):
    """ask_optional_str_list should return None when input is empty."""
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = main_module.ask_optional_str_list("Enter optional string list: ")

    assert result is None


def test_ask_optional_str_list_returns_valid_str_list(monkeypatch):
    """ask_optional_str_list should return a valid list of strings."""
    monkeypatch.setattr("builtins.input", lambda _: "young,adult,elder")

    result = main_module.ask_optional_str_list("Enter optional string list: ")

    assert result == ["young", "adult", "elder"]


def test_ask_optional_str_list_retries_until_valid(monkeypatch):
    """ask_optional_str_list should retry after invalid list input."""
    inputs = iter(["young,,elder", "young,adult,elder"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.ask_optional_str_list("Enter optional string list: ")

    assert result == ["young", "adult", "elder"]


def make_test_result() -> SimulationResult:
    """Create a small SimulationResult for main.py tests."""
    return SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12]},
        events={"births": [3], "deaths": [1]},
        parameters={"generations": 1},
        seed=42,
    )


def test_validate_matching_lengths_true():
    """validate_matching_lengths should return True for equal lengths."""
    result = main_module.validate_matching_lengths(
        [1, 2, 3],
        [4, 5, 6],
        ["a", "b", "c"],
    )

    assert result is True


def test_validate_matching_lengths_false():
    """validate_matching_lengths should return False for different lengths."""
    result = main_module.validate_matching_lengths(
        [1, 2, 3],
        [4, 5],
        ["a", "b", "c"],
    )

    assert result is False


def test_print_result_single_population(capsys):
    """print_result should print the final value of one population series."""
    result = SimulationResult(
        model_name="birth_death",
        populations={"population": [10, 12]},
        events={"births": [3], "deaths": [1]},
        parameters={"generations": 1},
        seed=42,
    )

    main_module.print_result(result)
    captured = capsys.readouterr()

    assert "Model: birth_death" in captured.out
    assert "Final populations:" in captured.out
    assert "population: 12" in captured.out


def test_print_result_multiple_populations(capsys):
    """print_result should print all final populations."""
    result = SimulationResult(
        model_name="predator_prey",
        populations={
            "prey": [50, 60],
            "predators": [10, 12],
        },
        events={
            "prey_births": [15],
            "prey_deaths": [5],
            "predator_births": [3],
            "predator_deaths": [1],
        },
        parameters={"generations": 1},
        seed=42,
    )

    main_module.print_result(result)
    captured = capsys.readouterr()

    assert "prey: 60" in captured.out
    assert "predators: 12" in captured.out


def test_run_birth_death_returns_simulation_result():
    """run_birth_death should return a SimulationResult."""
    args = argparse.Namespace(
        lambda_birth=0.4,
        mu_death=0.2,
        initial_population=10,
        generations=2,
        seed=42,
    )

    result = main_module.run_birth_death(args)

    assert isinstance(result, SimulationResult)
    assert result.model_name == "simple_birth_death"


def test_run_logistic_returns_simulation_result():
    """run_logistic should return a SimulationResult."""
    args = argparse.Namespace(
        lambda_birth=0.4,
        mu_death=0.1,
        carrying_capacity=100,
        initial_population=20,
        generations=2,
        seed=42,
    )

    result = main_module.run_logistic(args)

    assert isinstance(result, SimulationResult)
    assert result.model_name == "logistic"


def test_run_age_structured_returns_simulation_result():
    """run_age_structured should return a SimulationResult."""
    args = argparse.Namespace(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=2,
        age_groups=["young", "adult", "elder"],
        seed=42,
    )

    result = main_module.run_age_structured(args)

    assert isinstance(result, SimulationResult)
    assert result.model_name == "age_structured"


def test_run_predator_prey_returns_simulation_result():
    """run_predator_prey should return a SimulationResult."""
    args = argparse.Namespace(
        lambda_prey=0.4,
        mu_prey=0.1,
        lambda_pred=0.2,
        mu_pred=0.1,
        predation_rate=0.01,
        initial_prey=50,
        initial_predators=10,
        generations=2,
        seed=42,
    )

    result = main_module.run_predator_prey(args)

    assert isinstance(result, SimulationResult)
    assert result.model_name == "predator_prey"


def test_run_birth_death_interactive_returns_simulation_result(monkeypatch):
    """run_birth_death_interactive should return a SimulationResult."""
    inputs = iter(["0.4", "0.2", "10", "2", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.run_birth_death_interactive()

    assert isinstance(result, SimulationResult)
    assert result.model_name == "simple_birth_death"


def test_run_logistic_interactive_returns_simulation_result(monkeypatch):
    """run_logistic_interactive should return a SimulationResult."""
    inputs = iter(["0.4", "0.1", "100", "20", "2", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.run_logistic_interactive()

    assert isinstance(result, SimulationResult)
    assert result.model_name == "logistic"


def test_run_age_structured_interactive_returns_simulation_result(monkeypatch):
    """run_age_structured_interactive should return a SimulationResult."""
    inputs = iter(
        [
            "0.2,0.5,0.1",
            "0.1,0.05,0.2",
            "10,20,5",
            "2",
            "young,adult,elder",
            "42",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.run_age_structured_interactive()

    assert isinstance(result, SimulationResult)
    assert result.model_name == "age_structured"


def test_run_predator_prey_interactive_returns_simulation_result(monkeypatch):
    """run_predator_prey_interactive should return a SimulationResult."""
    inputs = iter(
        [
            "0.4",
            "0.1",
            "0.2",
            "0.1",
            "0.01",
            "50",
            "10",
            "2",
            "42",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = main_module.run_predator_prey_interactive()

    assert isinstance(result, SimulationResult)
    assert result.model_name == "predator_prey"


def test_add_common_seed_argument_parses_seed():
    """add_common_seed_argument should add a working seed argument."""
    parser = argparse.ArgumentParser()
    main_module.add_common_seed_argument(parser)

    args = parser.parse_args(["--seed", "42"])

    assert args.seed == 42


def test_add_common_seed_argument_defaults_to_none():
    """add_common_seed_argument should default seed to None."""
    parser = argparse.ArgumentParser()
    main_module.add_common_seed_argument(parser)

    args = parser.parse_args([])

    assert args.seed is None


def test_build_parser_birth_death_args():
    """build_parser should parse birth-death arguments."""
    parser = main_module.build_parser()

    args = parser.parse_args(
        [
            "birth_death",
            "--lambda-birth",
            "0.4",
            "--mu-death",
            "0.2",
            "--initial-population",
            "10",
            "--generations",
            "2",
            "--seed",
            "42",
        ]
    )

    assert args.model == "birth_death"
    assert args.lambda_birth == 0.4
    assert args.mu_death == 0.2
    assert args.initial_population == 10
    assert args.generations == 2
    assert args.seed == 42


def test_build_parser_logistic_args():
    """build_parser should parse logistic arguments."""
    parser = main_module.build_parser()

    args = parser.parse_args(
        [
            "logistic",
            "--lambda-birth",
            "0.4",
            "--mu-death",
            "0.1",
            "--carrying-capacity",
            "100",
            "--initial-population",
            "20",
            "--generations",
            "2",
            "--seed",
            "42",
        ]
    )

    assert args.model == "logistic"
    assert args.lambda_birth == 0.4
    assert args.mu_death == 0.1
    assert args.carrying_capacity == 100
    assert args.initial_population == 20
    assert args.generations == 2
    assert args.seed == 42


def test_build_parser_age_structured_args():
    """build_parser should parse age-structured arguments."""
    parser = main_module.build_parser()

    args = parser.parse_args(
        [
            "age_structured",
            "--birth-rates",
            "0.2,0.5,0.1",
            "--death-rates",
            "0.1,0.05,0.2",
            "--initial-age-distribution",
            "10,20,5",
            "--generations",
            "2",
            "--age-groups",
            "young,adult,elder",
            "--seed",
            "42",
        ]
    )

    assert args.model == "age_structured"
    assert args.birth_rates == [0.2, 0.5, 0.1]
    assert args.death_rates == [0.1, 0.05, 0.2]
    assert args.initial_age_distribution == [10, 20, 5]
    assert args.generations == 2
    assert args.age_groups == ["young", "adult", "elder"]
    assert args.seed == 42


def test_build_parser_predator_prey_args():
    """build_parser should parse predator-prey arguments."""
    parser = main_module.build_parser()

    args = parser.parse_args(
        [
            "predator_prey",
            "--lambda-prey",
            "0.4",
            "--mu-prey",
            "0.1",
            "--lambda-pred",
            "0.2",
            "--mu-pred",
            "0.1",
            "--predation-rate",
            "0.01",
            "--initial-prey",
            "50",
            "--initial-predators",
            "10",
            "--generations",
            "2",
            "--seed",
            "42",
        ]
    )

    assert args.model == "predator_prey"
    assert args.lambda_prey == 0.4
    assert args.mu_prey == 0.1
    assert args.lambda_pred == 0.2
    assert args.mu_pred == 0.1
    assert args.predation_rate == 0.01
    assert args.initial_prey == 50
    assert args.initial_predators == 10
    assert args.generations == 2
    assert args.seed == 42


def test_build_parser_invalid_model_raises_system_exit():
    """build_parser should reject unknown model names."""
    parser = main_module.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["unknown_model"])


def test_interactive_main_runs_birth_death_choice(monkeypatch):
    """interactive_main should run birth-death mode for choice 1."""
    called = {"birth_death": False}

    def fake_run_birth_death_interactive() -> SimulationResult:
        called["birth_death"] = True
        return make_test_result()

    monkeypatch.setattr("builtins.input", lambda _: "1")
    monkeypatch.setattr(
        main_module,
        "run_birth_death_interactive",
        fake_run_birth_death_interactive,
    )
    monkeypatch.setattr(main_module, "print_result", lambda _: None)

    main_module.interactive_main()

    assert called["birth_death"] is True


def test_interactive_main_runs_logistic_choice(monkeypatch):
    """interactive_main should run logistic mode for choice 2."""
    called = {"logistic": False}

    def fake_run_logistic_interactive() -> SimulationResult:
        called["logistic"] = True
        return make_test_result()

    monkeypatch.setattr("builtins.input", lambda _: "2")
    monkeypatch.setattr(
        main_module,
        "run_logistic_interactive",
        fake_run_logistic_interactive,
    )
    monkeypatch.setattr(main_module, "print_result", lambda _: None)

    main_module.interactive_main()

    assert called["logistic"] is True


def test_interactive_main_runs_age_structured_choice(monkeypatch):
    """interactive_main should run age-structured mode for choice 3."""
    called = {"age_structured": False}

    def fake_run_age_structured_interactive() -> SimulationResult:
        called["age_structured"] = True
        return make_test_result()

    monkeypatch.setattr("builtins.input", lambda _: "3")
    monkeypatch.setattr(
        main_module,
        "run_age_structured_interactive",
        fake_run_age_structured_interactive,
    )
    monkeypatch.setattr(main_module, "print_result", lambda _: None)

    main_module.interactive_main()

    assert called["age_structured"] is True


def test_interactive_main_runs_predator_prey_choice(monkeypatch):
    """interactive_main should run predator-prey mode for choice 4."""
    called = {"predator_prey": False}

    def fake_run_predator_prey_interactive() -> SimulationResult:
        called["predator_prey"] = True
        return make_test_result()

    monkeypatch.setattr("builtins.input", lambda _: "4")
    monkeypatch.setattr(
        main_module,
        "run_predator_prey_interactive",
        fake_run_predator_prey_interactive,
    )
    monkeypatch.setattr(main_module, "print_result", lambda _: None)

    main_module.interactive_main()

    assert called["predator_prey"] is True


def test_interactive_main_rejects_invalid_choice(monkeypatch, capsys):
    """interactive_main should print an error for invalid menu choices."""
    monkeypatch.setattr("builtins.input", lambda _: "9")

    main_module.interactive_main()
    captured = capsys.readouterr()

    assert "Invalid choice." in captured.out


def test_command_line_main_runs_valid_birth_death_command(monkeypatch, capsys):
    """command_line_main should run a valid birth-death command."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "birth_death",
            "--lambda-birth",
            "0.4",
            "--mu-death",
            "0.2",
            "--initial-population",
            "10",
            "--generations",
            "2",
            "--seed",
            "42",
        ],
    )

    main_module.command_line_main()
    captured = capsys.readouterr()

    assert "Model: simple_birth_death" in captured.out


def test_command_line_main_invalid_args_raise_system_exit(monkeypatch):
    """command_line_main should raise SystemExit for invalid arguments."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "birth_death",
            "--lambda-birth",
            "0.4",
        ],
    )

    with pytest.raises(SystemExit):
        main_module.command_line_main()
