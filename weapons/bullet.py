from gameobject.dynamic_game_object import DynamicGameObject
import pygame


class Bullet(DynamicGameObject):
    def __init__(self, image_file, surface, speed):
        DynamicGameObject.__init__(self, image_file, surface, speed)
        scaled_size = self._scale(self._size, 8)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
