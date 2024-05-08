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


import pygame
import numpy as np
import time

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

#Creating a grid to place the cells
def initialize_grid():
    return np.zeros((ROWS, COLS))

def initialize_age_grid():
    return np.zeros((ROWS, COLS))
# drawing the cells 
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
# upgrading the grid on each generation
def update_grid(grid, generation, alive_cells, age_grid):
    new_grid = grid.copy()
    new_age_grid = age_grid.copy()
    lifespans = []
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3: #rule 1
                    lifespans.append(age_grid[row][col])
                    new_grid[row][col] = 0
                    new_age_grid[row][col] = 0
                else:
                    new_age_grid[row][col] += 1
            else:
                if neighbors == 3: #rule 2
                    new_grid[row][col] = 1
                    new_age_grid[row][col] = 1
    generation += 1
    return new_grid, new_age_grid, generation, np.sum(new_grid), lifespans

#counting the neighours from left to right
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
    age_grid = initialize_age_grid()
    running = True
    placing_cells = False
    simulation_running = False
    last_update_time = time.time()
    update_interval = 0.1  # in seconds
    generation = 0
    alive_cells = 0
    all_lifespans = []

    while running:
        current_time = time.time()
        # events for interacting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    placing_cells = True
                elif event.button == 3:
                    placing_cells = False
            elif event.type == pygame.MOUSEMOTION:
                if placing_cells:
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    update_initial_config(grid, row, col)
                    alive_cells = np.sum(grid)  # Update alive cells count
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_c:
                    placing_cells = not placing_cells
                elif event.key == pygame.K_r:
                    grid = initialize_grid()
                    generation = 0
                    alive_cells = 0

        if simulation_running and (current_time - last_update_time > update_interval):
            grid, age_grid, generation, alive_cells, lifespans = update_grid(grid, generation, alive_cells, age_grid)
            all_lifespans.extend(lifespans)
            last_update_time = current_time

        draw_grid(screen, grid, generation, alive_cells)

    pygame.quit()

    if all_lifespans:
        average_lifespan = np.mean(all_lifespans)
        print("Average Lifespan of Cells:", average_lifespan)

if __name__ == "__main__":
    main()
