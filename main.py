"""Command-line interface for stochastic population simulations."""

import argparse
import sys

from models.age_structured import AgeStructured
from models.birth_death import SimpleBirthDeath
from models.logistic import Logistic
from models.predator_prey import PredatorPrey
from utils import SimulationResult


def parse_float_list(value: str) -> list[float]:
    """Parse a comma-separated string into a list of floats.

    Args:
        value: Comma-separated numeric values.

    Returns:
        List    Raises:
        ValueError: If the list is empty or a value cannot be converted.
    """
    items = [item.strip() for item in value.split(",")]

    if not items or any(item == "" for item in items):
        raise ValueError("list values cannot be empty")

    return [float(item) for item in items]
 

def parse_int_list(value: str) -> list[int]:
    """Parse a comma-separated string into a list of integers.

    Args:
        value: Comma-separated integer values.

    Returns:
        List of integers.

    Raises:
        ValueError: If the list is empty or a value cannot be converted.
    """
    items = [item.strip() for item in value.split(",")]

    if not items or any(item == "" for item in items):
        raise ValueError("list values cannot be empty")

    return [int(item) for item in items]


def parse_str_list(value: str) -> list[str]:
    """Parse a comma-separated string into a list of strings.

    Args:
        value: Comma-separated text values.

    Returns:
        List of stripped strings.

    Raises:
        ValueError: If one of the values is empty.
    """
    items = [item.strip() for item in value.split(",")]

    if not items or any(item == "" for item in items):
        raise ValueError("list values cannot be empty")

    return items


def ask_float(prompt: str) -> float:
    """Ask the user for a floating-point value.

    Args:
        prompt: Message shown to the user.

    Returns:
        User-provided float.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def ask_int(prompt: str) -> int:
    """Ask the user for an integer value.

    Args:
        prompt: Message shown to the user.

    Returns:
        User-provided integer.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def ask_probability(prompt: str) -> float:
    """Ask the user for a probability in the interval (0, 1].

    Args:
        prompt: Message shown to the user.

    Returns:
        Valid probability value.
    """
    while True:
        value = ask_float(prompt)

        if 0 < value <= 1:
            return value

        print("Please enter a value greater than 0 and less than or equal to 1.")


def ask_positive_int(prompt: str) -> int:
    """Ask the user for a positive integer.

    Args:
        prompt: Message shown to the user.

    Returns:
        Positive integer.
    """
    while True:
        value = ask_int(prompt)

        if value > 0:
            return value

        print("Please enter an integer greater than 0.")


def ask_positive_float(prompt: str) -> float:
    """Ask the user for a positive float.

    Args:
        prompt: Message shown to the user.

    Returns:
        Positive float.
    """
    while True:
        value = ask_float(prompt)

        if value > 0:
            return value

        print("Please enter a value greater than 0.")


def ask_non_negative_float(prompt: str) -> float:
    """Ask the user for a non-negative float.

    Args:
        prompt: Message shown to the user.

    Returns:
        Non-negative float.
    """
    while True:
        value = ask_float(prompt)

        if value >= 0:
            return value

        print("Please enter a value greater than or equal to 0.")


def ask_optional_int(prompt: str) -> int | None:
    """Ask the user for an optional integer value.

    Args:
        prompt: Message shown to the user.

    Returns:
        Integer value, or None if the user leaves the input empty.
    """
    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer, or leave empty.")


def ask_float_list(prompt: str) -> list[float]:
    """Ask the user for a comma-separated list of floats.

    Args:
        prompt: Message shown to the user.

    Returns:
        List of floats.
    """
    while True:
        try:
            return parse_float_list(input(prompt))
        except ValueError:
            print("Please enter comma-separated numbers.")
            print("Example: 0.2,0.5,0.1")


def ask_int_list(prompt: str) -> list[int]:
    """Ask the user for a comma-separated list of integers.

    Args:
        prompt: Message shown to the user.

    Returns:
        List of integers.
    """
    while True:
        try:
            return parse_int_list(input(prompt))
        except ValueError:
            print("Please enter comma-separated integers.")
            print("Example: 10,20,5")


