# Conway's Game of Life and its Extended Implementations

## Access Code on GitHub
[Link to GitHub Repository](https://github.com/yourusername/GameOfLife)

## Aim
The aim of this project is to analyze the emergent behavior of cells when the initial rules of Conway's Game of Life are modified. By changing the rules to non-deterministic ones and introducing new behaviors such as selfishness, sacrifice, and stochastic growth, we aim to deepen our understanding of cellular automata.

## File Structure
| File                        | Purpose                                                          |
|-----------------------------|------------------------------------------------------------------|
| GameOfLife_CustomPlace.py   | Original Game of Life implementation with custom cell placement  |
| GameOfLife_SelfishRules.py  | Implementation where cells exhibit selfish behavior              |
| GameOfLife_SacrificeRules.py| Implementation where cells exhibit sacrifice behavior            |
| stochastic_GOL.py           | Implementation with stochastic growth properties                 |

## Functionalities of Extensions
### Game of Life Original
- Stable patterns.
- Can produce highly complex patterns depending on the initial configurations.
- **Emergent Patterns:** Despite its simple rules, the Game of Life can give rise to complex and interesting patterns. These emergent patterns can provide insights into how simple rules can lead to complex behaviors.
- **Stable Patterns:** Configurations that remain unchanged over multiple generations. These stable patterns include still lifes, such as blocks and beehives, where cells remain fixed in position.
- **Oscillators:** Oscillators are patterns that cycle through a set of configurations repeatedly. They can be simple, like blinkers and toads, or more complex, like pentadecathlons and pulsars.
- **Spaceships:** Some patterns move across the grid over time. These are called spaceships or gliders. They maintain their overall shape as they move, often leaving behind a trail of stable patterns or oscillators.
- **Growth and Decay:** Some patterns may grow indefinitely, while others may stabilize or eventually die out.
- **Interaction of Patterns:** Different patterns interact with each other. They can collide, merge, or influence each other's behavior in unexpected ways.
- **Self-Replication:** Some configurations in the Game of Life can self-replicate, creating copies of themselves as they evolve. These replicators are fascinating examples of emergent complexity.
- **Edge Effects:** Because the grid is finite, patterns near the edges may exhibit different behaviors compared to those in the central region.

### Game of Life with Sacrifice Rules
- Number of neighbors when sacrifice happens can be given as input "n".
- Optimization of population for "n" values.
- When "n = 2", new stable patterns other than the defined ones in Conway's Game of Life.

### Game of Life with Selfish Rules
- Level of selfishness can be given in terms of percentage.
- Optimization of population for some levels of selfishness.

### Game of Life with Probability
- The probability and mask can be given as input.
- Cells expand infinitely for some probabilities and can heal themselves.
- Can show some coherent growth properties.

**Note:** All the rules taken into account are just inspirations, and experimentation is done according to the team's creative thinking.

## User Installation
1. Clone this repository:
    ```
    git clone https://github.com/yourusername/GameOfLife.git
    ```
2. Navigate to the directory:
    ```
    cd GameOfLife
    ```
3. Run the desired implementation file as mentioned above.

## Dependencies
The main dependencies for running the various versions of Conway's Game of Life are:

- Python: Primary programming language.
- pygame: Cross-platform set of Python modules designed for writing video games.
- numpy: Fundamental package for scientific computing with Python.
- matplotlib: Comprehensive library for creating static, animated, and interactive visualizations in Python.
- csv (optional): Module used for reading and writing CSV files.

You can install the dependencies using pip, Python's package manager.

## Installation Instructions
1. Install dependencies using pip:
    ```
    pip install pygame numpy matplotlib
    ```
2. If you choose to run the version that utilizes the csv module, you can install it with:
    ```
    pip install csv
    ```

These commands will install all the necessary dependencies required to run Conway's Game of Life and its extended implementations.

Once the dependencies are installed, you can run each version of the game by executing the corresponding Python script. For example:
    ```
    python GameOfLife_CustomPlace.py
    ```
Ensure that you are in the correct directory where the Python scripts are located when running the commands. With the dependencies installed, you should be able to enjoy exploring the different implementations of Conway's Game of Life!

## How to Play
### Game of Life (Original)
- Run `GameOfLife_CustomPlace.py`.
- Left-click to place live cells, right-click to remove.
- Press spacebar to start/stop the simulation.

### Selfish Rules
- Run `GameOfLife_SelfishRules.py`.
- The cells exhibit selfish behavior with a specified level of selfishness.
- Specify the level of selfishness when prompted.

### Sacrifice Rules
- Run `GameOfLife_SacrificeRules.py`.
- The cells exhibit sacrifice behavior where they sacrifice themselves if they have a certain number of neighbors.
- Specify the number of neighbors for sacrifice when prompted.

### Probability of death
- Run `stochastic_GOL.py`.
- Cells exhibit self-healing and self-controlled growth properties.
- Specify the probability of cell death when prompted.

## Acknowledgments
1. John Horton Conway for creating Conway's Game of Life.
2. The Python community for developing and maintaining the libraries used in this project.
3. Yaroslavsky, Leonid. (2013). Self-controlled growth, coherent shrinkage, eternal life in a self-bounded space and other amazing evolutionary dynamics of stochastic pattern formation and growth models inspired by Conways Game of Life.
4. Mühlenbernd, R. and Schulz, S. (2014) The Game of Life, Decision and Communication. Natural Science, 6, 1093-1102. doi: 10.4236/ns.2014.613097.
5. M. R. Lauer, P. A. Mitchem and R. A. Gagliano, "Resource optimization and self interest: variations on the game of life," Proceedings of Simulation Symposium, Phoenix, AZ, USA, 1995, pp. 136-143, doi: 10.1109/SIMSYM.1995.393586.

Enjoy exploring the various behaviors of cellular automata in Conway's Game of Life!
