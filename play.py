import sys, pygame
import time
from threading import Thread
#from threading import activeCount
#from threading import Event

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

	def getRect(self):
		return self._colBox

	def setRect(self, rect):
		self._colBox = rect

	def getImage(self):
		return self._image

	def getImagePos(self):
		return pygame.Rect((int((self._image.get_rect().left) + (self._colBox.left)) - int(self._image.get_rect().width/2)) + int(self._colBox.width/2), 
							(int((self._image.get_rect().top) + (self._colBox.top)) - int(self._image.get_rect().height/2)) + int(self._colBox.height/2),
							self._image.get_rect().height,
							self._image.get_rect().width)


class Bullet(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self._image = pygame.transform.scale(img, (int(size[0]//4), int(size[1]//4)))
		self._colBox = pygame.Rect(location[0], location[1], int(self._screen.get_rect().height//16), int(self._screen.get_rect().width//16))
		self._speed = 10

	def getSpeed(self):
		return self._speed


class Bullets(Thread):
	def __init__(self, imageFile, screen, player):
		Thread.__init__(self)
		self._image = imageFile
		self._screen = screen
		self._player = player

	def getSpeed(self):
		return self._speed

	def run(self):
		global IS_GAME_RUNNING

		while(IS_GAME_RUNNING):
			if (pygame.key.get_pressed()[pygame.K_SPACE]):
				location = self._player.getRect()
				bullet = Bullet(self._image, location, self._screen)
				while(bullet.getRect().bottom > self._screen.get_rect().top):
					print("FIRE!")
					newPos = bullet.getRect()
					#newPos.left = (int((self._image.get_rect().left) + (self._colBox.left)) - int(self._image.get_rect().width/2)) + int(self._colBox.width/2)
					newPos.top -= bullet.getSpeed()

					# uncomment to see the collision box
					#pygame.draw.rect(self._screen, (255, 0, 0), newPos)
		
					self._screen.blit(bullet.getImage(), bullet.getImagePos())

					#time.sleep(150)


class Player(GameObject):
	def __init__(self, imageFile, location, screen):
		GameObject.__init__(self, imageFile, location, screen)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self._image = pygame.transform.scale(img, (int(size[0]//4), int(size[1]//4)))
		self._colBox = pygame.Rect(location[0], location[1], int(self._screen.get_rect().height//6), int(self._screen.get_rect().width//4))
		self.__speed = 5
		self._bullets = Bullets('resources/sprites/bullet01.png', self._screen, self)
		self._bullets.start()

	def getSpeed(self):
		return self.__speed

	def getDir(self):
		return self.__direction

	def move(self, direction):		
		newPos = self._colBox
		if (direction == DIRECTION["RIGHT"]):
			newPos.right += self.__speed
		elif (direction == DIRECTION["LEFT"]):
			newPos.left -= self.__speed
		elif (direction == DIRECTION["TOP"]):
			newPos.top -= self.__speed
		elif (direction == DIRECTION["BOTTOM"]):
			newPos.bottom += self.__speed

		# uncomment to see the collision box
		#pygame.draw.rect(self._screen, (255, 0, 0), newPos)
		
		self._screen.blit(self._image, self.getImagePos())
		pygame.display.update()


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
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["RIGHT"])

		elif (pygame.key.get_pressed()[pygame.K_LEFT] and (chungus.getRect().left) > screen.get_rect().left):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["LEFT"])

		if (pygame.key.get_pressed()[pygame.K_UP] and (chungus.getRect().top) > screen.get_rect().top):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["TOP"])

		elif (pygame.key.get_pressed()[pygame.K_DOWN] and (chungus.getRect().bottom) < screen.get_rect().bottom):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["BOTTOM"])

	sys.exit(0)

main()


