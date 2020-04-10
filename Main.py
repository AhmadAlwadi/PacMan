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

# The PacMan class 
class PacMan(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Resources/PacManOpenMouth.png')
		self.image = pygame.transform.scale(self.image, (30, 30))

		self.rect = self.image.get_rect()
		self.rect.center = (290, 570)

	def update(self):
		self.rect.x += xChange
		self.rect.y += yChange

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

def ImportWalls():
	walls = []
	coords = []
	LevelPath = "Levels/Level".strip() + str(LvlNumber).strip() + ".json"
	with open(LevelPath) as f:
		walls = json.load(f)
	for i in walls['Walls']:
		coords.append(i)
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
	pygame.mixer.music.load(f"Resources/{TrackName}.wav")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(0)

# This function handles all the text blitting
def BlitText(stuff, size, Coord, font, colour):
	x = Coord[0]
	y = Coord[1]
	TextToBlit = Text(x, y, size)
	TextToBlit.update(SCREEN, stuff, font, colour)

''' This function checks if ghost/pacman have collided with wall
	arr will be the array of coordinates that we are checking against
	this function returns a boolean value, true if the don't collide 
	and false if they do
'''
def CheckCollision(arr, coord):
	for i in arr:
		if i[0] == coord[0] and i[1] == coord[1]:
			return False

# This function is blitting a specific image to the screen
def BlitImage(x, y):
	SCREEN.blit(PacmanImage, (x, y))


def MainLoop():
	global xChange, yChange

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
			if counter == 1:
				BlitText("Get Ready!", 15, (235, 210), "Resources/emulogic.ttf", RED)
				LoadMusic('BKGDMusic')
				time.sleep(5)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					print('player moved left')
					xChange = -5

				elif event.key == pygame.K_RIGHT:
					print('player moved right')
					xChange = 5

				elif event.key == pygame.K_UP:
					yChange = -5

				elif event.key == pygame.K_DOWN:
					yChange = 5


			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					xChange = 0

				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					yChange = 0

		# Update
		AllSprites.update()

		# Render
		SCREEN.fill(BLACK)
		AllSprites.draw(SCREEN)
		pygame.display.flip()
		CLOCK.tick(60)

if __name__ == '__main__':
	MainLoop()
