
import pytest

from models.age_structured import AgeStructured
from utils import SimulationResult


def test_invalid_parameters():
    """Invalid constructor parameters should raise TypeError or ValueError."""
    # non-list age_groups
    with pytest.raises(TypeError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations=5,
            age_groups="young,adult,elder",
        )
    # non-list birth_rates
    with pytest.raises(TypeError):
        AgeStructured(
            birth_rates="0.5,0.4,0.2",
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations=5,
        )
    # non-list death_rates
    with pytest.raises(TypeError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates="0.1,0.1,0.2",
            initial_age_distribution=[10, 5, 2],
            generations=5,
        )
    # non-list initial distribution
    with pytest.raises(TypeError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution="10,5,2",
            generations=5,
        )
    # non-integer generations
    with pytest.raises(TypeError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations="5",
        )
    # mismatched lengths
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 0.4],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations=5,
        )
    # invalid generations
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations=0,
        )
    # birth rate out of range
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 1.5, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, 5, 2],
            generations=5,
        )
    # death rate out of range
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.0],
            initial_age_distribution=[10, 5, 2],
            generations=5,
        )
    # negative population
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[10, -1, 2],
            generations=5,
        )
    # zero total population
    with pytest.raises(ValueError):
        AgeStructured(
            birth_rates=[0.5, 0.4, 0.2],
            death_rates=[0.1, 0.1, 0.2],
            initial_age_distribution=[0, 0, 0],
            generations=5,
        )


def test_run_output_structure_and_types():
    """Run returns SimulationResult with expected shape and types."""

    model = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=5,
        seed=42,
    )

    results = model.run()

    assert isinstance(results, SimulationResult)

    population = results.populations["population"]
    births = results.events["births"]
    deaths = results.events["deaths"]

    assert len(population) == 6
    assert len(births) == 5
    assert len(deaths) == 5

    assert all(isinstance(x, int) for x in population)
    assert all(isinstance(x, int) for x in births)
    assert all(isinstance(x, int) for x in deaths)

    assert all(x >= 0 for x in population)

    for group in model.age_groups:
        series = results.populations[group]

        assert len(series) == 6
        assert all(isinstance(x, int) for x in series)
        assert all(x >= 0 for x in series)



def test_reproducibility_with_seed():
    """Two runs with the same seed should produce identical results."""

    m1 = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=10,
        seed=42,
    )

    m2 = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=10,
        seed=42,
    )

    assert m1.run() == m2.run()


def test_population_non_negative():
    """Populations should never become negative."""

    model = AgeStructured(
        birth_rates=[0.01, 0.01, 0.01],
        death_rates=[1.0, 1.0, 1.0],
        initial_age_distribution=[5, 5, 5],
        generations=10,
        seed=42,
    )

    results = model.run()

    for series in results.populations.values():
        assert all(value >= 0 for value in series)


def test_population_equals_sum_of_age_groups():
    """Total population should equal the sum of age-group populations."""

    model = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=5,
        seed=42,
    )

    results = model.run()

    for i in range(model.generations + 1):
        total = sum(
            results.populations[group][i]
            for group in model.age_groups
        )

        assert total == results.populations["population"][i]


def test_default_age_groups_used():
    """Default age groups should be used when none are provided."""

    model = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=5,
    )

    assert model.age_groups == ["young", "adult", "elder"]


def test_age_group_series_lengths_match():
    """All age-group population series should have expected length."""

    model = AgeStructured(
        birth_rates=[0.2, 0.5, 0.1],
        death_rates=[0.1, 0.05, 0.2],
        initial_age_distribution=[10, 20, 5],
        generations=5,
        seed=42,
    )

    results = model.run()

    for group in model.age_groups:
        assert len(results.populations[group]) == model.generations + 1
