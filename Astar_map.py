import numpy as np
import os

# GRID_SIZE should match MAX_X, MAX_Y in
GRID_SIZE = 10  # 101
NUM_MAZES = 5  # 50


class Map:
    def __init__(self):
        self.obstacles = [0, 1]
        self.probabilities = [0.7, 0.3]

    # Given a probability, generates a 0 or a 1
    def create_obstacle_randomly(self):
        return np.random.choice(self.obstacles, 1, p=self.probabilities)[0]

    # Creates a GRID_SIZE x GRID_SIZE maze of 0,1 using discrete obstacle function
    def make_maze(self):
        grid = [[self.create_obstacle_randomly() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # for x in grid:
        #     print(x)
        return grid


def main():
    # Check if mazes folder exists. If not, create it.
    if not os.path.exists('mazes'):
        os.makedirs('mazes')

    # Creates NUM_MAZES mazes and saves them in mazes directory
    for i in range(NUM_MAZES):
        map_obj = Map()
        with open(('mazes\\maze_' + str(i) + '.txt'), 'w') as file:
            file.write(str(map_obj.make_maze()))


# Run this before running plan.py
if __name__ == '__main__':
    main()
