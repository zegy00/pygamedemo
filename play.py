import sys, pygame
import time
from threading import Thread

IS_GAME_RUNNING = True
DIRECTION = {"LEFT": 0, "RIGHT": 1, "TOP": 2, "BOTTOM": 3}
screenHeight, screenWidth = 1024, 1024

class Node:
	def __init__(self, dataval):
		self._dataval = dataval
		self._nextval = None

	def setNext(self, nextval):
		self._nextval = nextval

	def next(self):
		return self._nextval

	def getValue(self):
		return self._dataval

class GameObject(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, screen):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self._image = pygame.transform.scale(img, size)
		self._colBox = pygame.Rect(location[0], location[1], self._screen.get_rect().height, self._screen.get_rect().width)
		self._imagePos = pygame.Rect(0, 0, self._image.get_rect().height, self._image.get_rect().width)
		self._speed = 5

	def getRect(self):
		return self._colBox

	def setLocation(self, left, top):
		self._colBox.left = left
		self._colBox.top = top

	def getImage(self):
		return self._image

	def getImagePos(self):
		self._imagePos.left = (int((self._image.get_rect().left) + (self._colBox.left)) - int(self._image.get_rect().width/2)) + int(self._colBox.width/2)
		self._imagePos.top = (int((self._image.get_rect().top) + (self._colBox.top)) - int(self._image.get_rect().height/2)) + int(self._colBox.height/2)

		return self._imagePos

	def getSpeed(self):
		return self._speed

	def move(self, direction):		
		newPos = self._colBox
		if (direction == DIRECTION["RIGHT"]):
			newPos.right += self._speed
		elif (direction == DIRECTION["LEFT"]):
			newPos.left -= self._speed
		elif (direction == DIRECTION["TOP"]):
			newPos.top -= self._speed
		elif (direction == DIRECTION["BOTTOM"]):
			newPos.bottom += self._speed

		# uncomment to see the collision box
		#pygame.draw.rect(self._screen, (255, 0, 0), newPos)
		
		self._screen.blit(self._image, self.getImagePos())

