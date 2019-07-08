# just test for range of map
MAX_X = 10
MAX_Y = 10
G_VALUE = 1

class Node:
    def __init__(self, pos, f = 0, g =0, h =0, parent = None):
        self.pos = pos   # type is tuple

        self.f = f
        self.g = g
        self.h = h
        self.parent = parent
        self.closed = False
        self.visited = False

    def __repr__(self):
        return repr((self.pos, self.f, self.h, self.g, self.parent, self.closed))


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


start = (0,0)
end = (2,9)

'''
Testing for Opened list & closed List
'''
openedList = []
closedList = []

#first node
root = Node(start)
# root.h = heuristic(start, end)  # just test heuristic func - > works!
openedList.append(root)
# print(openedList)
# closedList.append(root)
tmp_cnt_openList = 0
# print(len_openList)

while openedList is not None:
    '''
    process first node, which is start node
    '''
    # print(openedList)
    current_node = openedList.pop()
    # print(current_node)
    closedList.append(current_node)
    current_node.closed = True
    # print(closedList)

    # to avoid obstacles added in opened list
    getObstacleLocation = location_of_obstacle(map)
    # print(getObstacleLocation)

    if current_node.pos == end:     # if this node pos is same as end position, we get it. it's destination
        # print(closedList)
        # later I will set list or tuple to return pos of instance
        #print(getClosedListMemberPos(closedList))
        break
    else:
        '''
            for searching available path (up, down, left, right)
        '''
        #print(len_openList)
        tmp_cnt_openList = 0
        for available  in [(current_node.pos[0]+1, current_node.pos[1]),
                          (current_node.pos[0], current_node.pos[1]+1),
                          (current_node.pos[0]-1, current_node.pos[1]),
                          (current_node.pos[0], current_node.pos[1]-1)]:

            # if out of map, just skip it
            if available[0] < 0 or available[1] < 0 or available[0] > MAX_X or available[1] > MAX_Y:
                continue

            # if obstacle, skip
            if available in getObstacleLocation:
                continue

            # if node is in closed List, then skip it
            ret = getClosedListMemberPos(closedList)
            if available in ret:
                continue

            # if node is already in the opened list, then skip it
            is_visited = isVisited(openedList)
            if available in is_visited:
                continue


            h = heuristic(available, end)
            f = h+1
            # g value is always 1
            new_neighbor = Node(available, f, G_VALUE, h, current_node)
            new_neighbor.visited = True
            openedList.append(new_neighbor)

            # to prepare if this path will be blocked
            tmp_cnt_openList += 1

        # print(openedList)    # expected [ ((1,0), 11, 10, 1, ( (0,0), 0, 0, 0, None, Ture), False) ]  -> ok!

        # current_node = neighbor_nodes  -> nope!
        openedList = sorted(openedList, key=lambda obj: obj.f, reverse=True)  # reverse sort because I want to use pop func to move to closed list

        # compare between length of lists so if it opened list is larger than there is no more path

        if tmp_cnt_openList < 1:   # no more to go.. We need to go back until find new path
            current_node = current_node.parent  # go back to parent
            # do sth here not visited


       # break   # for testing break here temporarily

result_path = getClosedListMemberPos(closedList)
print(result_path)




