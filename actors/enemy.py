from actors.actor import Actor
from weapons.bullet import Bullet
from weapons.weapon import Railgun
from utilities import globals
import pygame


class Enemy(Actor):
    def __init__(self, surface):
        image_file = 'resources/sprites/chungus.jpg'
        bullet = Bullet('resources/sprites/enemy_bullet01.png', surface, 60)
        railgun = Railgun(bullet, 100000, self)
        Actor.__init__(self, image_file=image_file, surface=surface, health=80, damage=1,
                       fire_direction=globals.DIRECTION["BOTTOM"], speed=6, weapon=railgun)
        scaled_size = self._scale(self._size, 6)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
