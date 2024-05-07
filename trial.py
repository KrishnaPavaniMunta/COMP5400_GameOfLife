import pygame
import numpy as np
import time
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def initialize_grid():
    """Initializes a grid with all cells dead."""
    return np.zeros((ROWS, COLS), dtype=int)

def draw_grid(screen, grid):
    """Draws the cells on the grid."""
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            color = GREEN if grid[row, col] == 1 else GRAY
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

def update_grid(grid):
    """Updates the grid based on Conway's Game of Life rules."""
    new_grid = np.zeros((ROWS, COLS), dtype=int)
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row, col] == 1:
                if neighbors in (2, 3):
                    new_grid[row, col] = 1
            else:
                if neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid

def count_neighbors(grid, row, col):
    """Counts the number of live neighbors around a cell."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            n_row, n_col = row + i, col + j
            if 0 <= n_row < ROWS and 0 <= n_col < COLS:
                count += grid[n_row][n_col]
    return count

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    grid = initialize_grid()
    running = True
    placing = False
    removing = False
    update_interval = 1.0  # Seconds between generation updates
    last_update_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    placing = True
                elif event.button == 3:  # Right mouse button
                    removing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    placing = False
                elif event.button == 3:
                    removing = False
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if placing and 0 <= row < ROWS and 0 <= col < COLS:
                    grid[row][col] = 1
                elif removing and 0 <= row < ROWS and 0 <= col < COLS:
                    grid[row][col] = 0
                draw_grid(screen, grid)  # Update the grid display after change

        # Update the grid based on the Game of Life rules at each interval
        if time.time() - last_update_time > update_interval:
            grid = update_grid(grid)
            draw_grid(screen, grid)
            last_update_time = time.time()

    pygame.quit()

if __name__ == "__main__":
    main()
