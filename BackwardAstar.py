from Astar_map import Map
from matplotlib import pyplot
from collections import OrderedDict
from itertools import repeat


# just test for range of map
MAX_X = 4
MAX_Y = 4

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

'''
mapData = Map()
map = mapData.make_maze()
'''

map = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
    ]
'''
# just test map
map = [
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0]
    ]
'''


def location_of_obstacle(maze):    #to know where are obstacles
    obstacle = []
    for idx1, val1 in enumerate(maze):
        for idx2, val2 in enumerate(val1):
            if val2 == 1:
                obstacle.append((idx1, idx2))
    return obstacle

# using matplotlib, drawing distance
def getClosedListMemberPos(closedList):
    closedPos = []
    for p in closedList:
        if p.closed is True:
            closedPos.append(p.pos)
    return closedPos

def isVisited(openedList):
    openedPos = []
    for p in openedList:
        openedPos.append(p.pos)
    return openedPos

def heuristic(start, end):
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    return x + y

def ret_f_value(closedList):
    total = 0
    for i in closedList:
        total += i.f
    return total


# #######################################################################################################
#    The problem is that how to set start and end positions. Our map is changed barriors every time.
#########################################################################################################
start = (4,2)
end = (4,4)

'''
Testing for Opened list & closed List
'''
openedList = []
closedList = []

#first node
root = Node(start)
root.h = heuristic(start, end)  # just   test heuristic func - > works!
root.f = root.h
root.p_pos = start
openedList.append(root)
# print(openedList)
# closedList.append(root)

# print(len_openList)
end_Node = Node(end)
back_tracking = []
tmp_cnt_openList =1
current_node = None
getObstacleLocation = location_of_obstacle(map)

def backward(start, end, openedList, closedList, end_Node, back_tracking, tmp_cnt_openList, current_node, getObstacleLocation):
    while openedList is not None:
        '''
        process first node, which is start node
        '''
        if tmp_cnt_openList < 1:  # no more to go.. We need to go back until find new path
            back_tracking.append(current_node.pos)
           # closedList.remove(current_node)
            current_node = current_node.parent
        else:
            current_node = openedList.pop()
            closedList.append(current_node)
            current_node.closed = True

        # print(openedList)
        # print(current_node)
        # print(closedList)
        # to avoid obstacles added in opened list

        # print(getObstacleLocation)

        if current_node.pos == end:     # if this node pos is same as end position, we get it. it's destination
            end_Node.g = current_node.g
            end_Node.f = end_Node.g
            tmp = current_node.parent
            current_node.p_pos = tmp.pos
            break
        else:
            '''
                for searching available path (up, down, left, right)
            '''
            #print(len_openList)
            tmp_cnt_openList = 0
            for available in [(current_node.pos[0]+1, current_node.pos[1]),
                              (current_node.pos[0], current_node.pos[1]+1),
                              (current_node.pos[0]-1, current_node.pos[1]),
                              (current_node.pos[0], current_node.pos[1]-1)]:

                # if out of map, just skip it
                if available[0] < 0 or available[1] < 0 or available[0] > MAX_X or available[1] > MAX_Y:
                    continue

                # if obstacle, skip
                if available in getObstacleLocation:
                    current_node.g = heuristic(current_node.pos, start)
                    current_node.h = 0
                    current_node.f = current_node.g + current_node.h
                    continue

                # if node is in closed List, then skip it
                ret = getClosedListMemberPos(closedList)
                if available in ret:
                    continue

                '''
                # if node is already in the opened list, then skip it
                is_visited = isVisited(openedList)
                if available in is_visited:
                    continue
                '''
                if available in back_tracking:
                    continue

                # h = 0
                # backward = available , start
                # frontward = available , end
                h = heuristic(end, available)
                g = G_VALUE + current_node.g
                f = g + h
                '''
                h = heuristic(start, available)
                tmp_g = heuristic(end, available)
                g = tmp_g - G_VALUE
                # g = G_VALUE
                f = g + h
                '''
                new_neighbor = Node(available, f, g, h, current_node)
                new_neighbor.visited = True
                new_neighbor.p_pos = current_node.pos
                #end_Node.p_pos = current_node.pos
                openedList.append(new_neighbor)

                # to prepare if this path will be blocked, count children
                tmp_cnt_openList += 1

            # print(openedList)    # expected [ ((1,0), 11, 10, 1, ( (0,0), 0, 0, 0, None, Ture), False) ]  -> ok!

            # current_node = neighbor_nodes  -> nope!
            openedList = sorted(openedList, key=lambda obj: obj.f, reverse=True)  # reverse sort because I want to use pop func to move to closed list



           # break   # for testing break here temporarily


    last_node = closedList[-1]
    print(last_node.f, " ", last_node.g, " ", last_node.h)
    #print(last_node)
    last_list = []
    last_list.append(last_node.pos)
    parent = last_node.parent
    last_list.append(parent.pos)
    print(parent.f, " ", parent.g, " ", parent.h)
    #print(parent)
    while True:
        parent = parent.parent
        last_list.append(parent.pos)
        print(parent.f, " ", parent.g, " ", parent.h)
        if parent.pos == start:
            break
    #print(last_list)
    last_list.reverse()
    #print(last_list)



    cmap = pyplot.cm.binary
    cmap.set_bad(color='blue')
    pyplot.imshow(map, interpolation='none', cmap=cmap)
    pyplot.plot([v[1] for v in last_list], [v[0] for v in last_list])
    pyplot.grid(b=True, which='both', axis='both')

    pyplot.show()

backward(start, end, openedList, closedList, end_Node, back_tracking, tmp_cnt_openList, current_node, getObstacleLocation)
