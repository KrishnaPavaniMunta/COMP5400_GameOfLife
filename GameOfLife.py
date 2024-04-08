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
   

def addStillLifeBlock(i, j, grid):
    """Adds a block still life pattern with top left cell at (i, j)"""
    block = np.array([[255, 255],
                      [255, 255]])
    grid[i:i+2, j:j+2] = block

def addOscillatorBlinker(i, j, grid):
    """Adds a blinker oscillator pattern with top left cell at (i, j)"""
    blinker = np.array([[255, 255, 255]])
    grid[i:i+1, j:j+3] = blinker

def addSpaceshipGlider(i, j, grid):
    """Adds a glider spaceship pattern with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider


def addMethuselahRpentomino(i, j, grid):
    """Adds an R-pentomino Methuselah pattern with top left cell at (i, j)"""
    r_pentomino = np.array([[0, 255, 255],
                             [255, 255, 0],
                             [0, 255, 0]])
    grid[i:i+3, j:j+3] = r_pentomino

# Additional patterns can be added similarly


def update(frameNum, img, grid, N): 

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
	return img, 

# main() function 
def main(): 

	# Command line args are in sys.argv[1], sys.argv[2] .. 
	# sys.argv[0] is the script name itself and can be ignored 
	# parse arguments 
	parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

	# add arguments 
	parser.add_argument('--grid-size', dest='N', required=False) 
	parser.add_argument('--mov-file', dest='movfile', required=False) 
	parser.add_argument('--interval', dest='interval', required=False)
	parser.add_argument('--glider', action='store_true', required=False)
	parser.add_argument('--still_life_block', action='store_true', required=False)
	parser.add_argument('--oscillator_blinker', action='store_true', required=False)
	parser.add_argument('--spaceship_glider', action='store_true', required=False)
	parser.add_argument('--methuselah_r_pentomino', action='store_true', required=False)
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
	elif args.still_life_block:
		grid = np.zeros(N * N).reshape(N, N)
		addStillLifeBlock(5, 5, grid)  # Adjust position as needed
	elif args.oscillator_blinker:
		grid = np.zeros(N * N).reshape(N, N)
		addOscillatorBlinker(5, 5, grid)  # Adjust position as needed
	elif args.spaceship_glider:
		grid = np.zeros(N * N).reshape(N, N)
		addSpaceshipGlider(5, 5, grid)  # Adjust position as needed
	elif args.methuselah_r_pentomino:
		grid = np.zeros(N * N).reshape(N, N)
		addMethuselahRpentomino(5, 5, grid)  # Adjust position as needed
# Add more conditions for other patterns as needed

	else: # populate grid with random on/off - 
			# more off than on 
		grid = randomGrid(N) 

	# set up animation 
	fig, ax = plt.subplots() 
	img = ax.imshow(grid, interpolation='nearest') 
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), 
								frames = 10, 
								interval=updateInterval, 
								save_count=50) 

	# # of frames? 
	# set output file 
	if args.movfile: 
		ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 

	plt.show() 

# call main 
if __name__ == '__main__': 
	main() 