def ask_optional_str_list(prompt: str) -> list[str] | None:
    """Ask the user for an optional comma-separated list of strings.

    Args:
        prompt: Message shown to the user.

    Returns:
        List of strings, or None if the user leaves the input empty.
    """
    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        try:
            return parse_str_list(value)
        except ValueError:
            print("Please enter comma-separated names without empty values.")
            print("Example: young,adult,elder")


def validate_matching_lengths(*lists) -> bool:
    """Check whether all provided lists have the same length.

    Args:
        *lists: Lists to compare.

    Returns:
        True if all lists have the same length, False otherwise.
    """
    lengths = {len(values) for values in lists}

    return len(lengths) == 1


def print_result(result: SimulationResult) -> None:
    """Print simulation results in a readable format.

    Args:
        result: SimulationResult returned by a population model.
    """
    print()
    print(f"Model: {result.model_name}")
    print(f"Generations: {result.generation_count}")
    print(f"Seed: {result.seed}")

    print()
    print("Final populations:")
    for key, values in result.populations.items():
        print(f"  {key}: {values[-1]}")

    print()
    print("Parameters:")
    for key, value in result.parameters.items():
        print(f"  {key}: {value}")

    print()
    print("Populations over time:")
    for key, values in result.populations.items():
        print(f"  {key}: {values}")

    if result.events:
        print()
        print("Events:")
        for key, values in result.events.items():
            print(f"  {key}: {values}")


def run_birth_death(args) -> SimulationResult:
    """Run the simple birth-death model.

    Args:
        args: Parsed command-line arguments.

    Returns:
        SimulationResult produced by the model.
    """
    model = SimpleBirthDeath(
        lambda_birth=args.lambda_birth,
        mu_death=args.mu_death,
        initial_population=args.initial_population,
        generations=args.generations,
        seed=args.seed,
    )

    return model.run()


def run_logistic(args) -> SimulationResult:
    """Run the logistic population model.

    Args:
        args: Parsed command-line arguments.

    Returns:
        SimulationResult produced by the model.
    """
    model = Logistic(
        lambda_birth=args.lambda_birth,
        mu_death=args.mu_death,
        carrying_capacity=args.carrying_capacity,
        initial_population=args.initial_population,
        generations=args.generations,
        seed=args.seed,
    )

    return model.run()


def run_age_structured(args) -> SimulationResult:
    """Run the age-structured population model.

    Args:
        args: Parsed command-line arguments.

    Returns:
        SimulationResult produced by the model.
    """
    model = AgeStructured(
        birth_rates=args.birth_rates,
        death_rates=args.death_rates,
        initial_age_distribution=args.initial_age_distribution,
        generations=args.generations,
        age_groups=args.age_groups,
        seed=args.seed,
    )

    return model.run()


def run_predator_prey(args) -> SimulationResult:
    """Run the predator-prey population model.

    Args:
        args: Parsed command-line arguments.

    Returns:
        SimulationResult produced by the model.
    """
    model = PredatorPrey(
        lambda_prey=args.lambda_prey,
        mu_prey=args.mu_prey,
        lambda_pred=args.lambda_pred,
        mu_pred=args.mu_pred,
        predation_rate=args.predation_rate,
        initial_prey=args.initial_prey,
        initial_predators=args.initial_predators,
        generations=args.generations,
        seed=args.seed,
    )

    return model.run()


def run_birth_death_interactive() -> SimulationResult:
    """Ask for birth-death parameters and run the model.

    Returns:
        SimulationResult produced by the model.
    """
    lambda_birth = ask_probability("Birth rate lambda, in (0, 1]: ")
    mu_death = ask_probability("Death rate mu, in (0, 1]: ")
    initial_population = ask_positive_int("Initial population, > 0: ")
    generations = ask_positive_int("Generations, > 0: ")
    seed = ask_optional_int("Seed, optional: ")

    model = SimpleBirthDeath(
        lambda_birth=lambda_birth,
        mu_death=mu_death,
        initial_population=initial_population,
        generations=generations,
        seed=seed,
    )

    return model.run()


