"""Predator-Prey stochastic population model using Monte Carlo sampling.

Two interacting populations: prey and predators. Prey births are constant,
deaths increase with predator density. Predator births depend on prey
availability; deaths are constant.
"""
import monte_carlo
from utils import SimulationResult


class PredatorPrey:
    """Stochastic predator-prey population model.

    Attributes:
        lambda_prey (float): Prey birth rate per generation
        mu_prey (float): Base prey death rate per generation
        lambda_pred (float): Base predator birth rate per generation
        mu_pred (float): Predator death rate per generation
        predation_rate (float): Strength of predation effect on prey
        initial_prey (int): Starting prey population
        initial_predators (int): Starting predator population
        generations (int): Number of generations to simulate
        seed (int | None): RNG seed for reproducible results
    """

    def __init__(
        self,
        lambda_prey: float,
        mu_prey: float,
        lambda_pred: float,
        mu_pred: float,
        predation_rate: float,
        initial_prey: int,
        initial_predators: int,
        generations: int,
        seed: int = None,
    ) -> None:
        """Initialize the Predator-Prey model.

        Args:
            lambda_prey: Prey birth rate (0 < λ_prey <= 1)
            mu_prey: Base prey death rate (0 < μ_prey <= 1)
            lambda_pred: Predator birth rate (0 < λ_pred <= 1)
            mu_pred: Predator death rate (0 < μ_pred <= 1)
            predation_rate: Predation strength (>= 0)
            initial_prey: Initial prey population (> 0)
            initial_predators: Initial predator population (> 0)
            generations: Number of generations to simulate (> 0)
            seed: Optional RNG seed for reproducibility

        Raises:
            TypeError / ValueError for invalid parameters
        """
        self.lambda_prey = lambda_prey
        self.mu_prey = mu_prey
        self.lambda_pred = lambda_pred
        self.mu_pred = mu_pred
        self.predation_rate = predation_rate
        self.initial_prey = initial_prey
        self.initial_predators = initial_predators
        self.generations = generations
        self.seed = seed

        self._validate_parameters()

        if seed is not None:
            monte_carlo.set_seed(seed)

    def _validate_parameters(self) -> None:
        """Validate constructor parameters."""
        if not isinstance(self.lambda_prey, (int, float)):
            raise TypeError("lambda_prey must be a number")
        if not isinstance(self.mu_prey, (int, float)):
            raise TypeError("mu_prey must be a number")
        if not isinstance(self.lambda_pred, (int, float)):
            raise TypeError("lambda_pred must be a number")
        if not isinstance(self.mu_pred, (int, float)):
            raise TypeError("mu_pred must be a number")
        if not isinstance(self.predation_rate, (int, float)):
            raise TypeError("predation_rate must be a number")
        if not isinstance(self.initial_prey, int):
            raise TypeError("initial_prey must be an integer")
        if not isinstance(self.initial_predators, int):
            raise TypeError("initial_predators must be an integer")
        if not isinstance(self.generations, int):
            raise TypeError("generations must be an integer")

        if self.lambda_prey <= 0 or self.lambda_prey > 1:
            raise ValueError("lambda_prey must be in (0, 1]")
        if self.mu_prey <= 0 or self.mu_prey > 1:
            raise ValueError("mu_prey must be in (0, 1]")
        if self.lambda_pred <= 0 or self.lambda_pred > 1:
            raise ValueError("lambda_pred must be in (0, 1]")
        if self.mu_pred <= 0 or self.mu_pred > 1:
            raise ValueError("mu_pred must be in (0, 1]")
        if self.predation_rate < 0:
            raise ValueError("predation_rate must be >= 0")
        if self.initial_prey <= 0:
            raise ValueError("initial_prey must be > 0")
        if self.initial_predators <= 0:
            raise ValueError("initial_predators must be > 0")
        if self.generations <= 0:
            raise ValueError("generations must be > 0")

    def _prey_death_probability(self, predators: int) -> float:
        """Compute prey death probability given predator count.

        Formula: p_death = mu_prey * (1 + predation_rate * predators)
        Result is clamped to [0.0, 1.0].
        """
        p = self.mu_prey * (1.0 + self.predation_rate * predators)
        return min(1.0, max(0.0, p))

    def _predator_birth_probability(self, prey: int) -> float:
        """Compute predator birth probability given prey count.

        Formula: p_birth = lambda_pred * (prey / initial_prey)
        Result is clamped to [0.0, 1.0].
        """
        if self.initial_prey == 0:
            return 0.0
        p = self.lambda_pred * (float(prey) / float(self.initial_prey))
        return min(1.0, max(0.0, p))

    def run(self) -> SimulationResult:
        """Run the predator-prey simulation.

        Returns:
            SimulationResult with prey and predator population series and
            corresponding event series.
        """
        prey_population_over_time = [self.initial_prey]
        predator_population_over_time = [self.initial_predators]
        prey_births_per_generation = []
        prey_deaths_per_generation = []
        predator_births_per_generation = []
        predator_deaths_per_generation = []

        current_prey = self.initial_prey
        current_predators = self.initial_predators

        for _ in range(self.generations):
            p_prey_death = self._prey_death_probability(current_predators)
            prey_births = monte_carlo.binomial(current_prey, self.lambda_prey)
            prey_deaths = monte_carlo.binomial(current_prey, p_prey_death)

            p_pred_birth = self._predator_birth_probability(current_prey)
            predator_births = monte_carlo.binomial(
                current_predators, p_pred_birth
            )
            predator_deaths = monte_carlo.binomial(
                current_predators, self.mu_pred
            )

            prey_births_per_generation.append(prey_births)
            prey_deaths_per_generation.append(prey_deaths)
            predator_births_per_generation.append(predator_births)
            predator_deaths_per_generation.append(predator_deaths)

            current_prey = current_prey + prey_births - prey_deaths
            current_prey = max(current_prey, 0)

            current_predators = current_predators + predator_births
            current_predators = current_predators - predator_deaths
            current_predators = max(current_predators, 0)

            prey_population_over_time.append(current_prey)
            predator_population_over_time.append(current_predators)

        result = SimulationResult(
            model_name="predator_prey",
            populations={
                "prey": prey_population_over_time,
                "predators": predator_population_over_time,
            },
            events={
                "prey_births": prey_births_per_generation,
                "prey_deaths": prey_deaths_per_generation,
                "predator_births": predator_births_per_generation,
                "predator_deaths": predator_deaths_per_generation,
            },
            parameters={
                "lambda_prey": self.lambda_prey,
                "mu_prey": self.mu_prey,
                "lambda_pred": self.lambda_pred,
                "mu_pred": self.mu_pred,
                "predation_rate": self.predation_rate,
                "initial_prey": self.initial_prey,
                "initial_predators": self.initial_predators,
                "generations": self.generations,
            },
            seed=self.seed,
        )
        result.validate_lengths()

        return result
