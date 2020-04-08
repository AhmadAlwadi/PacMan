import pygame, time, sys, random, math, json

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

# Pygame initialisations
pygame.init()

# The window attributes
SCREEN_SIZE = (800, 800)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PacMan Game")
CLOCK = pygame.time.Clock()

# Global vars
Score = 0
LvlNumber = 1

# The PacMan class 
'''class PacMan:
	def __init__:
		position = (0, 0)'''

# This class to blit stuff on screen
class Text:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
 
    def update(self, screen, text):
        cover = pygame.Surface([len(text)*self.size//2.1, self.size*0.7])
        cover.fill([0,0,30])
        screen.blit(cover, (self.x, self.y))
        myscore = pygame.font.Font(None,self.size)
        label = myscore.render(text, True, WHITE)
        textrect = (self.x, self.y)            
        screen.blit(label, textrect)

# The wall class
class Wall:
	def __init__(self):
		self.start = 0
		self.end = 0
		self.width = 0
		self.height = 0

	def ImportWalls(self):
		walls = []
		coords = []
		LevelPath = "Levels/Level".strip() + str(LvlNumber).strip() + ".json"
		with open(LevelPath) as f:
			walls = json.load(f)
		for i in walls['Walls']:
			coords.append(i)
			print(f"{i} \n")
		return walls

def MainLoop():
	running = True
	placeholder = Wall()
	walls = []
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()
		while running:
			walls = placeholder.ImportWalls()
			running = False
		pygame.display.update()
		CLOCK.tick(60)

	pygame.quit()


if __name__ == '__main__':
	MainLoop()


'''walls = [ [0,0,6,600],
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