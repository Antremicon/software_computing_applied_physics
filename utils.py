"""Shared utilities for stochastic population simulations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SimulationResult:
    """Container for simulation outputs.

    Attributes:
        model_name: Name of the simulated model.
        populations: Population series by key (for example: "population",
            "prey", "predators").
        events: Event count series by key (for example: "births", "deaths").
        parameters: Input parameters used for the simulation.
        seed: Random seed used for reproducibility, if provided.
    """

    model_name: str
    populations: dict[str, list[int]]
    events: dict[str, list[int]] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    seed: int | None = None

    def validate_lengths(self) -> None:
        """Validate output shape consistency.

        Raises:
            ValueError: If population series are empty or if event series do not
                have length generations - 1.
        """
        if not self.populations:
            raise ValueError("populations cannot be empty")

        lengths = {len(series) for series in self.populations.values()}
        if len(lengths) != 1:
            raise ValueError("all population series must have the same length")

        generations = next(iter(lengths))
        if generations == 0:
            raise ValueError("population series cannot be empty")

        expected_event_len = generations - 1
        for key, series in self.events.items():
            if len(series) != expected_event_len:
                raise ValueError(
                    f"event series '{key}' must have length "
                    f"{expected_event_len}"
                )

    def final_population(self, key: str = "population") -> int:
        """Return the final population value for a specific series key.

        Args:
            key: Population key to read.

        Returns:
            Final population value for the given key.

        Raises:
            KeyError: If key is not present in populations.
        """
        if key not in self.populations:
            raise KeyError(f"population key '{key}' not found")

        return self.populations[key][-1]

    @property
    def generation_count(self) -> int:
        """Return the number of simulated generations."""
        first_series = next(iter(self.populations.values()), [])
        return max(len(first_series) - 1, 0)

    def initial_population(self, key: str = "population") -> int:
        """Return the initial population value for a specific series key.

        Args:
            key: Population key to read.

        Returns:
            Initial population value for the given key.

        Raises:
            KeyError: If key is not present in populations.
        """
        if key not in self.populations:
            raise KeyError(f"population key '{key}' not found")

        return self.populations[key][0]

    def to_dict(self) -> dict[str, Any]:
        """Export result to a serializable dictionary."""
        return {
            "model_name": self.model_name,
            "populations": self.populations,
            "events": self.events,
            "parameters": self.parameters,
            "seed": self.seed,
            "generation_count": self.generation_count,
        }
