import pytest

import monte_carlo


# ==============================================================================
# Test 1: Reproducibility
# Purpose: Verify that simulations can be reproduced by setting the same seed.
# ==============================================================================

def test_seed_reproducibility_bernoulli():
    """Test reproducibility of Bernoulli trials.

    What we're testing: Setting the same seed should produce the same sequence
    of random Bernoulli outcomes.

    What we expect: Two sequences generated with the same seed should be
    identical.
    """
    monte_carlo.set_seed(42)
    seq1 = [monte_carlo.bernoulli(0.5) for _ in range(20)]

    monte_carlo.set_seed(42)
    seq2 = [monte_carlo.bernoulli(0.5) for _ in range(20)]

    assert seq1 == seq2


def test_seed_reproducibility_binomial():
    """Test reproducibility of Binomial samples.

    What we're testing: Setting the same seed produces identical Binomial
    random samples.

    What we expect: Two Binomial sample sequences generated with the same seed
    are identical.
    """
    monte_carlo.set_seed(7)
    samples1 = [monte_carlo.binomial(10, 0.3) for _ in range(15)]

    monte_carlo.set_seed(7)
    samples2 = [monte_carlo.binomial(10, 0.3) for _ in range(15)]

    assert samples1 == samples2


def test_seed_reproducibility_uniform():
    """Test reproducibility of Uniform samples.

    What we're testing: Setting the same seed produces identical Uniform
    random samples.

    What we expect: Two Uniform sample sequences generated with the same seed
    are identical.
    """
    monte_carlo.set_seed(123)
    samples1 = [monte_carlo.uniform(0, 100) for _ in range(10)]

    monte_carlo.set_seed(123)
    samples2 = [monte_carlo.uniform(0, 100) for _ in range(10)]

    assert samples1 == samples2


# ==============================================================================
# Test 2: Edge Cases
# Purpose: Verify correct behavior at boundary conditions (p=0, p=1, n=0).
# ==============================================================================

def test_bernoulli_probability_zero():
    """Test Bernoulli with zero probability.

    What we're testing: Bernoulli(p=0) should never succeed.

    What we expect: All 100 trials return False.
    """
    monte_carlo.set_seed(1)
    results = [monte_carlo.bernoulli(0.0) for _ in range(100)]
    assert all(result is False for result in results)


def test_bernoulli_probability_one():
    """Test Bernoulli with probability one.

    What we're testing: Bernoulli(p=1) should always succeed.

    What we expect: All 100 trials return True.
    """
    monte_carlo.set_seed(1)
    results = [monte_carlo.bernoulli(1.0) for _ in range(100)]
    assert all(result is True for result in results)


def test_binomial_zero_trials():
    """Test Binomial with zero trials.

    What we're testing: Binomial(n=0, p) should always return 0 successes.

    What we expect: All 50 samples return 0.
    """
    monte_carlo.set_seed(1)
    results = [monte_carlo.binomial(0, 0.5) for _ in range(50)]
    assert all(result == 0 for result in results)


def test_binomial_zero_probability():
    """Test Binomial with zero success probability.

    What we're testing: Binomial(n, p=0) should always return 0 successes.

    What we expect: All 50 samples return 0.
    """
    monte_carlo.set_seed(1)
    results = [monte_carlo.binomial(100, 0.0) for _ in range(50)]
    assert all(result == 0 for result in results)


def test_binomial_probability_one():
    """Test Binomial with probability one.

    What we're testing: Binomial(n, p=1) should always return n successes.

    What we expect: For n in [5, 10, 50, 100], binomial returns exactly n.
    """
    monte_carlo.set_seed(1)
    for n in [5, 10, 50, 100]:
        result = monte_carlo.binomial(n, 1.0)
        assert result == n


# ==============================================================================
# Test 3: Range and Bounds
# Purpose: Verify that outputs fall within expected ranges and have correct
# types.
# ==============================================================================

