from mazegenerator import MazeGenerator


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


def print_maze(grid):
    height = len(grid)
    width = len(grid[0])

    # Top border
    for y in range(height):
        # Print north walls
        for x in range(width):
            if grid[y][x] & NORTH:
                print("+---", end="")
            else:
                print("+   ", end="")
        print("+")

        # Print west/east walls + cell content
        for x in range(width):
            if grid[y][x] & WEST:
                print("|", end="")
            else:
                print(" ", end="")

            print("   ", end="")

        # Right wall of the last cell
        if grid[y][width - 1] & EAST:
            print("|")
        else:
            print("")

    # Bottom border
    for x in range(width):
        if grid[height - 1][x] & SOUTH:
            print("+---", end="")
        else:
            print("+   ", end="")

    print("+")


# ====== Test =======

generator = MazeGenerator()

print_maze(generator.maze)