# Python code to implement Conway's Game Of Life 
import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

# setting up the values for the grid 
ON = 255
OFF = 0
vals = [ON, OFF] 

def randomGrid(N): 
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N) 

def addPattern(i, j, grid, pattern): 
    """adds a pattern with top left cell at (i, j)"""
    pattern_height, pattern_width = pattern.shape
    grid[i:i+pattern_height, j:j+pattern_width] = pattern
   
# Define various patterns
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

def update(frameNum, img, grid, N, text): 
    global generation_count
    
    # copy grid since we require 8 neighbors 
    # for calculation and we go line by line 
    newGrid = grid.copy() 
    for i in range(N): 
        for j in range(N): 

            # compute 8-neighbor sum 
            # using toroidal boundary conditions - x and y wrap around 
            # so that the simulation takes place on a toroidal surface. 
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255) 

            # apply Conway's rules 
            if grid[i, j] == ON: 
                if (total < 2) or (total > 3): 
                    newGrid[i, j] = OFF 
            else: 
                if total == 3: 
                    newGrid[i, j] = ON 

    # update data 
    img.set_data(newGrid) 
    grid[:] = newGrid[:] 
    generation_count += 1
    text.set_text("Generation: {}".format(generation_count))
    return img, text

# main() function 
def main(): 
    global generation_count

    generation_count = 0
    
    # Command line args are in sys.argv[1], sys.argv[2] .. 
    # sys.argv[0] is the script name itself and can be ignored 
    # parse arguments 
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

    # add arguments 
    parser.add_argument('--grid-size', dest='N', required=False) 
    parser.add_argument('--mov-file', dest='movfile', required=False) 
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--pattern', dest='pattern', required=False)
    parser.add_argument('--position', dest='position', required=False, type=int, nargs=2)
    args = parser.parse_args() 
    
    # set grid size 
    N = 100
    if args.N and int(args.N) > 8: 
        N = int(args.N) 
        
    # set animation update interval 
    updateInterval = 50
    if args.interval: 
        updateInterval = int(args.interval) 

    # declare grid 
    grid = np.zeros(N*N).reshape(N, N) 
    
    # Add user-specified pattern at position
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
        # Add more patterns as needed
        
    else: # populate grid with random on/off - 
        # more off than on 
        grid = randomGrid(N) 

    # set up animation 
    fig, ax = plt.subplots() 
    img = ax.imshow(grid, interpolation='nearest') 
    text = ax.text(0.5, 1.05, "", transform=ax.transAxes, ha="center")
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, text), 
                                frames = 10, 
                                interval=updateInterval, 
                                save_count=50) 

    # # of frames? 
    # set output file 
    if args.movfile: 
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 

    plt.show() 
    print("Total generations:", generation_count)

# call main 
if __name__ == '__main__': 
    main() 
