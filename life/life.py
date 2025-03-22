import random
from PIL import Image

# Size of the grid
GRID_SIZE = 32

# random chance to toggle alive
toggle_alive_chance = 0.005

def create_grid():
    """Creates a 32x32 grid with random initial alive (True) or dead (False) cells."""
    return [[random.choice([True, False]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def count_neighbors(grid, x, y):
    """Counts the number of live neighbors around a given cell (x, y)."""
    neighbors = 0
    for i in range(-1, 2):  # Iterate over a 3x3 area around the cell
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            nx, ny = x + i, y + j
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:  # Ensure coordinates are within bounds
                neighbors += grid[nx][ny]
    return neighbors

def next_generation(grid):
    """Generates the next generation of the grid based on the rules of the game."""
    new_grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = count_neighbors(grid, x, y)
            if grid[x][y]:
                # Any live cell with 2 or 3 neighbors stays alive; otherwise, it dies
                new_grid[x][y] = neighbors == 2 or neighbors == 3
            else:
                # Any dead cell with exactly 3 neighbors becomes alive
                new_grid[x][y] = neighbors == 3
            # small random chance to become alive or die
            if random.random() < toggle_alive_chance:
                if y - 1 >= 0:
                    grid[x][y-1] = True
                if y + 1 < 32:
                    grid[x][y-1] = True
                if x - 1 >= 0:
                    grid[x-1][y] = True
                if x + 1 < 32:
                    grid[x+1][y] = True
                grid[x][y] = True
    return new_grid

def count_living_neighbors(grid, x, y):
    """Counts the number of living (True) neighbors around a cell at position (x, y)."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            count += grid[nx][ny]
    return count

def render_grid_to_png(grid, filename="grid.png"):
    """Renders the grid as a PNG image where alive cells are green and dead cells are black."""
    img = Image.new("RGB", (GRID_SIZE, GRID_SIZE))  # Create a new RGB image (24-bit pixels)
    pixels = img.load()  # Access the pixel data

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            living_neighbors = count_living_neighbors(grid, x, y)
            if grid[x][y]:
                color = (0, int(living_neighbors * (255/3)), 0)  # Green for alive cells
            else:
                color = (0, int(living_neighbors * (255/6)), 0)  # Black for dead cells
            pixels[x, y] = color

    img.save(filename)  # Save the image as a PNG file
    print(f"Image saved as {filename}")

def get_next_generation(grid=None):
    """
    If no grid is provided, create a random grid.
    Otherwise, compute and return the next generation from the provided grid.
    """
    if grid is None:
        grid = create_grid()  # If no grid is passed, initialize one randomly
    
    return next_generation(grid)

