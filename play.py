import sys, pygame

DIRECTION = {"LEFT": 0, "RIGHT": 1}


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

class Chungus(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, screen):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self._screen = screen
		self.__image = pygame.transform.scale(img, (int(size[0]//4), int(size[1]//4)))
		self.__colBox = pygame.Rect(location[0], location[1], int(self._screen.get_rect().height//10), int(self._screen.get_rect().width//10))
		self.__speed = 5
		self.__direction = DIRECTION["RIGHT"]

	def getSpeed(self):
		return self.__speed

	def getDir(self):
		return self.__direction

	def getRect(self):
		return self.__colBox

	def getImage(self):
		return self.__image

	def getImagePos(self):
		return pygame.Rect(int((self.__image.get_rect().left) + (self.__colBox.left)) - int(self.__image.get_rect().width/2), int((self.__image.get_rect().top/2) + (self.__colBox.top/2)), self.__image.get_rect().height, self.__image.get_rect().width)

	def setDir(self, direction):
		self.__direction = direction

	def fire(self):
		bullet = BulletChungust('resources/sprites/bullet_couch.png', [self.__sizedImage.top, self.__sizedImage.right])
		if (chungus.getDir() == DIRECTION["RIGHT"]):
			#while(bullet.getRect().left() < )
			#bullet
			# fire to right
			pass

	def move(self, direction):		
		newPos = self.__colBox
		if (direction == DIRECTION["RIGHT"]):
			newPos.right += self.__speed
			self.setDir(DIRECTION["RIGHT"])
		elif (direction == DIRECTION["LEFT"]):
			newPos.left -= self.__speed
			self.setDir(DIRECTION["LEFT"])

		# uncomment to see the collision box
		pygame.draw.rect(self._screen, (255, 0, 0), self.__colBox)
		
		self._screen.blit(self.__image, self.getImagePos())
		pygame.display.update()


class BulletChungus(pygame.sprite.Sprite):
	def __init__(self, imageFile, location):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(imageFile)
		size = img.get_size()
		self.__image = pygame.transform.scale(pygame.image.load(imageFile), (int(size[0]//4), int(size[1]//4)))
		self.__rect = self.__sizedImage.get_rect()
		self.__rect.left, self.__rect.top = location
		self.__speed = 10
		self.__direction = DIRECTION["RIGHT"]

	def getSpeed(self):
		return self.__speed

	def getDir(self):
		return self.__direction

	def getRect(self):
		return self.__rect

	def getImage():
		return self.__image

	def setDir(self, direction):
		self.__direction = direction


def main():
	pygame.init()
	
	screenHeight, screenWidth = 1024, 768
	screen = pygame.display.set_mode((screenHeight, screenWidth))

	pygame.display.set_caption("Small py game demo")

	isGameRunning = True
	backgroundTropicalBeach = Background('resources/sprites/background_tropical_beach.jpg', [0, 0])
	startPoint = [0, 200]
	chungus = Chungus('resources/sprites/chungus.jpg', startPoint, screen)

	while(isGameRunning):

		screen.fill([255, 255, 255])
		screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
		screen.blit(chungus.getImage(), chungus.getImagePos())
		# uncomment to see the collision box
		pygame.draw.rect(screen, (255, 0, 0), chungus.getRect())
		pygame.display.update()

		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
				isGameRunning = False
			if (pygame.key.get_pressed()[pygame.K_SPACE]):
				pass
		
		if (pygame.key.get_pressed()[pygame.K_RIGHT] and (chungus.getRect().right) < screen.get_rect().right):
			print(str(chungus.getRect().right))
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["RIGHT"])

		elif (pygame.key.get_pressed()[pygame.K_LEFT] and (chungus.getRect().left) > screen.get_rect().left):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.getImage(), backgroundTropicalBeach.getRect())
			chungus.move(DIRECTION["LEFT"])



main()


