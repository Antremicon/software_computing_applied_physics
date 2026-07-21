import pytest

from utils import SimulationResult


def test_validate_lengths_accepts_valid_result():
    """validate_lengths should accept consistent population and event lengths."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
        events={"births": [3, 4], "deaths": [1, 1]},
    )

    result.validate_lengths()


def test_validate_lengths_empty_populations_raises_error():
    """validate_lengths should reject empty populations dictionary."""
    result = SimulationResult(
        model_name="test_model",
        populations={},
    )

    with pytest.raises(ValueError):
        result.validate_lengths()


def test_validate_lengths_mismatched_population_lengths_raises_error():
    """validate_lengths should reject population series with different lengths."""
    result = SimulationResult(
        model_name="test_model",
        populations={
            "prey": [10, 12, 15],
            "predators": [5, 6],
        },
    )

    with pytest.raises(ValueError):
        result.validate_lengths()


def test_validate_lengths_empty_population_series_raises_error():
    """validate_lengths should reject empty population series."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": []},
    )

    with pytest.raises(ValueError):
        result.validate_lengths()


def test_validate_lengths_invalid_event_length_raises_error():
    """validate_lengths should reject event series with invalid length."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
        events={"births": [3]},
    )

    with pytest.raises(ValueError):
        result.validate_lengths()


def test_final_population_returns_last_value():
    """final_population should return the last value of a population series."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
    )

    assert result.final_population() == 15


def test_final_population_custom_key_returns_last_value():
    """final_population should support custom population keys."""
    result = SimulationResult(
        model_name="test_model",
        populations={
            "prey": [50, 60],
            "predators": [10, 12],
        },
    )

    assert result.final_population("prey") == 60
    assert result.final_population("predators") == 12


def test_final_population_invalid_key_raises_error():
    """final_population should raise KeyError for missing population keys."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
    )

    with pytest.raises(KeyError):
        result.final_population("missing")


def test_generation_count_returns_number_of_simulated_generations():
    """generation_count should return population series length minus one."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
    )

    assert result.generation_count == 2


def test_generation_count_returns_zero_for_empty_populations():
    """generation_count should return zero when no population series exists."""
    result = SimulationResult(
        model_name="test_model",
        populations={},
    )

    assert result.generation_count == 0


def test_initial_population_returns_first_value():
    """initial_population should return the first value of a population series."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
    )

    assert result.initial_population() == 10


def test_initial_population_custom_key_returns_first_value():
    """initial_population should support custom population keys."""
    result = SimulationResult(
        model_name="test_model",
        populations={
            "prey": [50, 60],
            "predators": [10, 12],
        },
    )

    assert result.initial_population("prey") == 50
    assert result.initial_population("predators") == 10


def test_initial_population_invalid_key_raises_error():
    """initial_population should raise KeyError for missing population keys."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
    )

    with pytest.raises(KeyError):
        result.initial_population("missing")


def test_to_dict_contains_expected_values():
    """to_dict should export the SimulationResult data."""
    result = SimulationResult(
        model_name="test_model",
        populations={"population": [10, 12, 15]},
        events={"births": [3, 4], "deaths": [1, 1]},
        parameters={"generations": 2},
        seed=42,
    )

    result_dict = result.to_dict()

    assert result_dict["model_name"] == "test_model"
    assert result_dict["populations"] == {"population": [10, 12, 15]}
    assert result_dict["events"] == {"births": [3, 4], "deaths": [1, 1]}
    assert result_dict["parameters"] == {"generations": 2}
    assert result_dict["seed"] == 42
    assert result_dict["generation_count"] == 2
