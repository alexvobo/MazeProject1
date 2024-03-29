import ast
import Astar_map as gridMaker
from matplotlib import pyplot
from random import randrange
import os
import psutil
import time

# RANGES FOR GRID, SHOULD BE 101.
# Adjust size of grid in Astar_map file.
MAX_X = MAX_Y = gridMaker.GRID_SIZE

G_VALUE = 1


class Node:
    def __init__(self, pos, f = 0, g =0, h =0, parent = None):
        self.pos = pos   # type is tuple

        self.f = f
        self.g = g
        self.h = h

        self.parent = parent
        self.p_pos = []
        self.closed = False
        self.visited = False

    # to make sure to see what instance has
    def __repr__(self):
        return repr((self.pos, self.f, self.h, self.g, self.parent, self.closed))


# def location_of_obstacle(maze):  # to know where are obstacles
#     obstacle = []
#     for row_i, row in enumerate(maze):
#         for col_i, item in enumerate(row):
#             if maze[row_i][col_i] == 1:
#                 obstacle.append((col_i, row_i))
#     return obstacle


# using matplotlib, drawing distance
def get_closed_list_member_pos(closed_list):
    closed_pos = []
    for p in closed_list:
        if p.closed is True:
            closed_pos.append(p.pos)
    return closed_pos


def is_visited(opened_list):
    opened_pos = []
    for p in opened_list:
        opened_pos.append(p.pos)
    return opened_pos


def heuristic(start, end):
    (x1, y1) = start
    (x2, y2) = end
    return abs(x1 - x2) + abs(y1 - y2)


def ret_f_value(closed_list):
    total = 0
    for i in closed_list:
        total += i.f
    return total


# Creates random pairs of numbers for randomizing location of agent/target
def random_coordinates(grid):
    while True:
        agent = (randrange(MAX_X), randrange(MAX_Y))
        target = (randrange(MAX_X), randrange(MAX_Y))
        # loop terminates when agent and target do not have the same values.
        if agent != target:
            # create another pair of coordinates if agent/target land on an obstacle
            if grid[agent[1]][agent[0]] != 1 and grid[target[1]][target[0]] != 1:
                print(grid[agent[0]][agent[1]])
                print(grid[target[0]][target[1]])
                print('a= ', agent)
                print('t= ', target)
                return agent, target


def main():
    # To check how much memory used
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    t1 = time.perf_counter()

    # Call main func of gridMaker script. Overwrites all previous instances in 'mazes' up to gridMaker.NUM_MAZES
    gridMaker.main()
    path = 'mazes'
    # Loads mazes in mazes directory
    for fileName in os.listdir(path):
        print(fileName)
        # Opens first maze file
        with open(os.path.join(path, fileName), 'r') as file:
            # Gets grid in string form
            grid_str = file.readline()
            # converts string to list of lists
            grid = ast.literal_eval(grid_str)
            # Generate agent/target for grid
            start, end = random_coordinates(grid)
            # start = (76, 21)
            # end = (47, 98)

            '''
                open list should be priority queue(extra points)
            '''
            opened_list = []
            closed_list = []

            # first node
            root = Node(start)
            root.h = heuristic(start, end)  # just test heuristic func - > works!
            root.f = root.h
            root.p_pos = start
            opened_list.append(root)

            end_Node = Node(end)
            back_tracking = []
            tmp_cnt_openList = 1
            current_node = None
            cnt = 0
            while opened_list is not None:
                '''
                process first node, which is start node
                '''
                if tmp_cnt_openList < 1:  # no more to go.. We need to go back until find new path
                    back_tracking.append(current_node.pos)
                    grid[current_node.pos[1]][current_node.pos[0]] = 2
                    current_node = current_node.parent
                else:
                    current_node = opened_list.pop()
                    closed_list.append(current_node)
                    current_node.closed = True
                    cnt+=1

                if opened_list is []:
                    print("can't reach to the target!")
                    continue

                if current_node.pos == end:  # if this node pos is same as end position, we get it. it's destination
                    break
                else:
                    '''
                        for searching available path (up, down, left, right)
                    '''
                    # print(len_openList)
                    tmp_cnt_openList = 0
                    for available in [(current_node.pos[0] + 1, current_node.pos[1]),
                                      (current_node.pos[0], current_node.pos[1] + 1),
                                      (current_node.pos[0] - 1, current_node.pos[1]),
                                      (current_node.pos[0], current_node.pos[1] - 1)]:

                        # if out of map, just skip it
                        if available[0] < 0 or available[1] < 0 or available[1] >= MAX_X or available[0] >= MAX_Y:
                            continue

                        # if obstacle, skip
                        if grid[available[1]][available[0]] == 1:
                            current_node.g = 0
                            current_node.h = heuristic(current_node.pos, end)
                            current_node.f = current_node.g + current_node.h
                            continue

                        # if node is in closed List, then skip it
                        ret = get_closed_list_member_pos(closed_list)

                        if available in back_tracking:
                            #print("HERE")
                            continue

                        if available in ret:
                            continue



                        # backward = available , start
                        # frontward = available , end
                        h = heuristic(end, available)
                        # print(tmp_end_h)
                        g = G_VALUE + current_node.g
                        f = g + h
                        # ** g value will be cumulative
                        new_neighbor = Node(available, f, g, h, current_node)
                        new_neighbor.visited = True
                        new_neighbor.p_pos = current_node.pos  # may not needed

                        opened_list.append(new_neighbor)

                        # to prepare if this path will be blocked
                        tmp_cnt_openList += 1

                    # reverse sort because I want to use pop func to move to closed list
                    opened_list = sorted(opened_list, key=lambda obj: (obj.f, -obj.g), reverse=True)
            t2 = time.perf_counter()
            # To check how much memory used
            mem_after = process.memory_info().rss / 1024 / 1024
            total_time = t2 - t1
            print("Before memory: {}MB".format(mem_before))
            print("After memory: {}MB".format(mem_after))
            print("Total time: {}second".format(total_time))
            print("Total expanded: ", cnt)
            last_node = closed_list[-1]
            last_list = []
            last_list.append(last_node.pos)
            parent = last_node.parent
            last_list.append(parent.pos)

            while True:
                parent = parent.parent
                last_list.append(parent.pos)
                if parent.pos == start:
                    break

            last_list.reverse()
            #print(last_list)
            result_path = get_closed_list_member_pos(closed_list)
            #print(result_path)

            cmap = pyplot.cm.binary

            #print("HERE", back_tracking)
            pyplot.imshow(grid, interpolation='none', cmap=cmap, aspect=1, animated=True)

            pyplot.scatter([v[0] for v in result_path], [v[1] for v in result_path], marker=".", edgecolors='red')
            #print('a=', start)
            #print('t=', end)
            pyplot.plot(start[0], start[1], 'r+')
            pyplot.annotate("A", start)
            pyplot.annotate("T", end)
            pyplot.plot(end[0], end[1], 'g+')
            pyplot.plot([v[0] for v in last_list], [v[1] for v in last_list], marker=".")

            pyplot.show()



if __name__ == '__main__':
    main()
