import pytest

from models.logistic import Logistic


def test_invalid_parameters():
    """Invalid constructor parameters should raise TypeError or ValueError."""
    # non-numeric lambda
    with pytest.raises(TypeError):
        Logistic("0.5", 0.1, 100, 10, 5)
    # non-numeric mu
    with pytest.raises(TypeError):
        Logistic(0.5, "0.1", 100, 10, 5)
    # non-numeric K
    with pytest.raises(TypeError):
        Logistic(0.5, 0.1, "100", 10, 5)
    # non-integer initial population
    with pytest.raises(TypeError):
        Logistic(0.5, 0.1, 100, 10.5, 5)
    # non-integer generations
    with pytest.raises(TypeError):
        Logistic(0.5, 0.1, 100, 10, "5")
    # lambda or mu out of range
    with pytest.raises(ValueError):
        Logistic(0.0, 0.1, 100, 10, 5)
    with pytest.raises(ValueError):
        Logistic(0.5, 0.0, 100, 10, 5)
    # K <= 0
    with pytest.raises(ValueError):
        Logistic(0.5, 0.1, 0, 10, 5)
    # initial population <= 0 or generations <= 0
    with pytest.raises(ValueError):
        Logistic(0.5, 0.1, 100, 0, 5)
    with pytest.raises(ValueError):
        Logistic(0.5, 0.1, 100, 10, 0)


def test_run_output_structure_and_types():
    """Run returns expected keys and types; all values are non-negative."""
    model = Logistic(
        lambda_birth=0.4,
        mu_death=0.1,
        carrying_capacity=100,
        initial_population=20,
        generations=5,
        seed=42,
    )
    results = model.run()

    assert "population_over_time" in results
    assert "births_per_generation" in results
    assert "deaths_per_generation" in results

    pop = results["population_over_time"]
    births = results["births_per_generation"]
    deaths = results["deaths_per_generation"]

    assert len(pop) == 6  # generations + 1
    assert len(births) == 5
    assert len(deaths) == 5

    assert all(isinstance(x, int) for x in pop)
    assert all(isinstance(x, int) for x in births)
    assert all(isinstance(x, int) for x in deaths)
    assert all(x >= 0 for x in pop)


def test_reproducibility_with_seed():
    """Two runs with identical seed should produce identical results."""
    m1 = Logistic(0.5, 0.1, 100, 50, 10, seed=999)
    r1 = m1.run()

    m2 = Logistic(0.5, 0.1, 100, 50, 10, seed=999)
    r2 = m2.run()

    assert r1 == r2


def test_population_non_negative():
    """Population should never go negative."""
    model = Logistic(
        lambda_birth=0.2,
        mu_death=0.8,
        carrying_capacity=50,
        initial_population=5,
        generations=15,
        seed=7,
    )
    results = model.run()

    pop = results["population_over_time"]
    assert all(p >= 0 for p in pop)


def test_birth_rate_decreases_with_population():
    """Birth probability should decrease as N approaches K."""
    model = Logistic(
        lambda_birth=0.4,
        mu_death=0.05,
        carrying_capacity=100,
        initial_population=10,
        generations=1,
        seed=None,
    )

    # Test the private _birth_probability method
    p_at_10 = model._birth_probability(10)
    p_at_50 = model._birth_probability(50)
    p_at_100 = model._birth_probability(100)
    p_at_150 = model._birth_probability(150)

    # p(10) > p(50) > p(100)=0 > p(150)=0
    assert p_at_10 > p_at_50
    assert p_at_50 > p_at_100
    assert p_at_100 == 0.0
    assert p_at_150 == 0.0


def test_birth_probability_at_carrying_capacity():
    """When N >= K, birth probability should be clamped to 0."""
    model = Logistic(
        lambda_birth=0.5,
        mu_death=0.1,
        carrying_capacity=100,
        initial_population=50,
        generations=1,
    )

    p_at_100 = model._birth_probability(100)
    p_at_200 = model._birth_probability(200)

    assert p_at_100 == 0.0
    assert p_at_200 == 0.0


def test_birth_probability_range():
    """Birth probability should always be in [0.0, 1.0]."""
    model = Logistic(
        lambda_birth=0.9,
        mu_death=0.1,
        carrying_capacity=50,
        initial_population=10,
        generations=1,
    )

    for pop in [0, 1, 10, 25, 50, 100, 200]:
        p = model._birth_probability(pop)
        assert 0.0 <= p <= 1.0
