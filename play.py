import sys, pygame
pygame.init()

screenHeight, screenWidth = 1280, 720
screen = pygame.display.set_mode((screenHeight, screenWidth))

pygame.display.set_caption("Small py game demo")

isGameRunning = True

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

while(isGameRunning):
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
			isGameRunning = False

	backgroundTropicalBeach = Background('resources/sprites/background_tropical_beach.jpg', [0, 0])
	screen.fill([255, 255, 255])
	screen.blit(backgroundTropicalBeach.image, backgroundTropicalBeach.rect)

	chungus = Chungus('resources/sprites/chungus.jpg', [0, 0])
	screen.blit(chungus.image, chungus.rect)