"""Age-structured stochastic population model using Monte Carlo sampling.

Individuals are grouped by age classes. Each generation:
- deaths are sampled per age class
- births are sampled from survivors per age class
- survivors age into the next class
- the oldest class accumulates individuals that age beyond it
"""

import monte_carlo
from utils import SimulationResult


DEFAULT_AGE_GROUPS = ["young", "adult", "elder"]


class AgeStructured:
    """Stochastic age-structured population model.

    Attributes:
        age_groups: Names of age groups, ordered youngest to oldest.
        birth_rates: Birth probability per individual for each age group.
        death_rates: Death probability per individual for each age group.
        initial_age_distribution: Initial individuals per age group.
        generations: Number of generations to simulate.
        seed: Optional RNG seed for reproducibility.
    """

    def __init__(
        self,
        birth_rates: list[float],
        death_rates: list[float],
        initial_age_distribution: list[int],
        generations: int,
        age_groups: list[str] | None = None,
        seed: int = None,
    ) -> None:
        """Initialize the age-structured model.

        Args:
            age_groups: Ordered age-group names (youngest to oldest). If
                None, defaults to ["young", "adult", "elder"].
            birth_rates: Per-group birth probabilities in (0, 1].
            death_rates: Per-group death probabilities in (0, 1].
            initial_age_distribution: Initial population per age group.
            generations: Number of generations to simulate (> 0).
            seed: Optional RNG seed.

        Raises:
            TypeError: If parameter types are invalid.
            ValueError: If parameter values are invalid.
        """
        self.age_groups = (
            age_groups if age_groups is not None else DEFAULT_AGE_GROUPS.copy()
        )
        self.birth_rates = birth_rates
        self.death_rates = death_rates
        self.initial_age_distribution = initial_age_distribution
        self.generations = generations
        self.seed = seed

        self._validate_parameters()

        if seed is not None:
            monte_carlo.set_seed(seed)

    def _validate_parameters(self) -> None:
        """Validate constructor parameters."""
        if not isinstance(self.age_groups, list):
            raise TypeError("age_groups must be a list")
        if not isinstance(self.birth_rates, list):
            raise TypeError("birth_rates must be a list")
        if not isinstance(self.death_rates, list):
            raise TypeError("death_rates must be a list")
        if not isinstance(self.initial_age_distribution, list):
            raise TypeError("initial_age_distribution must be a list")
        if not isinstance(self.generations, int):
            raise TypeError("generations must be an integer")

        group_count = len(self.age_groups)
        if group_count == 0:
            raise ValueError("age_groups cannot be empty")

        if len(self.birth_rates) != group_count:
            raise ValueError("birth_rates length must match age_groups")
        if len(self.death_rates) != group_count:
            raise ValueError("death_rates length must match age_groups")
        if len(self.initial_age_distribution) != group_count:
            raise ValueError(
                "initial_age_distribution length must match age_groups"
            )

        if self.generations <= 0:
            raise ValueError("generations must be > 0")

        if any(not isinstance(name, str) or not name for name in self.age_groups):
            raise ValueError("all age group names must be non-empty strings")

        for p in self.birth_rates:
            if not isinstance(p, (int, float)):
                raise TypeError("birth_rates values must be numbers")
            if p <= 0 or p > 1:
                raise ValueError("birth_rates values must be in (0, 1]")

        for p in self.death_rates:
            if not isinstance(p, (int, float)):
                raise TypeError("death_rates values must be numbers")
            if p <= 0 or p > 1:
                raise ValueError("death_rates values must be in (0, 1]")

        for n in self.initial_age_distribution:
            if not isinstance(n, int):
                raise TypeError("initial_age_distribution values must be integers")
            if n < 0:
                raise ValueError(
                    "initial_age_distribution values must be >= 0"
                )

        if sum(self.initial_age_distribution) <= 0:
            raise ValueError("initial total population must be > 0")

    def run(self) -> SimulationResult:
        """Run the age-structured Monte Carlo simulation.

        Returns:
            SimulationResult with total and per-age-group population series,
            plus births and deaths event series.
        """
        current_distribution = self.initial_age_distribution.copy()

        total_population_over_time = [sum(current_distribution)]
        births_per_generation = []
        deaths_per_generation = []

        age_series: dict[str, list[int]] = {
            group: [count]
            for group, count in zip(self.age_groups, current_distribution)
        }

        for _ in range(self.generations):
            survivors = []
            deaths_this_generation = 0

            for count, death_rate in zip(current_distribution, self.death_rates):
                deaths = monte_carlo.binomial(count, death_rate)
                survivors_count = count - deaths
                survivors.append(survivors_count)
                deaths_this_generation += deaths

            births_this_generation = 0
            for survivors_count, birth_rate in zip(survivors, self.birth_rates):
                births_this_generation += monte_carlo.binomial(
                    survivors_count, birth_rate
                )

            next_distribution = [0] * len(self.age_groups)
            next_distribution[0] = births_this_generation

            for i in range(1, len(self.age_groups)):
                next_distribution[i] = survivors[i - 1]

            next_distribution[-1] += survivors[-1]

            current_distribution = next_distribution

            births_per_generation.append(births_this_generation)
            deaths_per_generation.append(deaths_this_generation)
            total_population_over_time.append(sum(current_distribution))

            for group, count in zip(self.age_groups, current_distribution):
                age_series[group].append(count)

        populations = {"population": total_population_over_time}
        populations.update(age_series)

        result = SimulationResult(
            model_name="age_structured",
            populations=populations,
            events={
                "births": births_per_generation,
                "deaths": deaths_per_generation,
            },
            parameters={
                "age_groups": self.age_groups,
                "birth_rates": self.birth_rates,
                "death_rates": self.death_rates,
                "initial_age_distribution": self.initial_age_distribution,
                "generations": self.generations,
            },
            seed=self.seed,
        )
        result.validate_lengths()

        return result
