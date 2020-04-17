'''
This file is supposed to test all the phases of the custom algorithm that
I wrote
'''

import math
from math import atan2, degrees, pi

pacmanLocation = (4, 8)
ghostLocation = (4, 5)
def MakeMaze():
	global StartCoord
	Maze = [[' ' for i in range(10)] for j in range(10)]
	Maze[pacmanLocation[0]][pacmanLocation[1]] = 'P'
	Maze[ghostLocation[0]][ghostLocation[1]] = 'G'

	for i in range(len(Maze)-1):
		for j in range(len(Maze)-1):
			if Maze[i][j] == " ":
				Maze[i][j] = "."
	return Maze

def printMaze(maze):
    print('printing maze')

    currentLine = ''
    for j, row in enumerate(maze):
        for i, col in enumerate(row):
        	currentLine = currentLine + maze[i][j]
        print(currentLine)
        currentLine = ''

def CalcAngle(pacmanPosition, ghostPosition):
	x1, y1, x2, y2 = pacmanPosition[0], pacmanPosition[1], ghostPosition[0], ghostPosition[1]

	dx = x2 - x1
	dy = y2 - y1

	rads = atan2(-dx,dy)
	rads %= 2*pi

	degs = degrees(rads)
	print(degs)

	return degs

def CalcQuadrant(angle):

	if angle >=0 and angle <= 90:
		quad = 1

	elif angle >90 and angle <= 180:
		quad = 2

	elif angle >180 and angle <= 270:
		quad = 3

	elif angle >270 and angle <= 360:
		quad = 4

	print(quad)
	return quad

def PrioetiseDirs(quad):
	if quad == 1:
		directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']

	elif quad == 2:
		directions = ['DOWN', 'RIGHT', 'UP', 'LEFT']

	elif quad == 3:
		directions = ['DOWN', 'LEFT', 'UP', 'RIGHT']

	elif quad == 4:
		directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']

	print(directions)
	return directions


class Ghost(pygame.sprite.Sprite):
	def __init__(self, name, coord, speed):
		pygame.sprite.Sprite.__init__(self)

		ImagePath = f"Resources/{name.strip()}.png"
		self.image = pygame.image.load(ImagePath)
		self.image = pygame.transform.scale(self.image, (1, 1))

		self.rect = self.image.get_rect()
		self.rect.left = coord[0]
		self.rect.top = coord[1]

		self.position = (self.rect.left, self.rect.top)

		self.speed = speed
		self.direction = ''

		self.xSpeed = 0
		self.ySpeed = 0

	def update(self, playerPos, walls):
		
		# Check if the ghost hit a wall first
		if self.Checkcollision(walls):
			NextDir = Pathfinding(playerPos, self.position, self, walls, self.speed)

			if NextDir == 'RIGHT':
				self.rect.left += self.speed
			
			elif NextDir == 'LEFT':
				self.rect.left -= self.speed
			
			elif NextDir == 'UP':
				self.rect.top -= self.speed
			
			elif NextDir == 'DOWN':
				self.rect.top += self.speed

		elif Frame%2==0:
			NextDir = Pathfinding(playerPos, self.position, self, walls, self.speed)

			if NextDir == 'RIGHT':
				self.rect.left += self.speed
			
			elif NextDir == 'LEFT':
				self.rect.left -= self.speed
			
			elif NextDir == 'UP':
				self.rect.top -= self.speed
			
			elif NextDir == 'DOWN':
				self.rect.top += self.speed

		self.rect.left += self.xSpeed
		self.rect.top += self.ySpeed



		# Update the position
		self.position = (self.rect.left, self.rect.top)

# The wall class
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x

def ImportWalls():
	global WallCoords
	walls = []
	coords = []
	LevelPath = "Levels/Level".strip() + str(LvlNumber).strip() + ".json"
	with open(LevelPath) as f:
		walls = json.load(f)
	for i in walls['Walls']:
		coords.append(i)
		WallCoords.append(i)
	return coords

def DrawWalls(AllSprites):
	WallList = pygame.sprite.RenderPlain()

	CoordList = ImportWalls()
	for i in CoordList:
		wall = Wall(i[0], i[1], i[2], i[3], WALLS_COLOR)
		WallList.add(wall)
		AllSprites.add(wall)
	return WallList


Maze = MakeMaze()
printMaze(Maze)
angle = CalcAngle(pacmanLocation, ghostLocation)
quad = CalcQuadrant(angle)
dirs = PrioetiseDirs(quad)

'''
Conclusions:
	--> CalcAngle() function takes x2, y2 as the origin thus i have to swap them
	--> It calculates the angle from the left x-axis downward to the positive 
		x-axis and that'd be 180, the negative y-axis would be 90
'''
