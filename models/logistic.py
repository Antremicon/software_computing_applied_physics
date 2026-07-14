"""Logistic stochastic population model using Monte Carlo sampling.

Birth probability decreases linearly as population approaches carrying
capacity K. Discrete-time generations with Monte Carlo sampling of births
and deaths each generation.
"""
import monte_carlo


class Logistic:
    """Stochastic logistic population model.

    Attributes:
        lambda_birth (float): Base birth rate per individual per generation
        mu_death (float): Death rate per individual per generation
        carrying_capacity (int | float): Carrying capacity K (> 0)
        initial_population (int): Starting population size
        generations (int): Number of generations to simulate
        seed (int | None): RNG seed for reproducible results
    """

    def __init__(
        self,
        lambda_birth: float,
        mu_death: float,
        carrying_capacity: float,
        initial_population: int,
        generations: int,
        seed: int = None,
    ) -> None:
        """Initialize the Logistic model.

        Args:
            lambda_birth: Base birth rate (0 < λ <= 1)
            mu_death: Death rate (0 < μ <= 1)
            carrying_capacity: Positive carrying capacity K
            initial_population: Initial population size (> 0)
            generations: Number of generations to simulate (> 0)
            seed: Optional RNG seed for reproducibility

        Raises:
            TypeError / ValueError for invalid parameters
        """
        self.lambda_birth = lambda_birth
        self.mu_death = mu_death
        self.carrying_capacity = carrying_capacity
        self.initial_population = initial_population
        self.generations = generations
        self.seed = seed

        self._validate_parameters()

        if seed is not None:
            monte_carlo.set_seed(seed)

    def _validate_parameters(self) -> None:
        """Validate constructor parameters."""
        if not isinstance(self.lambda_birth, (int, float)):
            raise TypeError("lambda_birth must be a number")
        if not isinstance(self.mu_death, (int, float)):
            raise TypeError("mu_death must be a number")
        if not isinstance(self.carrying_capacity, (int, float)):
            raise TypeError("carrying_capacity must be a number")
        if not isinstance(self.initial_population, int):
            raise TypeError("initial_population must be an integer")
        if not isinstance(self.generations, int):
            raise TypeError("generations must be an integer")

        if self.lambda_birth <= 0 or self.lambda_birth > 1:
            raise ValueError("lambda_birth must be in (0, 1]")
        if self.mu_death <= 0 or self.mu_death > 1:
            raise ValueError("mu_death must be in (0, 1]")
        if self.carrying_capacity <= 0:
            raise ValueError("carrying_capacity must be > 0")
        if self.initial_population <= 0:
            raise ValueError("initial_population must be > 0")
        if self.generations <= 0:
            raise ValueError("generations must be > 0")

    def _birth_probability(self, population: int) -> float:
        """Compute per-individual birth probability for current population.

        Uses formula p_birth = lambda_birth * max(0, 1 - N / K).
        The result is clamped to [0.0, 1.0].
        """
        frac = 1.0 - (population / float(self.carrying_capacity))
        p = self.lambda_birth * max(0.0, frac)
        # clamp
        if p < 0.0:
            p = 0.0
        if p > 1.0:
            p = 1.0
        return p

    def run(self) -> dict:
        """Run the logistic simulation.

        Returns a dict with:
         - 'population_over_time': list of population sizes (len = generations + 1)
         - 'births_per_generation'
         - 'deaths_per_generation'
        """
        population_over_time = [self.initial_population]
        births_per_generation = []
        deaths_per_generation = []

        current_population = self.initial_population

        for _ in range(self.generations):
            p_birth = self._birth_probability(current_population)
            births = monte_carlo.binomial(current_population, p_birth)
            deaths = monte_carlo.binomial(current_population, self.mu_death)

            births_per_generation.append(births)
            deaths_per_generation.append(deaths)

            current_population = current_population + births - deaths
            current_population = max(current_population, 0)

            population_over_time.append(current_population)

        return {
            "population_over_time": population_over_time,
            "births_per_generation": births_per_generation,
            "deaths_per_generation": deaths_per_generation,
        }