class Background(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		self._speed = 2

	def move(self, direction):		
		newPos = self._colBox
		if (direction == DIRECTION["RIGHT"]):
			newPos.right += self._speed
		elif (direction == DIRECTION["LEFT"]):
			newPos.left -= self._speed
		elif (direction == DIRECTION["TOP"]):
			newPos.top -= self._speed
		elif (direction == DIRECTION["BOTTOM"]):
			newPos.bottom += self._speed

		# uncomment to see the collision box
		#pygame.draw.rect(self._screen, (255, 0, 0), newPos)
		
		self._screen.blit(self._image, newPos)

# Use Node to create a looped linked list and pass header to the constructor
class BackgroundLoop(Thread):
	def __init__(self, backgrounds):
		Thread.__init__(self)
		self._backgrounds = backgrounds
		self._screen = pygame.display.set_mode((screenHeight, screenWidth))

	def run(self):
		global IS_GAME_RUNNING, screenHeight, screenWidth

		backgroundNode = self._backgrounds
		nextBackgroundNode = self._backgrounds.next()
		background = backgroundNode.getValue()
		nextBackground = nextBackgroundNode.getValue()
		background.setLocation(0, 0)
		nextBackground.setLocation(0, -self._screen.get_height())
		while(IS_GAME_RUNNING):			
			background.move(DIRECTION["BOTTOM"])
			nextBackground.move(DIRECTION["BOTTOM"])
			if(background.getRect().top > self._screen.get_rect().bottom):
				background.setLocation(0, -self._screen.get_height())
				backgroundNode = nextBackgroundNode
				nextBackgroundNode = nextBackgroundNode.next()
				background = backgroundNode.getValue()
				nextBackground = nextBackgroundNode.getValue()

			self._screen.blits(blit_sequence=[(background.getImage(), background.getRect()), (nextBackground.getImage(), nextBackground.getRect())])


class Bullet(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self._image = pygame.transform.scale(img, (int(size[0]//4), int(size[1]//4)))
		self._colBox = pygame.Rect(location[0], location[1], int(self._screen.get_rect().height//16), int(self._screen.get_rect().width//16))
		self._speed = 4

	def getBulletToDraw(self):
		return (self.getImage(), self.getImagePos())


class Bullets(Thread):
	def __init__(self, imageFile, screen, player):
		Thread.__init__(self)
		self._image = imageFile
		self._screen = screen
		self._player = player
		location = self._player.getRect()
		bullet = Bullet(self._image, location, self._screen)
		self._bullets = [bullet] * 10000

	def run(self):
		global IS_GAME_RUNNING

		while(IS_GAME_RUNNING):
			try:
				numBullets = 0
				if (pygame.key.get_pressed()[pygame.K_SPACE]):
					numBullets += 1

					location = self._player.getRect()
					self._bullets[numBullets].setLocation(location[0], location[1])
					while(numBullets):

						for bulletsIndx in range(numBullets):
							if (self._bullets[bulletsIndx].getRect().bottom > self._screen.get_rect().top):
								self._bullets[bulletsIndx].move(DIRECTION["TOP"])
							else :
								del self._bullets[bulletsIndx]
								numBullets -= 1	
					
						self._screen.blits(blit_sequence=[self._bullets[i].getBulletToDraw() for i in range(numBullets)])
			except Exception as ex:
				print(ex.args)
				sys.exit(0)
						


class Player(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self._image = pygame.transform.scale(img, (int(size[0]//4), int(size[1]//4)))
		self._colBox = pygame.Rect(location[0], location[1], int(self._screen.get_rect().height//6), int(self._screen.get_rect().width//4))
		self._speed = 5
		self._bullets = Bullets('resources/sprites/bullet01.png', self._screen, self)
		self._bullets.start()

def main():
	pygame.init()
	
	global IS_GAME_RUNNING, screenHeight, screenWidth

	screen = pygame.display.set_mode((screenHeight, screenWidth))

	pygame.display.set_caption("Small py game demo")

	backgroundTropicalBeach = Background('resources/sprites/background_space01.jpg', [0, 0], screen)
	background02 = Background('resources/sprites/background_space02.jpg', [0, screenHeight], screen)

	nodeBackground01 = Node(backgroundTropicalBeach)
	nodeBackground02 = Node(background02)
	nodeBackground01.setNext(nodeBackground02)
	nodeBackground02.setNext(nodeBackground01)

	startPoint = [0, 200]
	chungus = Player('resources/sprites/chungus.jpg', startPoint, screen)
	backgroundLoop = BackgroundLoop(nodeBackground01)
	backgroundLoop.start()

	while(IS_GAME_RUNNING):

		# screen.fill([255, 255, 255])
		# screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
		screen.blit(chungus.getImage(), chungus.getImagePos())
		# uncomment to see the collision box
		#pygame.draw.rect(screen, (255, 0, 0), chungus.getRect())
		pygame.display.update()

		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
				IS_GAME_RUNNING = False
		
		if (pygame.key.get_pressed()[pygame.K_RIGHT] and (chungus.getRect().right) < screen.get_rect().right):
			chungus.move(DIRECTION["RIGHT"])

		elif (pygame.key.get_pressed()[pygame.K_LEFT] and (chungus.getRect().left) > screen.get_rect().left):
			chungus.move(DIRECTION["LEFT"])

		if (pygame.key.get_pressed()[pygame.K_UP] and (chungus.getRect().top) > screen.get_rect().top):
			chungus.move(DIRECTION["TOP"])

		elif (pygame.key.get_pressed()[pygame.K_DOWN] and (chungus.getRect().bottom) < screen.get_rect().bottom):
			chungus.move(DIRECTION["BOTTOM"])

	sys.exit(0)

main()


