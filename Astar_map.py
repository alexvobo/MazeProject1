from matplotlib import pyplot as pyplot
from random import randrange
import numpy as np

GRIDSIZE = 50

class Map:
    def __init__(self):
        self.obstacles = [0,1]
        self.probabilities = [0.7, 0.3]

    def create_obstacle_randomly(self):
        return np.random.choice(self.obstacles, 1, p=self.probabilities)[0]

    def makeMaze(self):
        grid = [[self.create_obstacle_randomly() for _ in range(GRIDSIZE)] for _ in range(GRIDSIZE)]
        for x in grid:
            print(x)

        return grid



'''
data1 = Map()
data = data1.makeMaze()

cmap = pyplot.cm.binary
cmap.set_bad(color='blue')

pyplot.imshow(data, interpolation='none', cmap=cmap)
pyplot.xlim(0,100)
pyplot.ylim(0,100)
pyplot.grid(b=True, which='both', axis='both')
pyplot.show()
'''