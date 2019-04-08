from actors.actor import Actor
from weapons.bullet import Bullet
from weapons.weapon import Railgun
from utilities import globals
import pygame


class Player(Actor):
    def __init__(self, surface):
        image_file = 'resources/sprites/bear.png'
        bullet = Bullet('resources/sprites/bullet02.png', surface, 60)
        railgun = Railgun(bullet, 100000, self)
        Actor.__init__(self, image_file=image_file, surface=surface, health=100, damage=5,
                       fire_direction=globals.DIRECTION["TOP"], speed=8, weapon=railgun)
        scaled_size = self._scale(self._size, 2)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
