'''
Title: Selfish Rules to Conway's Game of Life
Authors: Krishna Pavani Munta, Abulfat Asadov, Ruth Onoba
Place: University of Leeds
Date: 05/05/2024
Description: The code allots an alive cell with a percentage of selfish behaviour 

Input: SELFISHNESS_LEVEL in range of 0 to 100

'''
import pygame
import numpy as np
import time
import random
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
SELFISHNESS_LEVEL = float(input("Please enter level of selfishness(0-100):"))/100  # Adjust the level of selfishness as needed

def initialize_grid():
    return np.zeros((ROWS, COLS))

import numpy as np

def initialize_selfishness(grid, SELFISHNESS_LEVEL):
    num_alive_cells = int(np.sum(grid))  # Count the number of alive cells
    alive_indices = np.argwhere(grid == 1)  # Get indices of alive cells
    num_cells_to_set_selfish = int(num_alive_cells * SELFISHNESS_LEVEL)  # Determine the number of cells to set selfishness for

    # Randomly select indices to set selfishness for
    indices_to_set_selfish = np.random.choice(len(alive_indices), num_cells_to_set_selfish, replace=False)

    selfishness = np.zeros_like(grid)  # Initialize selfishness matrix
    # Set selfishness to 1 for selected indices
    for idx in indices_to_set_selfish:
        row, col = alive_indices[idx]
        selfishness[row][col] = 1

    return selfishness

def is_selfish(cell_row, cell_col, selfishness):
    return selfishness[cell_row][cell_col] == 1



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
    screen.blit(alive_cells_text, (10, 50))
    screen.blit(titletext, (450, 10))
    pygame.display.update()

def update_grid(grid, generation, selfishness, alive_cells):
    new_grid = grid.copy()
    alive_cells = 0
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if is_selfish(row, col, initialize_selfishness(grid, SELFISHNESS_LEVEL)):  # cell is selfish
                if grid[row][col] == 1:
                    if neighbors >= 4:  # Rule 1
                        selfishness[row][col] += 1
                        kill_neighbors(new_grid, row, col)
                    elif neighbors <= 1:
                        if selfishness[row][col] >= 1:  # Rule 2
                            selfishness[row][col] -= 1
                        else:
                            grid[row][col] = 0
                else:  # Cell is dead
                    if neighbors == 3 or neighbors == 4:  # Rule 3
                        new_grid[row][col] = 1
                         # Assign selfishness randomly with a 25% chance to be 1
                        selfishness[row][col] = 1 if random.random() < SELFISHNESS_LEVEL else 0  # Rule 4
            else:
                if grid[row][col] == 1:
                    alive_cells += 1
                    if neighbors < 2 or neighbors > 3:
                        new_grid[row][col] = 0
                else:
                    if neighbors == 3:
                        new_grid[row][col] = 1
                        alive_cells += 1
    generation += 1
    alive_cells = np.sum(new_grid)
    return new_grid, generation, alive_cells

def kill_neighbors(grid, row, col):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Clockwise direction: left, down, right, up
    neighbors =  count_neighbors(grid, row, col) # Counter to track the number of neighbors killed
    
    for dx, dy in directions:
        while neighbors >= 3:
            new_row, new_col = row + dy, col + dx
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and grid[new_row][new_col] == 1:
                grid[new_row][new_col] = 0  # Kill neighbor
                neighbors -= 1  # Increment the counter
                row, col = new_row, new_col  # Move to the next neighbor
                
            else:
                break
    

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
    selfishness = initialize_selfishness(grid, SELFISHNESS_LEVEL)
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

        if simulation_running and current_time - last_update_time > update_interval:
            grid, generation, alive_cells = update_grid(grid, generation, selfishness, alive_cells)
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