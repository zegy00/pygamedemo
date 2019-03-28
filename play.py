import sys
import pygame
from threading import Thread

IS_GAME_RUNNING = True
DIRECTION = {"LEFT": 0, "RIGHT": 1, "TOP": 2, "BOTTOM": 3}
screenHeight, screenWidth = 1024, 1024


class Node:
    def __init__(self, dataval):
        self._dataval = dataval
        self._nextval = None

    def set_next(self, nextval):
        self._nextval = nextval

    def next(self):
        return self._nextval

    def get_value(self):
        return self._dataval


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vec2(new_x, new_y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self


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


class DynamicGameObject(GameObject):
    def __init__(self, image_file, screen):
        GameObject.__init__(self, image_file, screen)
        self._speed = 5

    def get_speed(self):
        return self._speed

    def move(self, direction):
        if direction == DIRECTION["RIGHT"]:
            self._rect.right += self._speed
        elif direction == DIRECTION["LEFT"]:
            self._rect.left -= self._speed
        elif direction == DIRECTION["TOP"]:
            self._rect.top -= self._speed
        elif direction == DIRECTION["BOTTOM"]:
            self._rect.bottom += self._speed

        self._surface.blit(self._image, self._rect)


class Background(DynamicGameObject):
    def __init__(self, image_file, surface):
        DynamicGameObject.__init__(self, image_file, surface)
        self._speed = 2

    def move(self, direction):
        if direction == DIRECTION["RIGHT"]:
            self._rect.right += self._speed
        elif direction == DIRECTION["LEFT"]:
            self._rect.left -= self._speed
        elif direction == DIRECTION["TOP"]:
            self._rect.top -= self._speed
        elif direction == DIRECTION["BOTTOM"]:
            self._rect.bottom += self._speed

        self._surface.blit(self._image, self._rect)


class Bullet(DynamicGameObject):
    def __init__(self, image_file, surface, speed):
        DynamicGameObject.__init__(self, image_file, surface)
        scaled_size = self._scale(self._size, 5)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
        self._speed = speed

    def get_bullet_to_draw(self):
        return (self.get_image(), self._rect)


class Weapon:
    def __init__(self, bullet, round_size, owner):
        self._bullet = bullet
        self._round = [bullet] * round_size
        self._owner = owner

    def shoot(self, direction):
        pass


class Railgun(Weapon):
    def __init__(self, bullet, round_size, owner):
        Weapon.__init__(self, bullet, round_size, owner)

    def shoot(self, direction):
        bullet = self._round.pop()
        location = self._owner.get_rect()
        bullet.set_location(location.centerx, location.top)
        surface = self._owner.get_surface()
        while surface.get_rect().contains(bullet.get_rect()):
            bullet.move(direction)
            surface.blit(bullet.get_image(), bullet.get_rect())
            pygame.time.wait(9)


class Arsenal(Thread):
    def __init__(self, weapon, direction):
        Thread.__init__(self)
        self._current_weapon = weapon
        self._weapons = []
        self._fire_direction = direction
        self.add_weapon(weapon)
        self.set_fire_direction(direction)

    def set_fire_direction(self, direction):
        self._fire_direction = direction

    def add_weapon(self, weapon):
        self._weapons.append(weapon)

    def switch_weapon(self, weapon):
        self._current_weapon = weapon

    def run(self):
        global IS_GAME_RUNNING

        while IS_GAME_RUNNING:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self._current_weapon.shoot(self._fire_direction)


class Destructible:
    def __init__(self, health):
        self._health = health
        self._current_health = health

    def decrease_health(self, health_points):
        if isinstance(health_points, int) and health_points > 0 and health_points < 10000:
            self._current_health -= health_points
            if self._current_health < 0:
                self._current_health = 0
        else:
            print("Destructible points should be of integer type and in range 0-10000")

    def increase_health(self, health_points):
        if isinstance(health_points, int) and health_points > 0 and health_points < 10000:
            self._current_health += health_points
            if self._current_health > self._health:
                self._current_health = self._health
        else:
            print("Destructible points should be of integer type and in range 0-10000")

    def get_health(self):
        return self._health

    def get_current_health(self):
        return self._current_health

    def get_current_hp_percentage(self):
        return (self._current_health * 100) / self._health


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


class Player(DynamicGameObject, Destructible):
    def __init__(self, image_file, surface, health):
        DynamicGameObject.__init__(self, image_file, surface)
        Destructible.__init__(self, health)
        scaled_size = self._scale(self._size, 2)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size
        self._speed = 8
        bullet = Bullet('resources/sprites/bullet02.png', self._surface, 60)
        railgun = Railgun(bullet, 100000, self)
        self._arsenal = Arsenal(railgun, DIRECTION["TOP"])
        self._arsenal.start()


def main():
    pygame.init()

    global IS_GAME_RUNNING, screenHeight, screenWidth

    screen = pygame.display.set_mode((screenHeight, screenWidth))

    pygame.display.set_caption("Small py game demo")

    background01 = Background('resources/sprites/background_space01.jpg', screen)
    background01.set_location(0, 0)
    background02 = Background('resources/sprites/background_space02.jpg', screen)
    background02.set_location(0, screenHeight)

    node_background01 = Node(background01)
    node_background02 = Node(background02)
    node_background01.set_next(node_background02)
    node_background02.set_next(node_background01)

    start_point = [400, 200]
    main_player = Player('resources/sprites/chungus.png', screen, 100)
    main_player.set_location(start_point[0], start_point[1])
    main_player_health_bar = HealthBar('resources/sprites/health_bar.png', screen, main_player)
    main_player_health_bar.set_location(15, 15)

    background_node = node_background01
    next_background_node = node_background01.next()
    background = background_node.get_value()
    next_background = next_background_node.get_value()
    background.set_location(0, 0)
    next_background.set_location(0, -screen.get_height())

    while IS_GAME_RUNNING:

        screen.blit(main_player.get_image(), main_player.get_rect())
        main_player_health_bar.draw_health_bar()
        pygame.display.update()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and
                pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
                IS_GAME_RUNNING = False

        if pygame.key.get_pressed()[pygame.K_RIGHT] and (main_player.get_rect().right < screen.get_rect().right):
            main_player.move(DIRECTION["RIGHT"])

        elif pygame.key.get_pressed()[pygame.K_LEFT] and (main_player.get_rect().left > screen.get_rect().left):
            main_player.move(DIRECTION["LEFT"])

        if pygame.key.get_pressed()[pygame.K_UP] and (main_player.get_rect().top > screen.get_rect().top):
            main_player.move(DIRECTION["TOP"])

        elif pygame.key.get_pressed()[pygame.K_DOWN] and (main_player.get_rect().bottom < screen.get_rect().bottom):
            main_player.move(DIRECTION["BOTTOM"])

        background.move(DIRECTION["BOTTOM"])
        next_background.move(DIRECTION["BOTTOM"])
        if background.get_rect().top > screen.get_rect().bottom:
            background.set_location(0, -screen.get_height())
            background_node = next_background_node
            next_background_node = next_background_node.next()
            background = background_node.get_value()
            next_background = next_background_node.get_value()

        screen.blits(blit_sequence=[(background.get_image(), background.get_rect()),
                                    (next_background.get_image(), next_background.get_rect())])

    sys.exit(0)


main()
