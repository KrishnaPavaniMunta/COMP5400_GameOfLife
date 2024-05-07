'''

Title: Sacrifice Rules to Conway's Game of Life
Authors: Krishna Pavani Munta, Abulfat Asadov, Ruth Onoba
Place: University of Leeds
Date: 06/05/2024

Description: A non-deterministic n-die game where the cells play a pre-game before 
the nature rules apply. A cell having exactly "n" neighbours will sacrifice itself.
 
Input: 
n --> number of neighbours for sacrifice.

'''

# importing all the dependencies
import pygame
import numpy as np
import time
import matplotlib.pyplot as plt
import random
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

#input for n-die game
n = int(input("Please input the number of neighbours for the cell to sacrifice itself: "))


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
    
    
# getting the alive cells list and shuffling them for the pre-game
def get_alive_cells(grid):
    alive_cells = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                alive_cells.append((row, col))
    random.shuffle(alive_cells)  # Shuffle the list of alive cell coordinates
    return alive_cells

# Upgrading the grid for eacch generation
def update_grid(grid, generation, alive_cells):
    new_grid = grid.copy()
    alive_cells = 0
    # sacrificial pre-game
    alive_cells_array = get_alive_cells(grid)
    for row, col in alive_cells_array:
        neighbors = count_neighbors(grid, row, col)
        if neighbors == n:  # Check if alive cell has more than 5 neighbors
            new_grid[row][col] = 0  # Sacrifice the alive cell
            
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
                if event.button == 1:
                    placing_cells = True
                elif event.button == 3:
                    placing_cells = False
            elif event.type == pygame.MOUSEMOTION:
                if placing_cells:
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    update_initial_config(grid,row,col)
                    alive_cells = np.sum(grid)
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        grid[row][col] = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_c:
                    placing_cells = not placing_cells
                elif event.key == pygame.K_r:
                    grid = initialize_grid()
                    generation = 0
                    alive_cells = 0
        # Upgrading the grid and alive cells count
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
    
    with open('AliveCells.csv', 'w', newline = '') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ' ')
        my_writer.writerow(alive_cells_array)

if __name__ == "__main__":
    main()
