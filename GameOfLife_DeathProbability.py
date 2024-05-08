'''

Title:  Death Probability of cells in Conway's Game of Life
Authors: Krishna Pavani Munta, Abulfat Asadov, Ruth Onoba
Place: University of Leeds
Date: 29/04/2024

Description: This file implements the Game of Life with modified rules where probability is introduced into the cell death and additional weighted masks are introduced to neighbors count. The Upgrade Grid function upgrades the rules inspired as mentioned in the paper by Leonid Yaroslavsky .

The modifications made to the standard Conway's model are done in two ways:

The "Deaths" of "live" cells are made stochastic with a certain probability 1/Pdeath, which is a model parameter.
The number of "live" cells in the 8-neighborhood of each cell is counted using a weighted summation with rounding up the summation result instead of a simple summation of their binary values.
Input: 
Masks -> weighted number of neighbours
Pdeath -> probability of death 

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
BLUE = (0, 0, 128)
RED = (255, 0, 255)

#masks as weighted sum
masks = {
    'Standard': np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
    'Isotropic': np.array([[0.7, 1, 0.7], [1, 0, 1], [0.7, 1, 0.7]]),
    'IsotropicDiag': np.array([[1, 0.7, 1], [0.7, 0, 0.7], [1, 0.7, 1]]),
    'Cross': np.array([[0.3, 1, 0.3], [1, 0, 1], [0.3, 1, 0.3]]),
    'Cross4': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
    'Cross4Diag': np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
    'Hex0': np.array([[1, 0, 1], [1, 0, 1], [1, 0, 1]]),
    'Hex1': np.array([[0.75, 0.5, 0.75], [1, 0, 1], [0.75, 0.5, 0.75]]),
    'Hex2': np.array([[1, 0.75, 0.5], [0.75, 0, 0.75], [0.5, 0.75, 1]])
}
print("Available masks:\n", end ="")
print("Standard, Isotropic, Diagonal\n", end ="")
print("Cross, Cross4, Cross4Diag\n", end ="")
print("Hex0, Hex1, Hex2\n",end ="")

#input for the mask
current_mask_name = input("Please input mask name: ")

#validating the mask name from user input
if current_mask_name in masks:
    current_mask = masks[current_mask_name]
else:
    print("Invalid mask name. Please select from the available masks.")
# Define the specific probability of cell death
Pdeath = float(input("Please input the probability (0-1): "))  # Specific probability

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
    mask_text = font.render(f"Mask/Probability: {current_mask_name}/{Pdeath}", True, WHITE)
    alive_cells_text = font.render(f"Alive Cells: {alive_cells}", True, WHITE)
    titletext = font.render(f"CONWAY'S GAME OF LIFE", True, WHITE)
    screen.blit(text, (10, 10))
    screen.blit(alive_cells_text, (10, 40))
    screen.blit(mask_text, (10, 70))
    screen.blit(titletext, (450, 10))
    pygame.display.update()
    
# Upgrading the grid for each generation
def update_grid(grid, generation, alive_cells):
    new_grid = grid.copy()
    alive_cells = 0
    cells_to_die = []

    #Checking the cells which will die and appending to a list
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col, current_mask)
            if grid[row][col] == 1 and (neighbors < 2 or neighbors > 3):
                cells_to_die.append((row, col))

    #number of cells to die
    num_cells_to_die = len(cells_to_die)
    
    # mutiplying with the probability
    expected_deaths = int(round(Pdeath * num_cells_to_die))
    
    # assigns numbers (1 to total number of expected deaths) to death cells randomly 
    # Assigns to death, the ones below expected deaths
    if expected_deaths < num_cells_to_die:
        deaths = random.sample(cells_to_die, expected_deaths) 
    else:
        deaths = cells_to_die

    for row, col in np.ndindex(grid.shape):
        neighbors = count_neighbors(grid, row, col,current_mask)
        # If cell is in death, it dies
        if (row, col) in deaths:
            new_grid[row, col] = 0
        # If the cell is dead and it has 3 neighbours, birth takes place
        elif grid[row, col] == 0 and neighbors == 3:
            new_grid[row, col] = 1

    generation += 1
    alive_cells = np.sum(new_grid)
    return new_grid, generation, alive_cells

# counting the neighbours of the particular cell
def count_neighbors(grid, row, col, mask):
    ROWS, COLS = grid.shape
    total = 0

    # Loop through each position in the 3x3 block centered on the current cell
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the center cell itself
            if i == 0 and j == 0:
                continue
            # Calculate neighbor's coordinates
            n_row, n_col = row + i, col + j
            # Ensure the neighbor is within grid bounds
            if 0 <= n_row < ROWS and 0 <= n_col < COLS:
                # Multiply the neighbor's state (1 or 0) by its corresponding weight
                total += grid[n_row, n_col] * mask[i+1, j+1]

    # Return the sum rounded to the nearest integer
    return int(np.ceil(total))
    
  

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