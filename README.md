## Project Scope

This project focuses on simulating stochastic population models using the
Monte Carlo method. The goal is to study how random events such as births,
deaths, and population interactions affect the evolution of one or more
populations over time.

The simulation will use a discrete-time approach and will include multiple
population models with random outcomes generated through Monte Carlo sampling.

## Features

The simulator includes four population models:

1. **Simple Birth-Death Model**
   - One population.
   - Each individual has a constant birth probability and death probability at every generation.

2. **Logistic Model**
   - One population with carrying capacity.
   - Birth probability decreases as the population approaches the carrying capacity.

3. **Age-Structured Model**
   - One population divided into age groups.
   - Birth and death rates can be different for each age group.
   - Individuals age from one group into the next at each generation.

4. **Predator-Prey Model**
   - Two interacting populations: prey and predators.
   - Prey deaths increase with predator density.
   - Predator births increase with prey availability.


## Project Structure


software_computing_applied_physics/
│
├── main.py
├── monte_carlo.py
├── utils.py
│
├── models/
│   ├── birth_death.py
│   ├── logistic.py
│   ├── age_structured.py
│   └── predator_prey.py
│
├── tests/
│   ├── test_birth_death.py
│   ├── test_logistic.py
│   ├── test_age_structured.py
│   ├── test_predator_prey.py
│   ├── test_monte_carlo.py
│   ├── test_main.py
│   └── test_utils.py
│
├── requirements.txt
└── README.md

## Installation

Clone the repository or download the project files, then open a terminal in the project root.

Create and activate a virtual environment:

```
python -m venv .venv
```

On Windows:

```
.venv\Scripts\activate
```

On macOS or Linux:

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

If `requirements.txt` is not available yet, install `pytest` manually:

```
pip install pytest
```

## Requirements

- Python 3.10 or newer is recommended.
- `pytest` is required to run the test suite.

The simulation code itself uses only the Python standard library.

## Usage

The main entry point is `main.py`.

You can run the program in two ways:

1. Interactive guided mode.
2. Direct command-line mode.

## Interactive Guided Mode

Run:

```
python main.py
```

The program will ask you to choose a model:

```
Choose a population model:
1. Simple birth-death
2. Logistic
3. Age-structured
4. Predator-prey
```

After selecting the model, the program asks for the required parameters one by one.

This mode is recommended when you want to avoid long commands or reduce the risk of typing mistakes.

## Direct Command-Line Mode

Direct command-line mode is useful when you want to run reproducible simulations quickly or document exact commands.

### Simple Birth-Death Model

```
python main.py birth_death --lambda-birth 0.4 --mu-death 0.2 --initial-population 10 --generations 5 --seed 42
```

Parameters:

- `--lambda-birth`: birth probability per individual, in `(0, 1]`.
- `--mu-death`: death probability per individual, in `(0, 1]`.
- `--initial-population`: starting population size, greater than `0`.
- `--generations`: number of generations, greater than `0`.
- `--seed`: optional integer seed for reproducibility.

### Logistic Model

```
python main.py logistic --lambda-birth 0.4 --mu-death 0.1 --carrying-capacity 100 --initial-population 20 --generations 5 --seed 42
```

Parameters:

- `--lambda-birth`: base birth probability, in `(0, 1]`.
- `--mu-death`: death probability, in `(0, 1]`.
- `--carrying-capacity`: carrying capacity `K`, greater than `0`.
- `--initial-population`: starting population size, greater than `0`.
- `--generations`: number of generations, greater than `0`.
- `--seed`: optional integer seed for reproducibility.

### Age-Structured Model

```
python main.py age_structured --birth-rates 0.2,0.5,0.1 --death-rates 0.1,0.05,0.2 --initial-age-distribution 10,20,5 --generations 5 --age-groups young,adult,elder --seed 42
```

Parameters:

- `--birth-rates`: comma-separated birth probabilities for each age group.
- `--death-rates`: comma-separated death probabilities for each age group.
- `--initial-age-distribution`: comma-separated starting populations for each age group.
- `--generations`: number of generations, greater than `0`.
- `--age-groups`: optional comma-separated age group names.
- `--seed`: optional integer seed for reproducibility.

The age-structured lists must have the same length. For example, if there are three birth rates, there must also be three death rates and three initial age distribution values.

### Predator-Prey Model

```
python main.py predator_prey --lambda-prey 0.4 --mu-prey 0.1 --lambda-pred 0.2 --mu-pred 0.1 --predation-rate 0.01 --initial-prey 50 --initial-predators 10 --generations 5 --seed 42
```

Parameters:

- `--lambda-prey`: prey birth probability, in `(0, 1]`.
- `--mu-prey`: base prey death probability, in `(0, 1]`.
- `--lambda-pred`: predator birth probability, in `(0, 1]`.
- `--mu-pred`: predator death probability, in `(0, 1]`.
- `--predation-rate`: non-negative predation strength.
- `--initial-prey`: initial prey population, greater than `0`.
- `--initial-predators`: initial predator population, greater than `0`.
- `--generations`: number of generations, greater than `0`.
- `--seed`: optional integer seed for reproducibility.

## Output

The program prints:

- the model name,
- the number of simulated generations,
- the seed used,
- final population values,
- model parameters,
- population values over time,
- event counts such as births and deaths.

## Reproducibility

These stochastic simulations use random sampling, so results may change between runs.

To make a simulation reproducible, pass a seed:

```
python main.py birth_death --lambda-birth 0.4 --mu-death 0.2 --initial-population 10 --generations 5 --seed 42
```

Running the same model with the same parameters and the same seed should produce the same result.

## Running Tests

The project uses `pytest`.

Run the full test suite from the project root:

```
pytest -v
```

or

```
python -m pytest tests/ -v
```

A successful run should show all tests passing.