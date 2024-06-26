'''

Title: Sacrifice Rules to Conway's Game of Life
Authors: Krishna Pavani Munta, Abulfat Asadov, Ruth Onoba
Place: University of Leeds
Date: 19/04/2024

Description: This file is the original implementation of the Game of Life following all the nature's rules. 
The Upgrade Grid function is designed to continuously update the grid by checking the rules of Conway's Game of Life. 
These rules are as follows:

If a living cell has zero or one neighbors, it will die due to loneliness. It will also die if it has more than four neighbors.
If a dead cell is surrounded by exactly three neighbors, a birth will occur, and the cell will become alive.

'''
# importing all the dependencies
import pygame
import numpy as np
import time
import matplotlib.pyplot as plt
import csv


# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
# Creating the grid
def initialize_grid():
    return np.zeros((ROWS, COLS))

# Drawing the grid with different colors and texts
def draw_grid(screen, grid, generation, alive_cells):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Generation: {generation}", True, WHITE)
    titletext = font.render(f"CONWAY'S GAME OF LIFE", True, WHITE)
    alive_cells_text = font.render(f"Alive Cells: {alive_cells}", True, WHITE) 
    screen.blit(text, (10, 10))
    screen.blit(titletext, (450, 10))
    screen.blit(alive_cells_text, (10, 50))
    pygame.display.update()

# Upgrading the grid for each generation
def update_grid(grid, generation, alive_cells):
    new_grid = grid.copy()
    alive_cells = 0
     # nature rules
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1:
                alive_cells += 1
            # rule  Death: If neighbors are less than 2 or greater than 3 
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
            else:
            # rule Birth: If there are 3 neighbours for a dead cell birth takes place
                if neighbors == 3:
                    new_grid[row][col] = 1
                    alive_cells += 1
    generation += 1
    alive_cells = np.sum(new_grid)
    return new_grid, generation, alive_cells

# counting the neighbours of the particular cell
def count_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (0 <= row + i < ROWS) and (0 <= col + j < COLS):
                count += grid[row + i][col + j]
    return count

def update_initial_config(grid, row, col):
    if 0 <= row < ROWS and 0 <= col < COLS:
        grid[row][col] = 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    grid = initialize_grid()
    running = True
    placing_cells = False
    simulation_running = False
    last_update_time = 0
    update_interval = 0.1  # in seconds
    generation = 0
    alive_cells = 0
    alive_cells_array = []

    while running:
        current_time = time.time()
        # interacting with the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    placing_cells = True  # Enable placing cells
                elif event.button == 3:  # Right mouse button
                    placing_cells = False  # Disable placing cells, prepare for clearing if held
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        grid[row][col] = 0  # Clear cell on single right-click
                    alive_cells = np.sum(grid)  # Update alive cells count after modification
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    placing_cells = False  # Disable placing or clearing on any button release
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Check if left button is held during motion
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        grid[row][col] = 1  # Set cell to alive
                elif event.buttons[2]:  # Check if right button is held during motion
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        grid[row][col] = 0  # Clear cells while right mouse button is held
                alive_cells = np.sum(grid)  # Update alive cells count after modification
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_r:
                    grid = initialize_grid()
                    generation = 0
                    alive_cells = 0

        if simulation_running and current_time - last_update_time > update_interval:
            grid, generation, alive_cells = update_grid(grid, generation, alive_cells)
            alive_cells_array.append(alive_cells)
            last_update_time = current_time

        draw_grid(screen, grid, generation, alive_cells)

        if not running:
            # Plot generations vs. alive_cells_array after the simulation loop
            plt.plot(range(generation), alive_cells_array)
            plt.xlabel('Generation')
            plt.ylabel('Alive Cells')
            plt.title('Game of Life: Alive Cells Over Generations')
            plt.grid(True)
            plt.show()

    pygame.quit()

    with open('AliveCells_OG.csv', 'w', newline = '') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ' ')
        my_writer.writerow(alive_cells_array)

if __name__ == "__main__":
    main()