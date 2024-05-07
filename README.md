# Conway's Game of Life and its extended implementations

Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

## Aim

The aim of this project is to analyze the emergent behavior of cells when the initial rules of Conway's Game of Life are modified. By changing the rules to non-deterministic ones and introducing new behaviors such as selfishness, sacrifice, and stochastic growth, we aim to deepen our understanding of cellular automata.

## File Structure

| File                       | Purpose                                                         |
|----------------------------|-----------------------------------------------------------------|
| `GameOfLife_CustomPlace.py`| Original Game of Life implementation with custom cell placement|
| `GameOfLife_SelfishRules.py`| Implementation where cells exhibit selfish behavior           |
| `GameOfLife_SacrificeRules.py`| Implementation where cells exhibit sacrifice behavior         |
| `stochastic_GOL.py`       | Implementation with stochastic growth properties               |

## How to Play

### Game of Life (Original)
- Run `GameOfLife_CustomPlace.py`.
- Left-click to place live cells, right-click to remove.
- Press spacebar to start/stop the simulation.
- Press 'r' to reset the grid.

### Selfish Rules
- Run `GameOfLife_SelfishRules.py`.
- The cells exhibit selfish behavior with a specified level of selfishness.
- Specify the level of selfishness when prompted.

### Sacrifice Rules
- Run `GameOfLife_SacrificeRules.py`.
- The cells exhibit sacrifice behavior where they sacrifice themselves if they have a certain number of neighbors.
- Specify the number of neighbors for sacrifice when prompted.

### Stochastic Growth
- Run `stochastic_GOL.py`.
- Cells exhibit self-healing and self-controlled growth properties.
- Specify the probability of cell death when prompted.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/GameOfLife.git
    ```

2. Navigate to the directory:

    ```bash
    cd GameOfLife
    ```

3. Run the desired implementation file as mentioned above.


### Dependencies

The main dependencies for running the various versions of Conway's Game of Life are:

1. **Python**: Python is the primary programming language used for implementing the game and its variations. Ensure you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **pygame**: Pygame is a cross-platform set of Python modules designed for writing video games. It includes computer graphics and sound libraries. To install pygame, you can use pip, Python's package manager.

3. **numpy**: Numpy is a fundamental package for scientific computing with Python. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays. Install numpy using pip.

4. **matplotlib**: Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. It is used for plotting the generation vs. alive cells graph. Install matplotlib using pip.

5. **csv** (optional): The csv module is used for reading and writing CSV files. It is used in one of the implementations to save data to a CSV file.

### Installation Instructions

You can install the dependencies using pip, which is the package installer for Python. Open your terminal or command prompt and execute the following commands:

```bash
pip install pygame numpy matplotlib
```

If you choose to run the version that utilizes the `csv` module, you can install it with:

```bash
pip install csv
```

These commands will install all the necessary dependencies required to run Conway's Game of Life and its extended implementations.

Once the dependencies are installed, you can run each version of the game by executing the corresponding Python script. For example:

```bash
python GameOfLife_CustomPlace.py
```

Ensure that you are in the correct directory where the Python scripts are located when running the commands. With the dependencies installed, you should be able to enjoy exploring the different implementations of Conway's Game of Life!

### Acknowledgments

1.John Horton Conway for creating Conway's Game of Life.
2.The Python community for developing and maintaining the libraries used in this project.

Enjoy exploring the various behaviors of cellular automata in Conway's Game of Life!
