import pygame
import numpy as np
import time
import random
import matplotlib.pyplot as plt

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

def initialize_grid():
    """Initialize the grid with random live cells for a more interesting start."""
    grid = np.zeros((ROWS, COLS), dtype=int)
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col] = random.randint(0, 1)  # Randomly assign cell as live or dead
    return grid

def draw_grid(screen, grid, next_grid):
    """Draw the current state of the grid with indications for deaths and births."""
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            color = GRAY if grid[row][col] == 0 else GREEN
            if grid[row][col] == 1 and next_grid[row][col] == 0:
                color = RED  # Cells that will die
            elif grid[row][col] == 0 and next_grid[row][col] == 1:
                color = BLUE  # Cells that will be born
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

def update_grid(grid):
    """Apply the rules of Conway's Game of Life to update the grid."""
    new_grid = np.zeros((ROWS, COLS), dtype=int)
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row][col] = 0
            elif grid[row][col] == 0 and neighbors == 3:
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = grid[row][col]
    return new_grid

def count_neighbors(grid, row, col):
    """Count the number of live neighbors around a specific cell."""
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            n_row, n_col = row + i, col + j
            if 0 <= n_row < ROWS and 0 <= n_col < COLS:
                total += grid[n_row][n_col]
    return total

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid = initialize_grid()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        next_grid = update_grid(grid)
        draw_grid(screen, grid, next_grid)
        grid = next_grid
        clock.tick(10)  # Limit the frame rate to 10 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
