from gameobject.game_object import GameObject
from utilities import globals


class DynamicGameObject(GameObject):
    def __init__(self, image_file, surface, speed):
        GameObject.__init__(self, image_file, surface)
        self._speed = speed

    def get_speed(self):
        return self._speed

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
