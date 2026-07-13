"""Monte Carlo primitives for stochastic simulations.

This module provides core Monte Carlo utilities used by population models.
All random draws are reproducible via set_seed().
"""
import random


_rng = random.Random()


def set_seed(seed: int) -> None:
    """Set the RNG seed for reproducible simulations.

    Args:
        seed: Integer seed for the random number generator.

    Raises:
        TypeError: If seed is not an integer.
    """
    if not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    _rng.seed(seed)


def bernoulli(p: float) -> bool:
    """Perform a single Bernoulli trial.

    Args:
        p: Success probability (0.0 <= p <= 1.0).

    Returns:
        True if success, False otherwise.

    Raises:
        ValueError: If p is not in [0.0, 1.0].
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0.0, 1.0]")
    return _rng.random() < p


def binomial(n: int, p: float) -> int:
    """Sample from Binomial(n, p) distribution.

    Each of n independent Bernoulli trials is sampled; the result is the
    number of successes.

    Args:
        n: Number of trials (n >= 0).
        p: Success probability per trial (0.0 <= p <= 1.0).

    Returns:
        Number of successes (0 to n).

    Raises:
        ValueError: If n < 0 or p not in [0.0, 1.0].
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0.0, 1.0]")

    count = 0
    for _ in range(n):
        if bernoulli(p):
            count += 1
    return count


def uniform(a: float, b: float) -> float:
    """Sample from Uniform(a, b) distribution.

    Args:
        a: Lower bound.
        b: Upper bound (b > a).

    Returns:
        Random float in [a, b].

    Raises:
        ValueError: If b <= a.
    """
    if b <= a:
        raise ValueError("b must be greater than a")
    return _rng.uniform(a, b)
