import ast
import math
import os

import Astar_map as gridMaker
from matplotlib import pyplot as pyplot
from matplotlib import widgets as wi
from random import randrange

# RANGES FOR GRID, SHOULD BE 101.
# Adjust size of grid in Astar_map file.
MAX_X = MAX_Y = gridMaker.GRID_SIZE

G_VALUE = 1


class Node:
    def __init__(self, pos, f=0, g=0, h=0, parent=None):
        self.pos = pos  # type is tuple

        self.f = f
        self.g = g
        self.h = h

        self.parent = parent
        self.parent_pos = []  # may not need

        self.closed = False
        self.visited = False

    # to make sure to see what instance has
    '''
    def __repr__(self):
        return repr((self.pos, self.f, self.g, self.h, self.parent, self.parent_pos, self.closed))
    '''

def location_of_obstacle(maze):  # to know where are obstacles
    obstacle = []
    for row_i, row in enumerate(maze):
        for col_i, item in enumerate(row):
            if maze[row_i][col_i] == 1:
                obstacle.append((row_i, col_i))
    return obstacle


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
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    return x + y


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
            if grid[agent[0]][agent[1]] != 1 and grid[target[0]][target[1]] != 1:
                print(grid[agent[0]][agent[1]])
                print(grid[target[0]][target[1]])
                print('a= ',agent)
                print('t= ', target)
                return agent, target


# #######################################################################################################
#    The problem is that how to set start and end positions. Our map is changed barriors every time.
#########################################################################################################
def main():
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
            #print('a=',start)
            #print('t=', end)

            '''
                open list should be priority queue(extra points)
            '''
            opened_list = []
            closed_list = []

            # first node
            root = Node(start)
            root.h = heuristic(start, end)
            root.f = root
            root.parent_pos = start
            opened_list.append(root)

            tmp_cnt_open_list = 0
            # print(len_openList)
            # to avoid obstacles added in opened list
            get_obstacle_location = location_of_obstacle(grid)
            back_tracking = []
            while opened_list != []:
                '''
                process first node, which is start node
                '''
                # print(opened_list)
                current_node = opened_list.pop()
                print("HERE",current_node)
                closed_list.append(current_node)
                current_node.closed = True


                if opened_list is None:
                    print("can't reach to the target!")


                # print(closed_list)

                # print(get_obstacle_location)

                if current_node.pos == end:  # if this node pos is same as end position, we get it. it's destination
                    # print(closed_list)
                    prev_parent = current_node.parent
                    current_node.g = prev_parent.g + G_VALUE
                    current_node.h = 0
                    current_node.f = current_node.g
                    break
                else:
                    '''
                        for searching available path (up, down, left, right)
                    '''
                    # print(len_openList)
                    tmp_cnt_open_list = 0
                    for available in [(current_node.pos[0] + 1, current_node.pos[1]),
                                      (current_node.pos[0], current_node.pos[1] + 1),
                                      (current_node.pos[0] - 1, current_node.pos[1]),
                                      (current_node.pos[0], current_node.pos[1] - 1)]:

                        # if out of map, just skip it
                        if available[0] < 0 or available[1] < 0 or available[0] > MAX_X or available[1] > MAX_Y:
                            continue

                        # if obstacle, skip
                        if available in get_obstacle_location:
                            continue

                        # if node is in closed List, then skip it
                        ret = get_closed_list_member_pos(closed_list)
                        if available in ret:
                            continue

                        # if node is already in the opened list, then skip it
                        visited = is_visited(opened_list)
                        if available in visited:
                            continue

                        if available in back_tracking:
                            # print(back_tracking)
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
                        new_neighbor.parent_pos = current_node.pos
                        # print(new_neighbor.parent_pos)
                        opened_list.append(new_neighbor)

                        # to prepare if this path will be blocked
                        tmp_cnt_open_list += 1
                    # print(opened_list)    # expected [ ((1,0), 11, 10, 1, ( (0,0), 0, 0, 0, None, Ture), False) ]  -> ok!

                    # current_node = neighbor_nodes  -> nope!
                    # reverse sort because I want to use pop func to move to closed list

                    # compare between length of lists so if it opened list is larger than there is no more path
                    if tmp_cnt_open_list < 1:  # no more to go.. We need to go back until find new path
                        back_tracking.append(current_node.pos)
                        current_node = current_node.parent  # go back to parent

                    opened_list = sorted(opened_list, key=lambda obj: obj.f, reverse=True)  # reverse sort because I want to use pop func to move to closed list
                    ## have to fix little bit more
                    #opened_list = sorted(opened_list, key=lambda obj: obj.g, reverse=True)
                # break   # for testing break here temporarily

           # result_path = get_closed_list_member_pos(closed_list)
            #print(result_path)
            #r = ret_f_value(closed_list)
            #print(r)
            lst = []
            for i in closed_list:
                lst.append(i.parent_pos)
            # print(i.p_pos)
            # print(len(closed_list))
            # list(OrderedDict.fromkeys(lst))   -> Not work!
            print(lst)
            lst.append(end)


            cmap = pyplot.cm.binary
            #cmap.set_bad(color='red')

            pyplot.imshow(grid, interpolation='none', cmap=cmap, aspect = 1,animated= True)
            pyplot.scatter([v[0] for v in lst], [v[1] for v in lst])
            print('a=', start)
            print('t=', end)
            pyplot.plot(start[0],start[1], 'r+')
            pyplot.annotate("A", start)
            pyplot.annotate("T", end)
            pyplot.plot(end[0],end[1], 'g+')
            pyplot.plot([v[0] for v in lst], [v[1] for v in lst])

            #pyplot.grid(b=False, which='both', axis='both')

            #rax = pyplot.axes([0.02, 0.7, 0.15, 0.15])
            #radio = wi.RadioButtons(rax, ('Foward', 'Backward', '???'))
            '''
            def foward(sth_here):
                sth sth sth sth 
                plt.draw()
            radio.on_clicked(forward)
            '''
            pyplot.show()

            for x in grid:
                print(x)



if __name__ == '__main__':
    main()

'''
########################## Note ############################################################################
# 1 Diagonol problem on map if I use line: I know I set if visited then no more visited. NEED TO FIX IT.
    -+-+-> temporarily solved to use scatter instead of plot
# 2 Start and end position : search if I can use input UI in pyplot back ground to get start and end points
#############################################################################################################
'''
