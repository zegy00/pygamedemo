import pygame
from gameobject.game_object import GameObject


class GameObjectMock(GameObject):
    def __init__(self, image_file, surface):
        GameObject.__init__(self, image_file=image_file, surface=surface)

    def scale(self, size, divider):
        return self._scale(size, divider)


class TestGameObject:
    def test_scale(self):
        size = (40, 40)
        my_game_object = GameObjectMock("resources/sprites/background_space01.jpg", None)
        assert my_game_object.scale(size, 2) == (20, 20)
        size = (-40, -40)
        assert my_game_object.scale(size, 2) == -1

    def test_get_rect(self):
        my_game_object = GameObjectMock("resources/sprites/background_space01.jpg", None)
        my_game_object.set_rect(pygame.Rect(50, 50, 100, 100))
        assert my_game_object.get_rect() == pygame.Rect(50, 50, 100, 100)

