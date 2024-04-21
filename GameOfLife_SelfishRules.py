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
SELFISHNESS_LEVEL = 0.5  # Adjust the level of selfishness as needed

def initialize_grid():
    return np.zeros((ROWS, COLS))

def initialize_selfishness():
    return np.random.rand(ROWS, COLS) < SELFISHNESS_LEVEL

def draw_grid(screen, grid, generation):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Generation: {generation}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.update()

def update_grid(grid, generation,selfishness):
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            vitality = 0  # Initialize vitality factor for selfish chip
            if grid[row][col] == 1:
                if neighbors >= 4:  # If a selfish chip is surrounded by 4 or more chips
                    vitality = 1  # Increment vitality factor by one
                    kill_neighbors(new_grid, row, col)  # Kill neighbors in clockwise manner
                elif neighbors <= 1 and selfishness[row][col] > 0:  # If a selfish chip has 0 or 1 neighbor and vitality factor is greater than 0
                    selfishness[row][col] -= 1  # Decrement vitality by one
            else:
                if neighbors == 3 or neighbors == 4:  # Births are allowed at an empty cell if it has 3 or 4 neighbors in its template
                    new_grid[row][col] = 1
                    selfishness[row][col] = random.random() < SELFISHNESS_LEVEL  # Randomly designate the new chip as selfish based on selfishness level
    generation += 1
    return new_grid, generation

def kill_neighbors(grid, row, col):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Clockwise direction: left, down, right, up
    for dx, dy in directions:
        while True:
            new_row, new_col = row + dy, col + dx
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and grid[new_row][new_col] == 1:
                grid[new_row][new_col] = 0  # Kill neighbor
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    grid = initialize_grid()
    selfishness = initialize_selfishness()
    running = True
    placing_cells = False
    simulation_running = False
    last_update_time = 0
    update_interval = 0.1  # in seconds
    generation = 0

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

        if simulation_running and current_time - last_update_time > update_interval:
            grid, generation = update_grid(grid, generation,selfishness)
            last_update_time = current_time

        draw_grid(screen, grid, generation)

    pygame.quit()

if __name__ == "__main__":
    main()
