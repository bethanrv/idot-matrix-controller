from PIL import Image
import random

GRID_SIZE = 32
STARTING_PARTICLES = 7
PARTICLES = []
SPEED = 1

def rand_neg():
	if random.random() > 0.5:
		return -1
	return 1

def rand_color():
	return (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

def add_starting_particles(grid):
	for i in range(0, STARTING_PARTICLES):
		rand_x = int(random.random() * GRID_SIZE)
		rand_y = int(random.random() * GRID_SIZE)
		PARTICLES.append({
			'x' : rand_x,
			'y' : rand_y,
			'vx': SPEED * rand_neg() * 1,
			'vy': SPEED * rand_neg() * 1,
			'color' : rand_color()
		})
		grid[rand_x][rand_y] = True
	return grid

def create_grid():
    """Creates a 32x32 grid of false cells."""
    grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grid = add_starting_particles(grid)
    return grid

def move(grid):
	for particle in PARTICLES:
		grid[particle['x']][particle['y']] = False
		particle['x'] += particle['vx']
		particle['y'] += particle['vy']
		if particle['x'] <= 0:
			particle['x'] = 0
			particle['vx'] = -1 * particle['vx']
		elif particle['x'] >= GRID_SIZE - 1:
			particle['x'] = GRID_SIZE - 1
			particle['vx'] = -1 * particle['vx']
		if particle['y'] <= 0:
			particle['y'] = 0
			particle['vy'] = -1 * particle['vy']
		elif particle['y'] >= GRID_SIZE - 1:
			particle['y'] = GRID_SIZE - 1
			particle['vy'] = -1 * particle['vy']
		particle['x'] = int(particle['x'])
		particle['y'] = int(particle['y'])
		grid[particle['x']][particle['y']] = True
	return grid

def render_grid_to_png(grid, filename="grid.png"):
    """Renders the grid as a PNG image"""
    grid = move(grid)
    img = Image.new("RGB", (GRID_SIZE, GRID_SIZE))  # Create a new RGB image (24-bit pixels)
    pixels = img.load()  # Access the pixel data

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = (0, 0, 0)
            pixels[x, y] = color

    for particle in PARTICLES:
    	pixels[particle['x'], particle['y']] = particle['color']

    img.save(filename)  # Save the image as a PNG file
    print(f"Image saved as {filename}")