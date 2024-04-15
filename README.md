Here's how you can improve the `README.md` file:

```markdown
# Conway's Game of Life

Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/GameOfLife.git
    ```

2. Navigate to the directory:

    ```bash
    cd GameOfLife
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the simulation

To run the simulation with random organisms:

```bash
python GameOfLife.py
```

To place a specific pattern at a custom position, use the following format:

```bash
python GameOfLife.py --pattern PATTERN --position X Y
```

Replace `PATTERN` with the name of the pattern (e.g., `glider`, `still_life_block`) and `X` and `Y` with the coordinates to place the organism.

### Available Patterns

1. Glider
2. Still Life Block
3. Oscillator Blinker
4. Spaceship Glider
5. Methuselah R-pentomino

## Examples

To run a glider pattern at position (10, 10):

```bash
python GameOfLife.py --pattern glider --position 10 10
```

To run a still life block at position (5, 5):

```bash
python GameOfLife.py --pattern still_life_block --position 5 5
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

