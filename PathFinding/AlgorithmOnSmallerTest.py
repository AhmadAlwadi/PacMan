import queue, time
# Make maze
StartCoord = (0, 0)
def MakeMaze():
	global StartCoord
	Maze = [[' ' for i in range(10)] for j in range(10)]
	start = (1, 7)
	StartCoord = start
	end = (8, 8)

	Maze[start[0]][start[1]] = "O"
	Maze[end[0]][end[1]] = "X"

	Barriers = [
				[0,0,3,1],
		        [4,2,9,3],
		        [4,3,5,6],
		        [4,5,9,6],
		        [0,0,10,1],
		        [0,9,10,10],
		        [9,0,10,10],
		        [0,0,1,10]
	   		   ]

	x1, x2, y1, y2 = 0, 0, 0, 0
	for z in Barriers:
			x1, y1, x2, y2 = z[0], z[1], z[2], z[3]
			for i in range(y1, y2):
				for j in range(x1, x2):
					Maze[i][j] = '#'
	return Maze

def printMaze(maze, path=""):
    print('printing maze')
    for x, pos in enumerate(maze[StartCoord[0]]):
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

def Print_(maze):
	totString = ''
	for i in maze:
		print(i, '\n')
Print_(maze)
startTime = time.time()

while not findEnd(maze, add): 
	add = nums.get()
    #print(add)
	for j in ["L", "R", "U", "D"]:
		put = add + j       
		if valid(maze, put):
			nums.put(put)
print(f"It has taken {time.time() - startTime} seconds to run")