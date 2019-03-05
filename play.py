import sys, pygame
import time
from threading import Thread

IS_GAME_RUNNING = True
DIRECTION = {"LEFT": 0, "RIGHT": 1, "TOP": 2, "BOTTOM": 3}


class Background(pygame.sprite.Sprite):
	def __init__(self, imageFile, location):
		pygame.sprite.Sprite.__init__(self)
		self.__image = pygame.image.load(imageFile)
		self.__rect = self.__image.get_rect()
		self.__rect.left, self.__rect.top = location

	def getRect(self):
		return self.__rect

	def getImage(self):
		return self.__image

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
		self._bullets = deque([])
		location = self._player.getRect()
		bullet = Bullet(self._image, location, self._screen)
		self._bulletsToDraw = [bullet] * 1000

	def run(self):
		global IS_GAME_RUNNING

		while(IS_GAME_RUNNING):
			try:
				numBullets = 0
				if (pygame.key.get_pressed()[pygame.K_SPACE]):
					numBullets += 1

					location = self._player.getRect()
					self._bulletsToDraw[numBullets].setLocation(location[0], location[1])
					while(numBullets):

						for bulletsIndx in range(numBullets):
							if (self._bulletsToDraw[bulletsIndx].getRect().bottom > self._screen.get_rect().top):
								self._bulletsToDraw[bulletsIndx].move(DIRECTION["TOP"])
							else :
								del self._bulletsToDraw[bulletsIndx]
								numBullets -= 1	
					
						self._screen.blits(blit_sequence=[self._bulletsToDraw[i].getBulletToDraw() for i in range(numBullets)])
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
	
	global IS_GAME_RUNNING

	screenHeight, screenWidth = 1024, 768
	screen = pygame.display.set_mode((screenHeight, screenWidth))

	pygame.display.set_caption("Small py game demo")

	backgroundTropicalBeach = Background('resources/sprites/background_tropical_beach.jpg', [0, 0])

	startPoint = [0, 200]
	chungus = Player('resources/sprites/chungus.jpg', startPoint, screen)

	while(IS_GAME_RUNNING):

		screen.fill([255, 255, 255])
		screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
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


