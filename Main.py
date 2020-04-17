import pygame, time, sys, random, math, json
from pygame.locals import *
from math import atan2, degrees, pi


# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WALLS_COLOR = (60, 66, 196)
GREY = (171, 173, 189)

# Pygame initialisations
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# The window attributes
SCREEN_SIZE = (606, 606)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pac-Man Game")
CLOCK = pygame.time.Clock()

# Global vars
Score = 0
LvlNumber = 1
WallCoords = []
xChange = 0
yChange = 0
WallCoords = []
Frame = 0 

# The PacMan class 
class PacMan(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Resources/PacManOpenMouth.png')
		self.image = pygame.transform.scale(self.image, (32, 32))

		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.prev_x = x
		self.prev_y = y

		self.position = (self.rect.x, self.rect.y)

		self.direction = 'Left'

	def update(self, WallCoords, gate):

		# Making a backup of the values
		self.CurrentX = self.rect.left
		self.CurrentY = self.rect.top

		# Changing the values and updating the position
		NewX = self.CurrentX + xChange
		NewY = self.CurrentY + yChange

		self.rect.left = NewX

		# Check for collision
		XCollision = pygame.sprite.spritecollide(self, WallCoords, False)
		
		# Check if the x axis is colliding with any walls 
		if XCollision:	
			# Reset the x axis on the pacman
			self.rect.left = self.CurrentX
		else:
			self.rect.top = NewY
			# Check for a vertical collision
			YCollision = pygame.sprite.spritecollide(self, WallCoords, False)
			if YCollision:
				# Reset the y axis on the pacman
				self.rect.top = self.CurrentY
			else:
				# Updating the pacman position
				self.position = (self.rect.left, self.rect.top)

		if gate != False:
			gate_hit = pygame.sprite.spritecollide(self, gate, False)
			if gate_hit:
				self.rect.left = self.CurrentX
				self.rect.top = self.CurrentY



class Ghost(pygame.sprite.Sprite):
	def __init__(self, name, coord, speed):
		pygame.sprite.Sprite.__init__(self)

		ImagePath = f"Resources/{name.strip()}.png"
		self.image = pygame.image.load(ImagePath)
		self.image = pygame.transform.scale(self.image, (24, 24))

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

	def Checkcollision(self, walls):
		xSpeed = 0
		ySpeed = 0

		if self.direction == 'RIGHT':
			self.xSpeed = self.speed

		elif self.direction == 'LEFT':
			self.xSpeed -= self.speed

		elif self.direction == 'UP':
			self.ySpeed -= self.speed

		elif self.direction == 'DOWN':
			self.ySpeed = self.speed

		# Making a backup of the values
		CurrentX = self.rect.left
		CurrentY = self.rect.top

		# Changing the values and updating the position
		NewX = CurrentX + xSpeed
		NewY = CurrentY + ySpeed

		self.rect.left = NewX

		# Check for collision
		XCollision = pygame.sprite.spritecollide(self, walls, False)
		
		# Check if the x axis is colliding with any walls 
		if XCollision:	
			# Reset the x axis on the ghost
			self.rect.left = CurrentX
			self.xSpeed = 0
			return True
		else:
			self.rect.top = NewY
			# Check for a vertical collision
			YCollision = pygame.sprite.spritecollide(self, walls, False)
			if YCollision:
				# Reset the y axis on the ghost
				self.rect.top = CurrentY
				self.ySpeed = 0
				return True
			else:
				# Resetting the values to their original values till the ghost gets a new direction
				self.rect.left = CurrentX
				self.rect.top = CurrentY
				return False

# This class to blit text on screen
class Text:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
 
    def update(self, screen, text, font, colour):
        cover = pygame.Surface([len(text)*self.size//2.1, self.size*0.7])
        cover.fill([0,0,30])
        screen.blit(cover, (self.x, self.y))
        myscore = pygame.font.Font(font,self.size)
        label = myscore.render(text, True, colour)
        textrect = (self.x, self.y)            
        screen.blit(label, textrect)

# The wall class
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x

# The pacdot class 
class PacDot(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("Resources/PacDot.png")
		self.image = pygame.transform.scale(self.image, (4, 4))

		self.rect = self.image.get_rect()

		self.position = (self.rect.x, self.rect.y)

# This class holds the large pacdots that scare the ghosts, it inherits the 
# regular pacdot, except it has a larger scale
class Energizers(PacDot):
	def __init__(self):
		self.image = pygame.transform.scale(self.image, (8, 8))

		self.rect = self.image.get_rect()

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

def DrawGate(AllSprites):
	gate = pygame.sprite.RenderPlain()
	gate.add(Wall(282, 242, 42, 2, GREY))
	AllSprites.add(gate)
	return gate

# This function plays music
def LoadMusic(TrackName):
	if not (pygame.mixer.music.get_busy()):
		pygame.mixer.music.load(f"Resources/{TrackName}.wav")
		pygame.mixer.music.set_volume(0.0)
		pygame.mixer.music.play(0)

# This function handles all the text blitting
def BlitText(stuff, size, Coord, font, colour):
	x = Coord[0]
	y = Coord[1]
	TextToBlit = Text(x, y, size)
	TextToBlit.update(SCREEN, stuff, font, colour)

# This function calculates how many degrees does the image of the pacman have to roate
def CalcRota(pacman, NextDir):
	if pacman.direction == 'Left':
		if NextDir == 'Right':
			rotation = 180
		elif NextDir == 'Up':
			rotation = -90
		elif NextDir == 'Down':
			rotation = 90
		else:
			rotation = 0

	elif pacman.direction == 'Right':
		if NextDir == 'Left':
			rotation = 180
		elif NextDir == 'Up':
			rotation = 90
		elif NextDir == 'Down':
			rotation = -90
		else:
			rotation = 0

	elif pacman.direction == 'Up':
		if NextDir == 'Down':
			rotation = 180
		elif NextDir == 'Right':
			rotation = -90
		elif NextDir == 'Left':
			rotation = 90
		else:
			rotation = 0

	elif pacman.direction == 'Down':
		if NextDir == 'Up':
			rotation = 180
		elif NextDir == 'Right':
			rotation = 90
		elif NextDir == 'Left':
			rotation = -90
		else:
			rotation = 0

	pacman.image = pygame.transform.rotate(pacman.image, rotation)


# ALL THE PATHFINDING ALGORITHM CODE SHOULD GO HERE 

def Pathfinding(pacmanPosition, ghostPosition, ghost, walls, speed):

	ViableDirs = GetViableDirections(ghostPosition, ghost, walls, speed)
	angle = CalcAngle(pacmanPosition, ghostPosition)
	quad = CalcQuadrant(angle)
	prioritisedDirections = PrioetiseDirs(quad)

	runLoop = True
	
	while runLoop:
		for i in prioritisedDirections:
			for j in ViableDirs:
				if i == j:
					finalDir = i
					runLoop = False
		randomDir = random.choice(ViableDirs)
		finalDir = randomDir
		runLoop = False
	
	#print(ViableDirs, angle, quad, prioritisedDirections, finalDir)	
	return finalDir

def GetViableDirections(ghostPosition, ghost, walls, speed):
	x, y = ghostPosition[0], ghostPosition[1]

	directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

	# Use sprite collision to see if they have collided
	for i in range (0, len(directions)-1):
		if i == 0:
			ghost.rect.top = y - speed
			# Check for a vertical collision
			YCollision = pygame.sprite.spritecollide(ghost, walls, False)

			if YCollision:
				# Reset the y axis on the pacman
				ghost.rect.top = y
				directions.remove('UP')
			else:
				# Updating the pacman position
				ghost.position = (ghost.rect.left, ghost.rect.top)

		elif i == 1:
			ghost.rect.top = y + speed
			# Check for a vertical collision
			YCollision = pygame.sprite.spritecollide(ghost, walls, False)

			if YCollision:
				# Reset the y axis on the pacman
				ghost.rect.top = y
				directions.remove('DOWN')
			else:
				# Updating the pacman position
				ghost.position = (ghost.rect.left, ghost.rect.top)

		elif i == 2:
			ghost.rect.left = x - speed

			# Check for collision
			XCollision = pygame.sprite.spritecollide(ghost, walls, False)
			
			# Check if the x axis is colliding with any walls 
			if XCollision:	
				# Reset the x axis on the pacman
				ghost.rect.left = x
				directions.remove('LEFT')

			else:
				ghost.rect.top = y 
				# Check for a vertical collision
				YCollision = pygame.sprite.spritecollide(ghost, walls, False)

				if YCollision:
					# Reset the y axis on the pacman
					ghost.rect.top = y
					directions.remove('LEFT')
				else:
					# Updating the pacman position
					ghost.position = (ghost.rect.left, ghost.rect.top)

		elif i == 3:
			ghost.rect.left = x + speed

			# Check for collision
			XCollision = pygame.sprite.spritecollide(ghost, walls, False)
			
			# Check if the x axis is colliding with any walls 
			if XCollision:	
				# Reset the x axis on the pacman
				ghost.rect.left = x
				directions.remove('RIGHT')
			else:
				ghost.rect.top = y 
				# Check for a vertical collision
				YCollision = pygame.sprite.spritecollide(ghost, walls, False)

				if YCollision:
					# Reset the y axis on the pacman
					ghost.rect.top = y
					directions.remove('RIGHT')

		ghost.position = ghostPosition

	return directions

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

	return directions


# END OF THE PATHFINDING ALFORITHM

def MainLoop():
	global xChange, yChange, Score, Frame

	AllSprites = pygame.sprite.RenderPlain()
	PacDots = pygame.sprite.RenderPlain()
	Ghosts = pygame.sprite.RenderPlain()
	PacManCollide = pygame.sprite.RenderPlain()
	Walls = DrawWalls(AllSprites)
	Gate = DrawGate(AllSprites)

	Pinky = Ghost("Pinky", (200, 270), 2)
	AllSprites.add(Pinky)

	Blinky = Ghost("Blinky", (278, 270), 3)
	AllSprites.add(Blinky)

	Inky = Ghost("Inky", (304, 270), 2)
	AllSprites.add(Inky)

	Clyde = Ghost("Clyde", (330, 270), 4)
	AllSprites.add(Clyde)


	Player = PacMan(287, 439)
	AllSprites.add(Player)


	# Draw the grid
	# Maybe try to optimise this it takes too much time
	for row in range(19):
	  for column in range(19):
	      if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
	          continue
	      else:
	        dot = PacDot()

	        # Set a random location for the pacdot
	        dot.rect.x = (30*column+6)+26
	        dot.rect.y = (30*row+6)+26

	        b_collide = pygame.sprite.spritecollide(dot, Walls, False)
	        p_collide = pygame.sprite.spritecollide(dot, PacManCollide, False)
	        if b_collide:
	          continue
	        elif p_collide:
	          continue
	        else:
	          # Add the block to the list of objects
	          PacDots.add(dot)
	          AllSprites.add(dot)

	# This counter is used to play the things that only play once	
	counter = 0 
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()
			
			counter += 1
			if counter == 2:
				LoadMusic('BKGDMusic')

				# Render once
				SCREEN.fill(BLACK)
				BlitText("Get Ready!", 15, (235, 210), "Resources/emulogic.ttf", RED)
				AllSprites.draw(SCREEN)
				pygame.display.flip()
				CLOCK.tick(60)

				time.sleep(4)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					CalcRota(Player, 'Left')
					Player.direction = 'Left'
					xChange = -30

				elif event.key == pygame.K_RIGHT:
					CalcRota(Player, 'Right')
					Player.direction = 'Right'
					xChange = 30

				elif event.key == pygame.K_UP:
					CalcRota(Player, 'Up')
					Player.direction = 'Up'
					yChange = -30

				elif event.key == pygame.K_DOWN:
					CalcRota(Player, 'Down')
					Player.direction = 'Down'
					yChange = 30

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					xChange = 0

				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					yChange = 0

		Frame += 1

		# See if the Pacman block has collided with anything.
		PacdotHit = pygame.sprite.spritecollide(Player, PacDots, True)
		
		# Check the list of collisions.
		if len(PacdotHit) > 0:
			LoadMusic('EatingMusic')
			Score +=10*len(PacdotHit)

		# Update
		#AllSprites.update()
		Player.update(Walls, Gate)
		Inky.update(Player.position, Walls)
		Clyde.update(Player.position, Walls)
		Blinky.update(Player.position, Walls)
		Pinky.update(Player.position, Walls)


		# Render
		SCREEN.fill(BLACK)
		BlitText(f"Score: {Score}", 12, (450, 10), 'Resources/emulogic.ttf',PURPLE)
		AllSprites.draw(SCREEN)
		pygame.display.flip()
		CLOCK.tick(60)

if __name__ == '__main__':
	MainLoop()

ImportWalls()
MakeWallAStar(WallCoords)