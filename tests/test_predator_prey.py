import pytest

from models.predator_prey import PredatorPrey


def test_invalid_parameters():
    """Invalid constructor parameters should raise TypeError or ValueError."""
    # non-numeric rates
    with pytest.raises(TypeError):
        PredatorPrey("0.3", 0.1, 0.2, 0.1, 0.01, 50, 5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, "0.1", 0.2, 0.1, 0.01, 50, 5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, "0.2", 0.1, 0.01, 50, 5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, 0.2, "0.1", 0.01, 50, 5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, "0.01", 50, 5, 10)
    # non-integer populations or generations
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 50.5, 5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 50, 5.5, 10)
    with pytest.raises(TypeError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 50, 5, "10")
    # rates out of range
    with pytest.raises(ValueError):
        PredatorPrey(0.0, 0.1, 0.2, 0.1, 0.01, 50, 5, 10)
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.0, 0.2, 0.1, 0.01, 50, 5, 10)
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.0, 0.1, 0.01, 50, 5, 10)
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.2, 0.0, 0.01, 50, 5, 10)
    # negative predation rate
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, -0.01, 50, 5, 10)
    # invalid populations or generations
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 0, 5, 10)
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 50, 0, 10)
    with pytest.raises(ValueError):
        PredatorPrey(0.3, 0.1, 0.2, 0.1, 0.01, 50, 5, 0)


def test_run_output_structure_and_types():
    """Run returns expected keys and types for both species."""
    model = PredatorPrey(
        lambda_prey=0.4,
        mu_prey=0.1,
        lambda_pred=0.2,
        mu_pred=0.15,
        predation_rate=0.005,
        initial_prey=100,
        initial_predators=10,
        generations=5,
        seed=42,
    )
    results = model.run()

    # Check all expected keys
    expected_keys = {
        "prey_population_over_time",
        "predator_population_over_time",
        "prey_births_per_generation",
        "prey_deaths_per_generation",
        "predator_births_per_generation",
        "predator_deaths_per_generation",
    }
    assert set(results.keys()) == expected_keys

    # Check lengths
    prey_pop = results["prey_population_over_time"]
    pred_pop = results["predator_population_over_time"]
    prey_births = results["prey_births_per_generation"]
    prey_deaths = results["prey_deaths_per_generation"]
    pred_births = results["predator_births_per_generation"]
    pred_deaths = results["predator_deaths_per_generation"]

    assert len(prey_pop) == 6  # generations + 1
    assert len(pred_pop) == 6
    assert len(prey_births) == 5
    assert len(prey_deaths) == 5
    assert len(pred_births) == 5
    assert len(pred_deaths) == 5

    # Check types and non-negativity
    assert all(isinstance(x, int) for x in prey_pop)
    assert all(isinstance(x, int) for x in pred_pop)
    assert all(x >= 0 for x in prey_pop)
    assert all(x >= 0 for x in pred_pop)


def test_reproducibility_with_seed():
    """Two runs with identical seed should produce identical results."""
    m1 = PredatorPrey(0.3, 0.1, 0.2, 0.15, 0.004, 100, 10, 10, seed=777)
    r1 = m1.run()

    m2 = PredatorPrey(0.3, 0.1, 0.2, 0.15, 0.004, 100, 10, 10, seed=777)
    r2 = m2.run()

    assert r1 == r2


def test_populations_non_negative():
    """Both prey and predator populations should never go negative."""
    model = PredatorPrey(
        lambda_prey=0.2,
        mu_prey=0.5,
        lambda_pred=0.1,
        mu_pred=0.6,
        predation_rate=0.01,
        initial_prey=20,
        initial_predators=5,
        generations=20,
        seed=999,
    )
    results = model.run()

    prey_pop = results["prey_population_over_time"]
    pred_pop = results["predator_population_over_time"]

    assert all(p >= 0 for p in prey_pop)
    assert all(p >= 0 for p in pred_pop)


def test_prey_death_rate_increases_with_predators():
    """Prey death probability should increase as predator count rises."""
    model = PredatorPrey(
        lambda_prey=0.3,
        mu_prey=0.05,
        lambda_pred=0.1,
        mu_pred=0.1,
        predation_rate=0.01,
        initial_prey=100,
        initial_predators=10,
        generations=1,
    )

    p_no_pred = model._prey_death_probability(0)
    p_few_pred = model._prey_death_probability(5)
    p_many_pred = model._prey_death_probability(20)

    assert p_no_pred < p_few_pred < p_many_pred
    assert p_no_pred == 0.05  # mu_prey when predators=0


def test_prey_death_probability_clamped():
    """Prey death probability should never exceed 1.0."""
    model = PredatorPrey(
        lambda_prey=0.3,
        mu_prey=0.5,
        lambda_pred=0.1,
        mu_pred=0.1,
        predation_rate=0.1,  # high predation rate
        initial_prey=100,
        initial_predators=10,
        generations=1,
    )

    for pred_count in [0, 5, 10, 50, 100]:
        p = model._prey_death_probability(pred_count)
        assert 0.0 <= p <= 1.0


def test_predator_birth_rate_increases_with_prey():
    """Predator birth probability should increase with prey availability."""
    model = PredatorPrey(
        lambda_prey=0.3,
        mu_prey=0.1,
        lambda_pred=0.2,
        mu_pred=0.1,
        predation_rate=0.005,
        initial_prey=100,
        initial_predators=10,
        generations=1,
    )

    p_no_prey = model._predator_birth_probability(0)
    p_few_prey = model._predator_birth_probability(50)
    p_many_prey = model._predator_birth_probability(100)
    p_excess_prey = model._predator_birth_probability(200)

    assert p_no_prey == 0.0
    assert p_few_prey < p_many_prey
    assert p_excess_prey <= 1.0


def test_predator_birth_probability_range():
    """Predator birth probability should always be in [0.0, 1.0]."""
    model = PredatorPrey(
        lambda_prey=0.3,
        mu_prey=0.1,
        lambda_pred=0.5,
        mu_pred=0.1,
        predation_rate=0.005,
        initial_prey=100,
        initial_predators=10,
        generations=1,
    )

    for prey_count in [0, 10, 50, 100, 200, 500]:
        p = model._predator_birth_probability(prey_count)
        assert 0.0 <= p <= 1.0
