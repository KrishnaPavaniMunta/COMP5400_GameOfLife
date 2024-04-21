import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

ON = 255
OFF = 0
vals = [ON, OFF] 

generation_count = 0
glider = np.array([[0, 0, 255], 
                   [255, 0, 255], 
                   [0, 255, 255]])

block = np.array([[255, 255],
                  [255, 255]])

blinker = np.array([[255, 255, 255]])

spaceship = np.array([[0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255]])

r_pentomino = np.array([[0, 255, 255],
                        [255, 255, 0],
                        [0, 255, 0]])


def randomGrid(N): 
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N) 

def addPattern(i, j, grid, pattern): 
    """adds a pattern with top left cell at (i, j)"""
    pattern_height, pattern_width = pattern.shape
    grid[i:i+pattern_height, j:j+pattern_width] = pattern

def selfishBehavior(i, j, grid, N):
    """Handle selfish behavior of chips"""
    total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                 grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                 grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                 grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
    
    vitality = 0  # Vitality factor for selfish chip
    
    if total >= 4:  # Chip is surrounded by 4 or more chips
        vitality = total - 3
        killNeighborsClockwise(i, j, grid, N, total - 3)
    elif total <= 1:  # Chip has 0 or 1 neighbor
        if grid[i, j] == ON and generation_count > vitality:
            grid[i, j] = OFF
            generation_count -= 1
        vitality = 0
    
    return vitality

def killNeighborsClockwise(i, j, grid, N, num_to_kill):
    """Kill neighbors in a clockwise manner until num_to_kill neighbors are left"""
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]  # Clockwise directions
    
    for direction in directions:
        if num_to_kill == 0:
            break
        
        dx, dy = direction
        x, y = i + dx, j + dy
        
        if grid[x % N, y % N] == ON:
            grid[x % N, y % N] = OFF
            num_to_kill -= 1

def update(frameNum, img, grid, N, text): 
    global generation_count
    
    newGrid = grid.copy() 
    for i in range(N): 
        for j in range(N): 
            if grid[i, j] == ON:
                vitality = selfishBehavior(i, j, grid, N)
                
                total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                             grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                             grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                             grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
                
                if total < 2 or total > 3: 
                    newGrid[i, j] = OFF 
                elif total == 3 or total == 4: 
                    newGrid[i, j] = ON 

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
    img = ax.imshow(grid, interpolation='nearest') 
    text = ax.text(0.5, 1.05, "", transform=ax.transAxes, ha="center")
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
