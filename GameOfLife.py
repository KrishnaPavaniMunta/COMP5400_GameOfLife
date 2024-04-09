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

def addGlider(i, j, grid): 
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255], 
                    [255, 0, 255], 
                    [0, 255, 255]]) 
    grid[i:i+3, j:j+3] = glider 
   
# Add other pattern functions similarly

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
    parser.add_argument('--glider', action='store_true', required=False)
    # Add other pattern arguments similarly
    args = parser.parse_args() 
    
    # set grid size 
    N = 200
    if args.N and int(args.N) > 8: 
        N = int(args.N) 
        
    # set animation update interval 
    updateInterval = 50
    if args.interval: 
        updateInterval = int(args.interval) 

    # declare grid 
    grid = np.array([]) 

    # check if "glider" demo flag is specified 
    if args.glider: 
        grid = np.zeros(N*N).reshape(N, N) 
        addGlider(1, 1, grid) 
    # Add other pattern conditions similarly

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