def test_bernoulli_returns_bool():
    """Test that Bernoulli returns a boolean type.

    What we're testing: Bernoulli(p) should return a bool for any valid p.

    What we expect: For p in [0.0, 0.25, 0.5, 0.75, 1.0], result is True or
    False (bool type).
    """
    monte_carlo.set_seed(1)
    for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
        result = monte_carlo.bernoulli(p)
        assert isinstance(result, bool)


def test_binomial_in_range():
    """Test that Binomial returns integers in valid range [0, n].

    What we're testing: Binomial(n, p) should return an integer in [0, n]
    for any valid n and p.

    What we expect: For various n and p, result is int type with 0 <= result
    <= n.
    """
    monte_carlo.set_seed(1)
    for n in [5, 10, 50]:
        for p in [0.1, 0.5, 0.9]:
            result = monte_carlo.binomial(n, p)
            assert isinstance(result, int)
            assert 0 <= result <= n


def test_uniform_in_range():
    """Test that Uniform returns floats in valid range [a, b].

    What we're testing: Uniform(a, b) should return a float in [a, b] for any
    valid a < b.

    What we expect: Over 100 samples with a=10, b=50, all results are float
    type with 10 <= result <= 50.
    """
    monte_carlo.set_seed(1)
    a, b = 10.0, 50.0
    for _ in range(100):
        result = monte_carlo.uniform(a, b)
        assert isinstance(result, float)
        assert a <= result <= b


# ==============================================================================
# Test 4: Input Validation and Error Handling
# Purpose: Verify that invalid inputs raise appropriate exceptions.
# ==============================================================================

def test_bernoulli_invalid_probability_negative():
    """Test that Bernoulli rejects negative probability.

    What we're testing: Bernoulli(p < 0) should raise ValueError.

    What we expect: ValueError is raised for p = -0.1.
    """
    with pytest.raises(ValueError):
        monte_carlo.bernoulli(-0.1)


def test_bernoulli_invalid_probability_above_one():
    """Test that Bernoulli rejects probability > 1.

    What we're testing: Bernoulli(p > 1) should raise ValueError.

    What we expect: ValueError is raised for p = 1.5.
    """
    with pytest.raises(ValueError):
        monte_carlo.bernoulli(1.5)


def test_binomial_invalid_trials_negative():
    """Test that Binomial rejects negative trial count.

    What we're testing: Binomial(n < 0, p) should raise ValueError.

    What we expect: ValueError is raised for n = -1.
    """
    with pytest.raises(ValueError):
        monte_carlo.binomial(-1, 0.5)


def test_binomial_invalid_probability_negative():
    """Test that Binomial rejects negative probability.

    What we're testing: Binomial(n, p < 0) should raise ValueError.

    What we expect: ValueError is raised for p = -0.1.
    """
    with pytest.raises(ValueError):
        monte_carlo.binomial(10, -0.1)


def test_binomial_invalid_probability_above_one():
    """Test that Binomial rejects probability > 1.

    What we're testing: Binomial(n, p > 1) should raise ValueError.

    What we expect: ValueError is raised for p = 1.5.
    """
    with pytest.raises(ValueError):
        monte_carlo.binomial(10, 1.5)


def test_uniform_invalid_bounds():
    """Test that Uniform rejects invalid bounds.

    What we're testing: Uniform(a, b) should raise ValueError if b <= a.

    What we expect: ValueError is raised for b = a and for b < a.
    """
    with pytest.raises(ValueError):
        monte_carlo.uniform(10.0, 10.0)
    with pytest.raises(ValueError):
        monte_carlo.uniform(50.0, 10.0)


def test_set_seed_invalid_type():
    """Test that set_seed rejects non-integer seeds.

    What we're testing: set_seed(seed) should raise TypeError if seed is not
    an integer.

    What we expect: TypeError is raised for float (3.14) and string ("42")
    seeds.
    """
    with pytest.raises(TypeError):
        monte_carlo.set_seed(3.14)
    with pytest.raises(TypeError):
        monte_carlo.set_seed("42")
