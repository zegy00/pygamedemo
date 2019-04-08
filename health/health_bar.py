from gameobject.game_object import GameObject
import pygame


class HealthBar(GameObject):
    def __init__(self, image_file, surface, player):
        GameObject.__init__(self, image_file, surface)
        scaled_size = self._scale(self._size, 4)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
        self._rectWidthMax = self._rect.width
        self._color = (237, 41, 57)
        self._player = player

    def _get_rectangle_percentage(self):
        cur_hp_percentage = self._player.get_current_hp_percentage()
        return (cur_hp_percentage / 100) * self._rectWidthMax

    def __adjust_health_bar(self):
        self._rect.width = int(self._get_rectangle_percentage())

    def draw_health_bar(self):
        self.__adjust_health_bar()
        pygame.draw.ellipse(self._surface, self._color, self._rect)
        self._surface.blit(self._image, self._rect)

