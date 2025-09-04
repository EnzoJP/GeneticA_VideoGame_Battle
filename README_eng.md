# Genetic Algorithms to Defeat Persona 3 Boss

Project developed for the Artificial Intelligence 1 course

Team members: Martinez Paula and Enzo Palau

-------

The goal of this project is to implement genetic algorithms to find the best strategy to defeat the boss "Sleeping Table" from the video game Persona 3, using the skills and characteristics of the available characters.

This battle is simulated via console and outputs the sequence of actions that the characters should perform to defeat the boss according to different criteria. If the user wishes, the battle can also be played manually.

The implemented genetic algorithms include:
- Random algorithm
- Basic genetic algorithm
- Modified and problem-adapted genetic algorithm
- NSGA-II algorithm (using the pymoo library)

----

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/usuario/proyecto-persona3-genetico.git
   cd proyecto-persona3-genetico
   ```

2. Install the `pymoo` library (only necessary if using the nsga-ii algorithm):

   ```bash
   pip install pymoo
   ```

## Execution

To run the genetic algorithm simulation and see the results in the console:

```bash
python main.py
```

During execution, the program will display:

- The user can choose between playing the battle manually (selecting actions each turn) or simulating the battle using different algorithms (random, genetic, modified genetic, NSGA-II).
- In simulation mode, multiple automatic battles are run and statistics such as number of victories, defeats, average turns, and win percentage for each algorithm are shown.
- The best sequence of actions and generation progress are not printed; the focus is on comparing the overall performance of each algorithm.
- At the end of each simulation, aggregate results are displayed (winrate, average turns, execution time).

## Project Structure

- `main.py`: Main file to run the game and simulations.
- `combat/party.py`, `combat/enemy.py`: Definition of characters and boss, along with their skills.
- `combat/combat.py`: Combat simulation logic and user menu.
- `genetics/`: Implementations of the different algorithms (random, model_genetic, modified_genetic, NGSA_ii).
- `combat/metrics_and_plots.py`: Calculation of metrics and generation of plots.
- `proyecto_final.md`: Detailed project documentation, explanation of algorithms, design decisions, and analysis of results.

## Documentation

The complete project documentation, including explanation of the algorithms, parameters used, analysis of results, and possible improvements, can be found in the [`proyecto_final.md`](proyecto_final.md) file.
