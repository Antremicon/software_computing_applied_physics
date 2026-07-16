
"""Command-line interface for stochastic population simulations."""

import argparse

from models.age_structured import AgeStructured
from models.birth_death import SimpleBirthDeath
from models.logistic import Logistic
from models.predator_prey import PredatorPrey



def parse_float_list(value: str) -> list[float]:
    """Parse a comma-separated string into a list of floats.

    Args:
     ma-separated numeric values.

    Returns:
        List of floats.

    Raises:
        ValueError: If one of the values cannot be converted to float.
    """
    return [float(item.strip()) for item in value.split(",")]


def parse_int_list(value: str) -> list[int]:
    """Parse a comma-separated string into a list of integers.

    Args:
        value: Comma-separated integer values.

    Returns:
        List of integers.

    Raises:
        ValueError: If one of the values cannot be converted to int.
    """
    return [int(item.strip()) for item in value.split(",")]


def parse_str_list(value: str) -> list[str]:
    """Parse a comma-separated string into a list of strings.

    Args:
        value: Comma-separated text values.

    Returns:
        List of stripped strings.
    """
    return [item.strip() for item in value.split(",")]



def print_result(result) -> None:
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


def run_birth_death(args):
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


def run_logistic(args):
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


def run_age_structured(args):
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


def run_predator_prey(args):
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


def build_parser():
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


def main() -> None:
    """Parse command-line arguments, run the model, and print results."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = args.func(args)
        print_result(result)
    except (TypeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
