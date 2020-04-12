import pygame, time, sys, random, math, json
from pygame.locals import *

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

# The PacMan class 
class PacMan(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Resources/PacManOpenMouth.png')
		self.image = pygame.transform.scale(self.image, (30, 30))

		self.rect = self.image.get_rect()
		self.rect.center = (290, 570)

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
			# Reset thwe x axis on the pacman
			self.rect.left = self.CurrentX
		else:
			self.rect.top = NewY
			# Check for a vertical collision
			YCollision = pygame.sprite.spritecollide(self, WallCoords, False)
			if YCollision:
				# Reset the y axis on the pacman
				self.rect.top = self.CurrentY

		'''if gate != False:
			gate_hit = pygame.sprite.spritecollide(self, gate, False)
			if gate_hit:
				self.rect.left = self.CurrentX
				self.rect.top = self.CurrentY'''

class Ghost(pygame.sprite.Sprite):
	def __init__(self, name, coord):
		pygame.sprite.Sprite.__init__(self)

		ImagePath = f"Resources/{name.strip()}.png"
		self.image = pygame.image.load(ImagePath)
		self.image = pygame.transform.scale(self.image, (24, 24))

		self.rect = self.image.get_rect()
		self.rect.x = coord[0]
		self.rect.y = coord[1]


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
		pygame.mixer.music.set_volume(0.3)
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

def MainLoop():
	global xChange, yChange, Score

	AllSprites = pygame.sprite.RenderPlain()
	PacDots = pygame.sprite.RenderPlain()
	Ghosts = pygame.sprite.RenderPlain()
	PacManCollide = pygame.sprite.RenderPlain()
	Walls = DrawWalls(AllSprites)
	Gate = DrawGate(AllSprites)

	Pinky = Ghost("Pinky", (252, 270))
	AllSprites.add(Pinky)

	Blinky = Ghost("Blinky", (278, 270))
	AllSprites.add(Blinky)

	Inky = Ghost("Inky", (304, 270))
	AllSprites.add(Inky)

	Clyde = Ghost("Clyde", (330, 270))
	AllSprites.add(Clyde)


	Player = PacMan()
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
					xChange = -5

				elif event.key == pygame.K_RIGHT:
					CalcRota(Player, 'Right')
					Player.direction = 'Right'
					xChange = 5

				elif event.key == pygame.K_UP:
					CalcRota(Player, 'Up')
					Player.direction = 'Up'
					yChange = -5

				elif event.key == pygame.K_DOWN:
					CalcRota(Player, 'Down')
					Player.direction = 'Down'
					yChange = 5

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					xChange = 0

				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					yChange = 0

		
		# See if the Pacman block has collided with anything.
		PacdotHit = pygame.sprite.spritecollide(Player, PacDots, True)
		
		# Check the list of collisions.
		if len(PacdotHit) > 0:
			LoadMusic('EatingMusic')
			Score +=10*len(PacdotHit)

		# Update
		#AllSprites.update()
		Player.update(Walls, Gate)

		# Render
		SCREEN.fill(BLACK)
		BlitText(f"Score: {Score}", 12, (450, 10), 'Resources/emulogic.ttf',PURPLE)
		AllSprites.draw(SCREEN)
		pygame.display.flip()
		CLOCK.tick(60)

if __name__ == '__main__':
	MainLoop()