def run_logistic_interactive() -> SimulationResult:
    """Ask for logistic model parameters and run the model.

    Returns:
        SimulationResult produced by the model.
    """
    lambda_birth = ask_probability("Base birth rate lambda, in (0, 1]: ")
    mu_death = ask_probability("Death rate mu, in (0, 1]: ")
    carrying_capacity = ask_positive_float("Carrying capacity K, > 0: ")
    initial_population = ask_positive_int("Initial population, > 0: ")
    generations = ask_positive_int("Generations, > 0: ")
    seed = ask_optional_int("Seed, optional: ")

    model = Logistic(
        lambda_birth=lambda_birth,
        mu_death=mu_death,
        carrying_capacity=carrying_capacity,
        initial_population=initial_population,
        generations=generations,
        seed=seed,
    )

    return model.run()


def run_age_structured_interactive() -> SimulationResult:
    """Ask for age-structured model parameters and run the model.

    Returns:
        SimulationResult produced by the model.
    """
    while True:
        birth_rates = ask_float_list(
            "Birth rates by age group, example 0.2,0.5,0.1: "
        )
        death_rates = ask_float_list(
            "Death rates by age group, example 0.1,0.05,0.2: "
        )
        initial_age_distribution = ask_int_list(
            "Initial age distribution, example 10,20,5: "
        )

        if not validate_matching_lengths(
            birth_rates,
            death_rates,
            initial_age_distribution,
        ):
            print("The three lists must have the same length.")
            print("Example:")
            print("  birth rates: 0.2,0.5,0.1")
            print("  death rates: 0.1,0.05,0.2")
            print("  initial distribution: 10,20,5")
            continue

        if any(rate <= 0 or rate > 1 for rate in birth_rates):
            print("All birth rates must be in (0, 1].")
            continue

        if any(rate <= 0 or rate > 1 for rate in death_rates):
            print("All death rates must be in (0, 1].")
            continue

        if any(count < 0 for count in initial_age_distribution):
            print("Initial age distribution values must be >= 0.")
            continue

        if sum(initial_age_distribution) <= 0:
            print("Initial total population must be greater than 0.")
            continue

        break

    generations = ask_positive_int("Generations, > 0: ")
    age_groups = ask_optional_str_list(
        "Age group names, optional, example young,adult,elder: "
    )

    if age_groups is not None and len(age_groups) != len(birth_rates):
        print("Age group names must match the number of rate values.")
        print("The default age group names will be used instead.")
        age_groups = None

    seed = ask_optional_int("Seed, optional: ")

    model = AgeStructured(
        birth_rates=birth_rates,
        death_rates=death_rates,
        initial_age_distribution=initial_age_distribution,
        generations=generations,
        age_groups=age_groups,
        seed=seed,
    )

    return model.run()


def run_predator_prey_interactive() -> SimulationResult:
    """Ask for predator-prey parameters and run the model.

    Returns:
        SimulationResult produced by the model.
    """
    lambda_prey = ask_probability("Prey birth rate lambda_prey, in (0, 1]: ")
    mu_prey = ask_probability("Prey base death rate mu_prey, in (0, 1]: ")
    lambda_pred = ask_probability("Predator birth rate lambda_pred, in (0, 1]: ")
    mu_pred = ask_probability("Predator death rate mu_pred, in (0, 1]: ")
    predation_rate = ask_non_negative_float("Predation rate, >= 0: ")
    initial_prey = ask_positive_int("Initial prey population, > 0: ")
    initial_predators = ask_positive_int("Initial predator population, > 0: ")
    generations = ask_positive_int("Generations, > 0: ")
    seed = ask_optional_int("Seed, optional: ")

    model = PredatorPrey(
        lambda_prey=lambda_prey,
        mu_prey=mu_prey,
        lambda_pred=lambda_pred,
        mu_pred=mu_pred,
        predation_rate=predation_rate,
        initial_prey=initial_prey,
        initial_predators=initial_predators,
        generations=generations,
        seed=seed,
    )

    return model.run()


