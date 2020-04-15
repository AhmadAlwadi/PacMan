# ALL THE PATHFINDING ALGORITHM CODE SHOULD GO HERE 
class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def AStarAlgo(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
	# Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

	# Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

	# Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

	    # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
    
        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

			# Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
# END OF THE PATHFINDING ALFORITHM
walls = []
f = open("Pixels.txt", "r")
if f.mode == 'r':
    walls.append(f.read())
start = (330, 270)
end = (287, 439)

print(AStarAlgo(walls, start, end))

'''Walls:
"Walls":[
        [0,0,6,600],
        [0,0,600,6],
        [0,600,606,6],
        [600,0,6,606],
        [300,0,6,66],
        [60,60,186,6],
        [360,60,186,6],
        [60,120,66,6],
        [60,120,6,126],
        [180,120,246,6],
        [300,120,6,66],
        [480,120,66,6],
      	[540,120,6,126],
      	[120,180,126,6],
      	[120,180,6,126],
      	[360,180,126,6],
      	[480,180,6,126],
      	[180,240,6,126],
      	[180,360,246,6],
      	[420,240,6,126],
      	[240,240,42,6],
      	[324,240,42,6],
      	[240,240,6,66],
      	[240,300,126,6],
      	[360,240,6,66],
      	[0,300,66,6],
      	[540,300,66,6],
      	[60,360,66,6],
      	[60,360,6,186],
      	[480,360,66,6],
      	[540,360,6,186],
      	[120,420,366,6],
      	[120,420,6,66],
      	[480,420,6,66],
      	[180,480,246,6],
      	[300,480,6,66],
      	[120,540,126,6],
      	[360,540,126,6]
      	]
'''

































