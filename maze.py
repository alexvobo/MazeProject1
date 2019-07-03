from matplotlib import colors, pyplot
from random import randrange
import numpy as np

gridSize = 100

def obstacleFxn():
    obstacles = [0,1]
    probabilities = [0.7, 0.3]
    return np.random.choice(obstacles, 1, p=probabilities)[0]


def makeMaze():
    grid = [[obstacleFxn() for _ in range(gridSize)] for _ in range(gridSize)]
    for x in grid:
        print(x)
    return grid

data = makeMaze()

# create colormap
cmap = pyplot.cm.binary
cmap.set_bad(color='black')

pyplot.imshow(data, interpolation='none', cmap=cmap)
pyplot.show()