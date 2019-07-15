import ast
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
        self.children = 0

        self.closed = False
        self.visited = False

    # to make sure to see what instance has
    def __repr__(self):
        return repr((self.pos, self.f, self.g, self.h, self.parent, self.parent_pos, self.children, self.closed))


def location_of_obstacle(maze):  # to know where are obstacles
    obstacle = []
    for idx1, val1 in enumerate(maze):
        for idx2, val2 in enumerate(val1):
            if val2 == 1:
                obstacle.append((idx1, idx2))
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
                return agent, target


# #######################################################################################################
#    The problem is that how to set start and end positions. Our map is changed barriors every time.
#########################################################################################################
def main():
    # Call main func of gridMaker script. Overwrites all previous instances in 'mazes' up to gridMaker.NUM_MAZES
    gridMaker.main()

    # Loads mazes in mazes directory
    for fileName in os.listdir("mazes\\"):
        print(fileName)
        # Opens first maze file
        with open(('mazes\\' + fileName), 'r') as file:
            # Gets grid in string form
            grid_str = file.readline()
            # converts string to list of lists
            grid = ast.literal_eval(grid_str)
            # Generate agent/target for grid
            start, end = random_coordinates(grid)
            '''
            Testing for Opened list & closed List
            '''
            opened_list = []
            closed_list = []
            temp_blocked_path = []

            # first node
            root = Node(start)
            # root.h = heuristic(start, end)  # just test heuristic func - > works!
            opened_list.append(root)
            # print(opened_list)
            # closed_list.append(root)
            tmp_cnt_open_list = 0
            # print(len_openList)

            while opened_list is not None:
                '''
                process first node, which is start node
                '''
                # print(opened_list)
                current_node = opened_list.pop()
                # print(current_node)
                closed_list.append(current_node)
                current_node.closed = True

                ### New added
                checking_node = None
                if len(closed_list) > 2:
                    checking_node = closed_list.pop()
                if current_node.parent is checking_node.parent:
                    continue
                else:
                    closed_list.append(checking_node)

                if opened_list is None:
                    print("can't reach to the target!")


                # print(closed_list)
                # to avoid obstacles added in opened list
                get_obstacle_location = location_of_obstacle(grid)
                # print(get_obstacle_location)

                if current_node.pos == end:  # if this node pos is same as end position, we get it. it's destination
                    # print(closed_list)
                    # later I will set list or tuple to return pos of instance
                    # print(getClosedListMemberPos(closed_list))
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

                        not_path = is_visited(temp_blocked_path)
                        if available in not_path:
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
                        new_neighbor.parent_pos.append(current_node.pos)
                        # print(new_neighbor.parent_pos)
                        opened_list.append(new_neighbor)
                        '''
                        h = heuristic(available, end)
                        f = h + G_VALUE
                        # g value is always 1
                        new_neighbor = Node(available, f, G_VALUE, h, current_node)
                        new_neighbor.visited = True
                        opened_list.append(new_neighbor)
                        '''
                        # to prepare if this path will be blocked
                        tmp_cnt_open_list += 1
                    current_node.children = tmp_cnt_open_list  # may not need it
                    # print(opened_list)    # expected [ ((1,0), 11, 10, 1, ( (0,0), 0, 0, 0, None, Ture), False) ]  -> ok!

                    # current_node = neighbor_nodes  -> nope!
                    # reverse sort because I want to use pop func to move to closed list
                    opened_list = sorted(opened_list, key=lambda obj: obj.f, reverse=True)

                    # compare between length of lists so if it opened list is larger than there is no more path
                    if tmp_cnt_open_list < 1:  # no more to go.. We need to go back until find new path
                        tmp = current_node
                        tmp.closed = False
                        temp_blocked_path.append(tmp)
                        for i in closed_list:
                            if i is current_node:
                                # print(i)
                                closed_list.remove(i)

                        current_node = current_node.parent  # go back to parent
                    opened_list = sorted(opened_list, key=lambda obj: obj.f,
                                        reverse=True)  # reverse sort because I want to use pop func to move to closed list
                    opened_list = sorted(opened_list, key=lambda obj: obj.g, reverse=True)
                # break   # for testing break here temporarily

            result_path = get_closed_list_member_pos(closed_list)
            print(result_path)
            r = ret_f_value(closed_list)
            print(r)



            cmap = pyplot.cm.binary
            cmap.set_bad(color='blue')

            pyplot.imshow(grid, interpolation='none', cmap=cmap)
            pyplot.scatter([v[1] for v in result_path], [v[0] for v in result_path])
            pyplot.grid(b=True, which='both', axis='both')

            rax = pyplot.axes([0.02, 0.7, 0.15, 0.15])
            radio = wi.RadioButtons(rax, ('Foward', 'Backward', '???'))
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
