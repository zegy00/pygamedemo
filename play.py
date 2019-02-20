import sys, pygame

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class Chungus(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.__image = pygame.image.load(image_file)
		self.rect = self.__image.get_rect()
		self.rect.left, self.rect.top = location
		self.size = self.__image.get_size()
		self.image = pygame.transform.scale(self.__image, (int(self.size[0]//4), int(self.size[1]//4)))
		self._speed = 5

	def getSpeed(self):
		return self._speed


def main():
	pygame.init()
	
	screenHeight, screenWidth = 1024, 768
	screen = pygame.display.set_mode((screenHeight, screenWidth))

	pygame.display.set_caption("Small py game demo")

	isGameRunning = True
	backgroundTropicalBeach = Background('resources/sprites/background_tropical_beach.jpg', [0, 0])
	startPoint = [0, 200]
	chungus = Chungus('resources/sprites/chungus.jpg', startPoint)

	while(isGameRunning):

		screen.fill([255, 255, 255])
		screen.blit(backgroundTropicalBeach.image, backgroundTropicalBeach.rect)
		screen.blit(chungus.image, chungus.rect)
		pygame.display.update()

		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
				isGameRunning = False
		
		if (pygame.key.get_pressed()[pygame.K_RIGHT]):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.image, backgroundTropicalBeach.rect)
			moveRightPos = chungus.rect
			moveRightPos.right += chungus.getSpeed()
			screen.blit(chungus.image, moveRightPos)
			pygame.display.update()
		elif (pygame.key.get_pressed()[pygame.K_LEFT]):
			screen.fill([255, 255, 255])
			screen.blit(backgroundTropicalBeach.image, backgroundTropicalBeach.rect)
			moveLeftPos = chungus.rect
			moveLeftPos.left -= chungus.getSpeed()
			screen.blit(chungus.image, moveLeftPos)
			pygame.display.update()


main()


