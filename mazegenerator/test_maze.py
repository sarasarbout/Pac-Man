from mazegenerator import MazeGenerator

generator = MazeGenerator()

print("Maze:")
for row in generator.maze:
    print(row)

print("Entry:", generator.maze_entry)
print("Exit:", generator.maze_exit)
print("Shortest path:", generator.shortest_path)