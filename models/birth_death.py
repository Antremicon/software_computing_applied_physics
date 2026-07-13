"""Simple Birth-Death population model using Monte Carlo simulation.

This module implements a basic stochastic population model where each
individual has a constant birth rate λ and death rate μ per generation.
"""
import monte_carlo


class SimpleBirthDeath:
    """Stochastic birth-death population model.

    Each generation:
    - Each individual has probability λ to reproduce (birth)
    - Each individual has probability μ to die
    - Births and deaths are sampled independently using Monte Carlo

    Attributes:
        lambda_birth (float): Birth rate per individual per generation
        mu_death (float): Death rate per individual per generation
        initial_population (int): Starting population size
        generations (int): Number of generations to simulate
        seed (int, optional): Random seed for reproducibility
    """

    def __init__(
        self,
        lambda_birth: float,
        mu_death: float,
        initial_population: int,
        generations: int,
        seed: int = None,
    ) -> None:
        """Initialize the Simple Birth-Death model.

        Args:
            lambda_birth: Birth rate (0 < λ <= 1)
            mu_death: Death rate (0 < μ <= 1)
            initial_population: Initial population size (> 0)
            generations: Number of generations to simulate (> 0)
            seed: Random seed for reproducibility (optional)

        Raises:
            ValueError: If any parameter is invalid
            TypeError: If types are incorrect
        """
        self.lambda_birth = lambda_birth
        self.mu_death = mu_death
        self.initial_population = initial_population
        self.generations = generations
        self.seed = seed

        self._validate_parameters()

        if seed is not None:
            monte_carlo.set_seed(seed)

    def _validate_parameters(self) -> None:
        """Validate input parameters.

        Raises:
            ValueError: If parameters are out of valid ranges
            TypeError: If parameter types are incorrect
        """
        if not isinstance(self.lambda_birth, (int, float)):
            raise TypeError("lambda_birth must be a number")
        if not isinstance(self.mu_death, (int, float)):
            raise TypeError("mu_death must be a number")
        if not isinstance(self.initial_population, int):
            raise TypeError("initial_population must be an integer")
        if not isinstance(self.generations, int):
            raise TypeError("generations must be an integer")

        if self.lambda_birth <= 0 or self.lambda_birth > 1:
            raise ValueError("lambda_birth must be in (0, 1]")
        if self.mu_death <= 0 or self.mu_death > 1:
            raise ValueError("mu_death must be in (0, 1]")
        if self.initial_population <= 0:
            raise ValueError("initial_population must be > 0")
        if self.generations <= 0:
            raise ValueError("generations must be > 0")

    def run(self) -> dict:
        """Run the birth-death simulation.

        Simulates the population over the specified number of generations.
        Each generation: sample births, sample deaths, update population.

        Returns:
            Dictionary with keys:
            - 'population_over_time': list of population sizes
            - 'births_per_generation': list of births per generation
            - 'deaths_per_generation': list of deaths per generation
        """
        population_over_time = [self.initial_population]
        births_per_generation = []
        deaths_per_generation = []

        current_population = self.initial_population

        for _ in range(self.generations):
            births = monte_carlo.binomial(current_population, self.lambda_birth)
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
