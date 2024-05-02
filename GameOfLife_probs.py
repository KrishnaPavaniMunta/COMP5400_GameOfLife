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
GRAY = (169, 169, 169)

def initialize_grid():
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
    titletext = font.render(f"CONWAY'S GAME OF LIFE", True, WHITE)
    alive_cells_text = font.render(f"Alive Cells: {alive_cells}", True, WHITE) 
    screen.blit(text, (10, 10))
    screen.blit(titletext, (450, 10))
    screen.blit(alive_cells_text, (10, 50))
    pygame.display.update()

def update_grid(grid, generation, alive_cells, Pdeath):
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1:
                # Apply stochastic death
                if random.random() < Pdeath or neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
            else:
                # Stochastic birth
                if neighbors == 3 and random.random() > Pdeath:
                    new_grid[row][col] = 1
    generation += 1
    alive_cells = np.sum(new_grid)
    return new_grid, generation, alive_cells

def draw_slider(screen, slider_position, slider_label):
    font = pygame.font.Font(None, 24)
    pygame.draw.rect(screen, WHITE, (slider_position[0], slider_position[1], 100, 10), 1)
    value_text = font.render(f"{slider_label}: {slider_position[2]:.2f}", True, WHITE)
    screen.blit(value_text, (slider_position[0] + 110, slider_position[1] - 10))

def handle_slider_event(event, slider_position):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if slider_position[0] <= event.pos[0] <= slider_position[0] + 100 and slider_position[1] <= event.pos[1] <= slider_position[1] + 10:
            slider_position[3] = True
    elif event.type == pygame.MOUSEBUTTONUP:
        slider_position[3] = False
    elif event.type == pygame.MOUSEMOTION and slider_position[3]:
        slider_position[2] = (event.pos[0] - slider_position[0]) / 100
        slider_position[2] = max(0, min(slider_position[2], 1))


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
    # Initialize Pygame and sliders
    Pdeath_slider = [10, HEIGHT - 40, 0.1, False]  # x, y, value, is_dragging

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

        if simulation_running and current_time - last_update_time > update_interval:
            # grid, generation, alive_cells = update_grid(grid, generation, alive_cells, Pdeath_slider[2])
            #alive_cells_array.append(alive_cells)
            last_update_time = current_time
            # Handle events
        for event in pygame.event.get():
            handle_slider_event(event, Pdeath_slider)

        if simulation_running:
            grid, generation, alive_cells = update_grid(grid, generation, alive_cells, Pdeath_slider[2])
            alive_cells_array.append(alive_cells)
        draw_grid(screen, grid, generation, alive_cells)
        draw_slider(screen, Pdeath_slider, "Pdeath")
        pygame.display.update()

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

if __name__ == "__main__":
    main()