def add_common_seed_argument(parser) -> None:
    """Add the optional seed argument to a subparser.

    Args:
        parser: argparse subparser.
    """
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible simulations.",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Returns:
        Configured argparse.ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Run stochastic population simulations."
    )

    subparsers = parser.add_subparsers(
        dest="model",
        required=True,
        help="Population model to run.",
    )

    birth_death_parser = subparsers.add_parser(
        "birth_death",
        help="Run the simple birth-death model.",
    )
    birth_death_parser.add_argument("--lambda-birth", type=float, required=True)
    birth_death_parser.add_argument("--mu-death", type=float, required=True)
    birth_death_parser.add_argument(
        "--initial-population",
        type=int,
        required=True,
    )
    birth_death_parser.add_argument("--generations", type=int, required=True)
    add_common_seed_argument(birth_death_parser)
    birth_death_parser.set_defaults(func=run_birth_death)

    logistic_parser = subparsers.add_parser(
        "logistic",
        help="Run the logistic population model.",
    )
    logistic_parser.add_argument("--lambda-birth", type=float, required=True)
    logistic_parser.add_argument("--mu-death", type=float, required=True)
    logistic_parser.add_argument(
        "--carrying-capacity",
        type=float,
        required=True,
    )
    logistic_parser.add_argument(
        "--initial-population",
        type=int,
        required=True,
    )
    logistic_parser.add_argument("--generations", type=int, required=True)
    add_common_seed_argument(logistic_parser)
    logistic_parser.set_defaults(func=run_logistic)

    age_parser = subparsers.add_parser(
        "age_structured",
        help="Run the age-structured population model.",
    )
    age_parser.add_argument(
        "--birth-rates",
        type=parse_float_list,
        required=True,
        help="Comma-separated birth rates, for example: 0.2,0.5,0.1",
    )
    age_parser.add_argument(
        "--death-rates",
        type=parse_float_list,
        required=True,
        help="Comma-separated death rates, for example: 0.1,0.05,0.2",
    )
    age_parser.add_argument(
        "--initial-age-distribution",
        type=parse_int_list,
        required=True,
        help="Comma-separated populations, for example: 10,20,5",
    )
    age_parser.add_argument("--generations", type=int, required=True)
    age_parser.add_argument(
        "--age-groups",
        type=parse_str_list,
        default=None,
        help="Optional comma-separated names, for example: young,adult,elder",
    )
    add_common_seed_argument(age_parser)
    age_parser.set_defaults(func=run_age_structured)

    predator_prey_parser = subparsers.add_parser(
        "predator_prey",
        help="Run the predator-prey population model.",
    )
    predator_prey_parser.add_argument(
        "--lambda-prey",
        type=float,
        required=True,
    )
    predator_prey_parser.add_argument("--mu-prey", type=float, required=True)
    predator_prey_parser.add_argument(
        "--lambda-pred",
        type=float,
        required=True,
    )
    predator_prey_parser.add_argument("--mu-pred", type=float, required=True)
    predator_prey_parser.add_argument(
        "--predation-rate",
        type=float,
        required=True,
    )
    predator_prey_parser.add_argument(
        "--initial-prey",
        type=int,
        required=True,
    )
    predator_prey_parser.add_argument(
        "--initial-predators",
        type=int,
        required=True,
    )
    predator_prey_parser.add_argument("--generations", type=int, required=True)
    add_common_seed_argument(predator_prey_parser)
    predator_prey_parser.set_defaults(func=run_predator_prey)

    return parser


def interactive_main() -> None:
    """Run the simulation using an interactive terminal menu."""
    print("Choose a population model:")
    print("1. Simple birth-death")
    print("2. Logistic")
    print("3. Age-structured")
    print("4. Predator-prey")

    choice = input("Model number: ").strip()

    try:
        if choice == "1":
            result = run_birth_death_interactive()
        elif choice == "2":
            result = run_logistic_interactive()
        elif choice == "3":
            result = run_age_structured_interactive()
        elif choice == "4":
            result = run_predator_prey_interactive()
        else:
            print("Invalid choice.")
            return

        print_result(result)
    except (TypeError, ValueError) as error:
        print(f"Input error: {error}")


def command_line_main() -> None:
    """Parse command-line arguments, run the model, and print results."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = args.func(args)
        print_result(result)
    except (TypeError, ValueError) as error:
        parser.error(str(error))


def main() -> None:
    """Run interactive mode if no arguments are provided."""
    if len(sys.argv) == 1:
        interactive_main()
    else:
        command_line_main()


if __name__ == "__main__":
    main()