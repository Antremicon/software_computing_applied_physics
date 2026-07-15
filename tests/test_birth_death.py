import pytest

from models.birth_death import SimpleBirthDeath
from utils import SimulationResult


def test_invalid_parameters():
    """Invalid constructor parameters should raise TypeError or ValueError."""
    # non-numeric lambda
    with pytest.raises(TypeError):
        SimpleBirthDeath("0.5", 0.1, 10, 5)
    # non-numeric mu
    with pytest.raises(TypeError):
        SimpleBirthDeath(0.5, "0.1", 10, 5)
    # non-integer initial population
    with pytest.raises(TypeError):
        SimpleBirthDeath(0.5, 0.1, 10.5, 5)
    # non-integer generations
    with pytest.raises(TypeError):
        SimpleBirthDeath(0.5, 0.1, 10, "5")
    # lambda or mu out of allowed range (<= 0)
    with pytest.raises(ValueError):
        SimpleBirthDeath(0.0, 0.1, 10, 5)
    with pytest.raises(ValueError):
        SimpleBirthDeath(0.5, 0.0, 10, 5)
    # invalid initial population or generations
    with pytest.raises(ValueError):
        SimpleBirthDeath(0.5, 0.1, 0, 5)
    with pytest.raises(ValueError):
        SimpleBirthDeath(0.5, 0.1, 10, 0)


def test_run_output_structure_and_types():
    """Run returns SimulationResult with expected shape and types."""
    model = SimpleBirthDeath(
        lambda_birth=0.4,
        mu_death=0.2,
        initial_population=10,
        generations=5,
        seed=42,
    )
    results = model.run()

    assert isinstance(results, SimulationResult)

    pop = results.populations["population"]
    births = results.events["births"]
    deaths = results.events["deaths"]

    assert len(pop) == 6  # generations + 1
    assert len(births) == 5
    assert len(deaths) == 5

    assert all(isinstance(x, int) for x in pop)
    assert all(isinstance(x, int) for x in births)
    assert all(isinstance(x, int) for x in deaths)

    assert all(x >= 0 for x in pop)


def test_reproducibility_with_seed():
    """Two runs with the same seed should produce identical results."""
    m1 = SimpleBirthDeath(0.3, 0.1, 20, 10, seed=123)
    r1 = m1.run()

    m2 = SimpleBirthDeath(0.3, 0.1, 20, 10, seed=123)
    r2 = m2.run()

    assert r1 == r2


def test_population_non_negative_and_clamping():
    """Population should never go negative; excessive deaths are clamped."""
    # Use high death rate so extinction is likely
    model = SimpleBirthDeath(lambda_birth=1e-6, mu_death=1.0, initial_population=5, generations=10, seed=7)
    results = model.run()

    pop = results.populations["population"]
    deaths = results.events["deaths"]

    assert all(p >= 0 for p in pop)
    # deaths cannot exceed population at that generation (births may increase it)
    # check per-generation constraint: deaths sampled <= population at start of that generation
    current = 5
    for d in deaths:
        assert 0 <= d <= current
        current = max(current + 0 - d, 0)
