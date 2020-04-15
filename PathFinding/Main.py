import queue
# Make maze
StartCoord = (0, 0)
def MakeMaze():
	global StartCoord
	Maze = [[' ' for i in range(606)] for j in range(606)]
	start = (400, 270)
	StartCoord = start
	end = (287, 439)

	Maze[start[0]][start[1]] = "O"
	Maze[end[0]][end[1]] = "X"

	Barriers = [
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

	x1, x2, y1, y2 = 0, 0, 0, 0
	for z in Barriers:
			x1, y1, x2, y2 = z[0], z[1], z[2], z[3]
			for i in range(x1, x2):
				for j in range(y1, y2):
					Maze[i][j] = '#'
	return Maze

def printMaze(maze, path=""):
    print('printing maze')
    for x, pos in enumerate(maze[StartCoord]):
        if pos == "O":
            start = x

    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))
    
    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(col + " ", end="")
        print()
        


def valid(maze, moves):
	global StartCoord
	for x, pos in enumerate(maze[StartCoord[0]]):
		if pos == "O":
			start = x

	i = start
	j = 0
	for move in moves:
		if move == "L":
			i -= 1

		elif move == "R":
			i += 1

		elif move == "U":
			j -= 1

		elif move == "D":
			j += 1

		if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
			return False
		elif (maze[j][i] == "#"):
			return False

	return True


def findEnd(maze, moves):
	global StartCoord
	for x, pos in enumerate(maze[StartCoord[0]]):
		if pos == "O":
			start = x

	i = start
	j = 0
	for move in moves:
		if move == "L":
			i -= 1

		elif move == "R":
			i += 1

		elif move == "U":
			j -= 1

		elif move == "D":
			j += 1

	if maze[j][i] == "X":
		print("Found: " + moves)
		printMaze(maze, moves)
		return True

	return False


# MAIN ALGORITHM

nums = queue.Queue()
nums.put("")
add = ""
maze  = MakeMaze()


while not findEnd(maze, add): 
	print('working')
	add = nums.get()
    #print(add)
	for j in ["L", "R", "U", "D"]:
		put = add + j       
		if valid(maze, put):
			nums.put(put)
