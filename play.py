import sys, pygame
pygame.init()

screenHeight, screenWidth = 640, 480
screen = pygame.display.set_mode((screenHeight, screenWidth))

pygame.display.set_caption("Small py game demo")

isGameRunning = True

while(isGameRunning):
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
			isGameRunning = False