import pygame
import numpy as np
import time
import matplotlib.pyplot as plt
import csv
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
n = 6  # Number of neighbors for the special rule

def initialize_grid():
    return np.zeros((ROWS, COLS))

def initialize_age_grid():
    return np.zeros((ROWS, COLS))

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
    alive_cells_text = font.render(f"Alive Cells: {alive_cells}", True, WHITE)
    titletext = font.render(f"CONWAY'S GAME OF LIFE", True, WHITE)
    screen.blit(text, (10, 10))
    screen.blit(alive_cells_text, (10, 50))
    screen.blit(titletext, (450, 10))
    pygame.display.update()

# def update_grid(grid, generation, alive_cells):
#     new_grid = grid.copy()
#     alive_cells = 0
    
#     # live_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if grid[row, col] == 1]
#     live_cells = []
#     for row in range(ROWS):
#         for col in range(COLS):
#             if grid[row][col] == 1:  # Check if the cell is alive
#                 live_cells.append((row, col))  # Add the coordinates of the live cell to the list
#     random.shuffle(live_cells)  # Shuffle the order of live cell coordinates
#     for row in range(ROWS):
#         for col in range(COLS):
#             neighbors = count_neighbors(grid, row, col)
#             if grid[row][col] == 1:
#                 alive_cells +=1
#                 if neighbors < 2 or neighbors > 3:
#                     new_grid[row][col] = 0  # Die if fewer than 2 or more than 3 neighbors
#                 if neighbors == n:
#                     new_grid[row][col] = 0  # Sacrifice if exactly n neighbors
#             else:
#                 if neighbors == 3:
#                     alive_cells += 1
#                     new_grid[row][col] = 1  # Birth if exactly 3 neighbors
#     generation += 1
#     alive_cells = np.sum(new_grid)
#     return new_grid, generation, alive_cells


# def count_neighbors(grid, row, col):
#     count = 0
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if i == 0 and j == 0:
#                 continue
#             if (0 <= row + i < ROWS) and (0 <= col + j < COLS): #if cell is within bounds of grid
#                 count += grid[row + i][col + j]
#     return count
    

def update_grid(grid, generation, alive_cells, n):
    ROWS, COLS = grid.shape
    new_grid = grid.copy()
    alive_cells = 0


    live_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if grid[row, col] == 1]
    random.shuffle(live_cells)  # Shuffle the order of live cell coordinates


    for i in live_cells:
        if new_grid[i[0], i[1]] == 1:
            neighbors = count_neighbors(new_grid, i[0], i[1])
            if neighbors == n:
                new_grid[i[0], i[1]] = 0
    
    # # First pass: handle the 'sacrifice' of live cells
    # for (row, col) in live_cells:
    #     if new_grid[row, col] == 1:  # Check if still alive
    #         neighbors = count_neighbors(new_grid, row, col)
    #         if neighbors == n:
    #             new_grid[row, col] = 0  # Sacrifice if exactly n neighbors

    # Second pass: apply regular Game of Life rules to the updated grid
    final_grid = new_grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(new_grid, row, col)  # Use new_grid for updated neighbor counts
            if new_grid[row, col] == 1:
                if neighbors < 2 or neighbors > 3:
                    final_grid[row, col] = 0  # Die by underpopulation or overpopulation
            else:
                if neighbors == 3:
                    final_grid[row, col] = 1  # Birth if exactly 3 neighbors
                    alive_cells +=1

    generation += 1
    alive_cells = np.sum(final_grid)
    return final_grid, generation, alive_cells

def count_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            n_row, n_col = row + i, col + j
            if 0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1]:
                count += grid[n_row, n_col]
    return count

def update_initial_config(grid, age_grid, row, col):
    if 0 <= row < ROWS and 0 <= col < COLS:
        grid[row][col] = 1
        age_grid[row][col] = 1  # Start with age 1 upon initial placement

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
    update_interval = 0.1
    generation = 0
    alive_cells = 0
    alive_cells_array = []
    all_lifespans = []

    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                placing_cells = True if event.button == 1 else placing_cells
            elif event.type == pygame.MOUSEBUTTONUP:
                placing_cells = False if event.button == 1 else placing_cells
            elif event.type == pygame.MOUSEMOTION and placing_cells:
                x, y = event.pos
                update_initial_config(grid, age_grid, y // CELL_SIZE, x // CELL_SIZE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_r:
                    grid = initialize_grid()
                    age_grid = initialize_age_grid()
                    generation = 0
                    alive_cells = 0

        if simulation_running and current_time - last_update_time > update_interval:
            grid, age_grid, generation, alive_cells, lifespans = update_grid(grid, age_grid, generation)
            all_lifespans.extend(lifespans)
            alive_cells_array.append(alive_cells)
            last_update_time = current_time

        draw_grid(screen, grid, generation, alive_cells)

    pygame.quit()

    if all_lifespans:
        average_lifespan = np.mean(all_lifespans)
        print("Average Lifespan of Cells:", average_lifespan)

    plt.plot(range(len(alive_cells_array)), alive_cells_array)
    plt.xlabel('Generation')
    plt.ylabel('Alive Cells')
    plt.title('Game of Life: Alive Cells Over Generations')
    plt.grid(True)
    plt.show()

    with open('AliveCells.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ')
        csv_writer.writerow(alive_cells_array)

if __name__ == "__main__":
    main()
