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
		self._colBox = self._image.get_rect()
		self._colBox.left, self._colBox.top = location[0], location[1]

	def getRect(self):
		return self._colBox

	def setLocation(self, left, top):
		self._colBox.left = left
		self._colBox.top = top

	def getImage(self):
		return self._image

class DynamicGameObject(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		self._speed = 5

	def getSpeed(self):
		return self._speed

	def move(self, direction):
		if (direction == DIRECTION["RIGHT"]):
			self._colBox.right += self._speed
		elif (direction == DIRECTION["LEFT"]):
			self._colBox.left -= self._speed
		elif (direction == DIRECTION["TOP"]):
			self._colBox.top -= self._speed
		elif (direction == DIRECTION["BOTTOM"]):
			self._colBox.bottom += self._speed

		# uncomment to see the collision box
		#pygame.draw.rect(self._screen, (255, 0, 0), newPos)

		self._screen.blit(self._image, self._colBox)

	def _scale(self, size, divider):
		return (int(size[0] / divider)), int((size[1] / divider))


class Background(DynamicGameObject):
	def __init__(self, imageFile, location, screen):
		DynamicGameObject.__init__(self, imageFile, location, screen)
		self._speed = 2

	def move(self, direction):		
		if (direction == DIRECTION["RIGHT"]):
			self._colBox.right += self._speed
		elif (direction == DIRECTION["LEFT"]):
			self._colBox.left -= self._speed
		elif (direction == DIRECTION["TOP"]):
			self._colBox.top -= self._speed
		elif (direction == DIRECTION["BOTTOM"]):
			self._colBox.bottom += self._speed

		# uncomment to see the collision box
		#pygame.draw.rect(self._screen, (255, 0, 0), newPos)
		
		self._screen.blit(self._image, self._colBox)


class Bullet(DynamicGameObject):
	def __init__(self, imageFile, location, screen):
		DynamicGameObject.__init__(self, imageFile, location, screen)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		scaledSize = self._scale(size, 5)
		self._image = pygame.transform.scale(img, (scaledSize[0], scaledSize[1]))
		self._colBox.left, self._colBox.top = location.centerx, location.centery
		self._colBox.height = scaledSize[0]
		self._colBox.width = scaledSize[1]
		self._speed = 3

	def getBulletToDraw(self):
		return (self.getImage(), self._colBox)


class Bullets(Thread):
	def __init__(self, imageFile, screen, player):
		Thread.__init__(self)
		self._image = imageFile
		self._screen = screen
		self._player = player
		location = self._player.getRect()
		bullet = Bullet(self._image, location, self._screen)
		self._bullets = [bullet] * 100000

	def run(self):
		global IS_GAME_RUNNING

		while(IS_GAME_RUNNING):
			try:
				numBullets = 0
				if (pygame.key.get_pressed()[pygame.K_SPACE]):
					numBullets += 1

					location = self._player.getRect()
					self._bullets[numBullets].setLocation(location.centerx, location.centery)
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

class Health():
	def __init__(self, health):
		self._health = health
		self._currentHealth = health

	def decreaseHealth(self, healthPoints):
		if(isinstance(healthPoints, int) and (healthPoints > 0 and healthPoints < 10000)):
			self._currentHealth -= healthPoints
			if self._currentHealth < 0:
				self._currentHealth = 0
		else:
			print("Health points should be of integer type and in range 0-10000")

	def increaseHealth(self, healthPoints):
		if(isinstance(healthPoints, int) and (healthPoints > 0 and healthPoints < 10000)):
			self._currentHealth += healthPoints 
			if self._currentHealth > self._health:
				self._currentHealth = self._health
		else:
			print("Health points should be of integer type and in range 0-10000")

	def getHealth(self):
		return self._health

	def getCurrentHealth(self):
		return self._currentHealth

	def getCurrentHpPercentage(self):
		return (self._currentHealth * 100) / self._health
						
class HealthBar(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, surface, player):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._image = pygame.transform.scale(img, self._scale(size, 4))
		self._rect = self._image.get_rect()
		self._rectWidthMax = self._rect.width
		self._rect.left, self._rect.top = location[0], location[1]
		self._surface = surface
		self._color = (237, 41, 57)
		self._player = player

	def _getRectanglePercentage(self):
		curHpPercentage = self._player.getCurrentHpPercentage()
		return (curHpPercentage / 100) * self._rectWidthMax

	def __adjustHealthBar(self):
		self._rect.width = int(self._getRectanglePercentage())

	def _scale(self, size, divider):
		return (int(size[0] / divider)), int((size[1] / divider))

	def drawHealthBar(self):
		self.__adjustHealthBar()
		pygame.draw.ellipse(self._surface, self._color, self._rect)
		self._surface.blit(self._image, self._rect)


class Player(DynamicGameObject, Health):
	def __init__(self, imageFile, location, screen, health):
		DynamicGameObject.__init__(self, imageFile, location, screen)
		Health.__init__(self, health)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		scaledSize = self._scale(size, 2)
		self._image = pygame.transform.scale(img, (scaledSize[0], scaledSize[1]))
		self._colBox.height = scaledSize[0]
		self._colBox.width = scaledSize[1]
		self._speed = 8
		self._bullets = Bullets('resources/sprites/bullet02.png', self._screen, self)
		self._bullets.start()

def main():
	pygame.init()
	
	global IS_GAME_RUNNING, screenHeight, screenWidth

	screen = pygame.display.set_mode((screenHeight, screenWidth))

	pygame.display.set_caption("Small py game demo")

	background01 = Background('resources/sprites/background_space01.jpg', [0, 0], screen)
	background02 = Background('resources/sprites/background_space02.jpg', [0, screenHeight], screen)

	nodeBackground01 = Node(background01)
	nodeBackground02 = Node(background02)
	nodeBackground01.setNext(nodeBackground02)
	nodeBackground02.setNext(nodeBackground01)

	startPoint = [400, 200]
	mainPlayer = Player('resources/sprites/chungus.png', startPoint, screen, 100)
	mainPlayerHealthBar = HealthBar('resources/sprites/health_bar.png', [15, 15], screen, mainPlayer)

	backgroundNode = nodeBackground01
	nextBackgroundNode = nodeBackground01.next()
	background = backgroundNode.getValue()
	nextBackground = nextBackgroundNode.getValue()
	background.setLocation(0, 0)
	nextBackground.setLocation(0, -screen.get_height())

	while(IS_GAME_RUNNING):

		screen.blit(mainPlayer.getImage(), mainPlayer.getRect())
		mainPlayerHealthBar.drawHealthBar()
		# uncomment to see the collision box
		#pygame.draw.rect(screen, (255, 0, 0), mainPlayer.getRect())
		pygame.display.update()

		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
				IS_GAME_RUNNING = False
		
		if (pygame.key.get_pressed()[pygame.K_RIGHT] and (mainPlayer.getRect().right) < screen.get_rect().right):
			mainPlayer.move(DIRECTION["RIGHT"])

		elif (pygame.key.get_pressed()[pygame.K_LEFT] and (mainPlayer.getRect().left) > screen.get_rect().left):
			mainPlayer.move(DIRECTION["LEFT"])

		if (pygame.key.get_pressed()[pygame.K_UP] and (mainPlayer.getRect().top) > screen.get_rect().top):
			mainPlayer.move(DIRECTION["TOP"])

		elif (pygame.key.get_pressed()[pygame.K_DOWN] and (mainPlayer.getRect().bottom) < screen.get_rect().bottom):
			mainPlayer.move(DIRECTION["BOTTOM"])


		background.move(DIRECTION["BOTTOM"])
		nextBackground.move(DIRECTION["BOTTOM"])
		if(background.getRect().top > screen.get_rect().bottom):
			background.setLocation(0, -screen.get_height())
			backgroundNode = nextBackgroundNode
			nextBackgroundNode = nextBackgroundNode.next()
			background = backgroundNode.getValue()
			nextBackground = nextBackgroundNode.getValue()

		screen.blits(blit_sequence=[(background.getImage(), background.getRect()), (nextBackground.getImage(), nextBackground.getRect())])

	sys.exit(0)

main()


