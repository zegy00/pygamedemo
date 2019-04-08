from gameobject.dynamic_game_object import DynamicGameObject
from utilities import globals
import pygame


class Background(DynamicGameObject):
    def __init__(self, image_file, surface):
        DynamicGameObject.__init__(self, image_file, surface, speed=2)
        scaled_size = surface.get_size()
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size

    def move(self, direction):
        if direction == globals.DIRECTION["RIGHT"]:
            self._rect.right += self._speed
        elif direction == globals.DIRECTION["LEFT"]:
            self._rect.left -= self._speed
        elif direction == globals.DIRECTION["TOP"]:
            self._rect.top -= self._speed
        elif direction == globals.DIRECTION["BOTTOM"]:
            self._rect.bottom += self._speed

        self._surface.blit(self._image, self._rect)
