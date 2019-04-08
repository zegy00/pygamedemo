import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_file, surface):
        pygame.sprite.Sprite.__init__(self)
        self._img = pygame.image.load(image_file)
        self._size = self._img.get_size()
        self._surface = surface
        self._image = pygame.transform.scale(self._img, self._size)
        self._rect = self._image.get_rect()

    def _scale(self, size, divider):
        return (int(size[0] / divider)), int((size[1] / divider))

    def get_rect(self):
        return self._rect

    def set_location(self, left, top):
        self._rect.left = left
        self._rect.top = top

    def get_image(self):
        return self._image

    def get_surface(self):
        return self._surface

