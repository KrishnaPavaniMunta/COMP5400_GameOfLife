import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

# Define cell states
DEAD = 0
ALIVE = 1

# Define colors
DEAD_COLOR = 'black'
ALIVE_COLOR = 'white'

# Define probabilities for initial grid
DEAD_PROBABILITY = 0.2
ALIVE_PROBABILITY = 0.8

# Define vitality factor thresholds for selfish cells
KILL_THRESHOLD = 5
VITALITY_THRESHOLD = 3

# Define rules for births
BIRTH_RULES = [(3, 1), (4, 0.8)]

def randomGrid(N): 
    """Returns a grid of NxN random values"""
    return np.random.choice([DEAD, ALIVE], N*N, p=[DEAD_PROBABILITY, ALIVE_PROBABILITY]).reshape(N, N) 

def addPattern(i, j, grid, pattern): 
    """Adds a pattern with top left cell at (i, j)"""
    pattern_height, pattern_width = pattern.shape
    grid[i:i+pattern_height, j:j+pattern_width] = pattern
   
# Define various patterns
glider = np.array([[DEAD, DEAD, ALIVE], 
                   [ALIVE, DEAD, ALIVE], 
                   [DEAD, ALIVE, ALIVE]])

block = np.array([[ALIVE, ALIVE],
                  [ALIVE, ALIVE]])

blinker = np.array([[ALIVE, ALIVE, ALIVE]])

spaceship = np.array([[DEAD, DEAD, ALIVE],
                      [ALIVE, DEAD, ALIVE],
                      [DEAD, ALIVE, ALIVE]])

r_pentomino = np.array([[DEAD, ALIVE, ALIVE],
                        [ALIVE, ALIVE, DEAD],
                        [DEAD, ALIVE, DEAD]])

def update(frameNum, img, grid, N, text): 
    global generation_count
    
    # copy grid since we require 8 neighbors 
    newGrid = grid.copy() 
    
    for i in range(N): 
        for j in range(N): 
            total = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    total += grid[(i+dx)%N, (j+dy)%N]  # Apply toroidal boundary conditions
            
            # Selfish cell behavior
            if grid[i, j] == ALIVE:
                if total > KILL_THRESHOLD:
                    newGrid[i, j] = DEAD
                elif total < VITALITY_THRESHOLD:
                    newGrid[i, j] = ALIVE
            
            # Birth rules
            elif grid[i, j] == DEAD:
                for rule in BIRTH_RULES:
                    if total == rule[0] and np.random.random() < rule[1]:
                        newGrid[i, j] = ALIVE
            
    img.set_data(newGrid) 
    grid[:] = newGrid[:] 
    generation_count += 1
    text.set_text("Generation: {}".format(generation_count))
    return img, text

def main(): 
    global generation_count

    generation_count = 0
    
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

    parser.add_argument('--grid-size', dest='N', required=False) 
    parser.add_argument('--mov-file', dest='movfile', required=False) 
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--pattern', dest='pattern', required=False)
    parser.add_argument('--position', dest='position', required=False, type=int, nargs=2)
    args = parser.parse_args() 
    
    N = 100
    if args.N and int(args.N) > 8: 
        N = int(args.N) 
        
    updateInterval = 50
    if args.interval: 
        updateInterval = int(args.interval) 

    grid = np.zeros(N*N).reshape(N, N) 
    
    if args.pattern and args.position:
        if args.pattern == 'glider':
            addPattern(args.position[0], args.position[1], grid, glider)
        elif args.pattern == 'block':
            addPattern(args.position[0], args.position[1], grid, block)
        elif args.pattern == 'blinker':
            addPattern(args.position[0], args.position[1], grid, blinker)
        elif args.pattern == 'spaceship':
            addPattern(args.position[0], args.position[1], grid, spaceship)
        elif args.pattern == 'r_pentomino':
            addPattern(args.position[0], args.position[1], grid, r_pentomino)
        
    else:
        grid = randomGrid(N) 

    fig, ax = plt.subplots() 
    img = ax.imshow(grid, interpolation='nearest', cmap=plt.get_cmap('binary'), vmin=0, vmax=1) 
    text = ax.text(0.5, 1.05, "", transform=ax.transAxes, ha="center", color='white')
    ax.set_facecolor(DEAD_COLOR)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, text), 
                                frames = 10, 
                                interval=updateInterval, 
                                save_count=50) 

    if args.movfile: 
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 

    plt.show() 
    print("Total generations:", generation_count)

if __name__ == '__main__': 
    main() 