import sys
import pygame
import ctypes
from threading import Thread

IS_GAME_RUNNING = True
DIRECTION = {"LEFT": 0, "RIGHT": 1, "TOP": 2, "BOTTOM": 3}


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
    def __init__(self, image_file, surface, speed):
        GameObject.__init__(self, image_file, surface)
        self._speed = speed

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
        DynamicGameObject.__init__(self, image_file, surface, speed=2)
        scaled_size = surface.get_size()
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size

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
        DynamicGameObject.__init__(self, image_file, surface, speed)
        scaled_size = self._scale(self._size, 8)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size


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
        bullet.set_location(location.centerx, location.centery)
        surface = self._owner.get_surface()
        targets = self._owner.get_targets()
        damage = self._owner.get_damage()

        if type(self._owner).__name__ == "Player":
            while surface.get_rect().top < bullet.get_rect().bottom:
                bullet.move(direction)
                surface.blit(bullet.get_image(), bullet.get_rect())
                for enemy, enemy_rect in targets.items():
                    if bullet.get_rect().colliderect(enemy_rect):
                        enemy.decrease_health(damage)
                pygame.time.wait(9)
        else:
            while surface.get_rect().bottom > bullet.get_rect().top:
                bullet.move(direction)
                surface.blit(bullet.get_image(), bullet.get_rect())
                for enemy, enemy_rect in targets.items():
                    if bullet.get_rect().colliderect(enemy_rect):
                        enemy.decrease_health(damage)
                pygame.time.wait(9)


class Offensive(Thread):
    def __init__(self, weapon, damage, fire_direction):
        Thread.__init__(self)
        self._current_weapon = weapon
        self._weapons = [weapon]
        self._fire_direction = fire_direction
        self._targets = {}
        self._damage = damage

    def set_fire_direction(self, direction):
        self._fire_direction = direction

    def add_weapon(self, weapon):
        self._weapons.append(weapon)

    def switch_weapon(self, weapon):
        self._current_weapon = weapon

    def add_targets(self, targets):
        self._targets.update(zip(targets, [target.get_rect() for target in targets]))

    def add_target(self, target):
        target_dict = {target: target.get_rect()}
        self._targets.update(target_dict)

    def get_targets(self):
        return self._targets

    def get_damage(self):
        return self._damage

    def run(self):
        global IS_GAME_RUNNING

        print(str(self._current_weapon))

        if type(self).__name__ == "Player":
            while IS_GAME_RUNNING:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self._current_weapon.shoot(self._fire_direction)
        else:
            while IS_GAME_RUNNING:
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


class Actor(DynamicGameObject, Destructible, Offensive):
    def __init__(self, image_file, surface, health, damage, fire_direction, speed, weapon):
        DynamicGameObject.__init__(self, image_file=image_file, surface=surface, speed=speed)
        Destructible.__init__(self, health=health)
        Offensive.__init__(self, damage=damage, fire_direction=fire_direction, weapon=weapon)


class Player(Actor):
    def __init__(self, surface):
        image_file = 'resources/sprites/bear.png'
        bullet = Bullet('resources/sprites/bullet02.png', surface, 60)
        railgun = Railgun(bullet, 100000, self)
        Actor.__init__(self, image_file=image_file, surface=surface, health=100, damage=5,
                       fire_direction=DIRECTION["TOP"], speed=8, weapon=railgun)
        scaled_size = self._scale(self._size, 2)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size


class Enemy(Actor):
    def __init__(self, surface):
        image_file = 'resources/sprites/chungus.jpg'
        bullet = Bullet('resources/sprites/enemy_bullet01.png', surface, 60)
        railgun = Railgun(bullet, 100000, self)
        Actor.__init__(self, image_file=image_file, surface=surface, health=80, damage=1,
                       fire_direction=DIRECTION["BOTTOM"], speed=6, weapon=railgun)
        scaled_size = self._scale(self._size, 6)
        self._image = pygame.transform.scale(self._img, scaled_size)
        self._rect.size = scaled_size


def main():
    pygame.init()

    global IS_GAME_RUNNING

    screen_width, screen_height = 1280, 720
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    if screen_width > 1920 and screen_height > 1080:
        screen_width, screen_height = 1920, 1080
    elif screen_width < 800 and screen_height < 600:
        print("Your screen resolution is too low")
        sys.exit(0)

    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("Small py game demo")

    background01 = Background('resources/sprites/background_space01.jpg', screen)
    background01.set_location(0, 0)
    background02 = Background('resources/sprites/background_space02.jpg', screen)
    background02.set_location(0, screen_height)

    node_background01 = Node(background01)
    node_background02 = Node(background02)
    node_background01.set_next(node_background02)
    node_background02.set_next(node_background01)

    start_point = [screen.get_rect().centerx, screen.get_rect().centery]
    main_player = Player(screen)
    main_player.set_location(start_point[0], start_point[1])
    main_player.start()
    main_player_health_bar = HealthBar('resources/sprites/health_bar.png', screen, main_player)
    main_player_health_bar.set_location(15, 15)

    enemy_start_point = [screen.get_rect().centerx, screen.get_rect().top]
    enemy = Enemy(screen)
    enemy.set_location(enemy_start_point[0], enemy_start_point[1])
    enemy.start()

    main_player.add_target(enemy)
    enemy.add_target(main_player)

    background_node = node_background01
    next_background_node = node_background01.next()
    background = background_node.get_value()
    next_background = next_background_node.get_value()
    background.set_location(0, 0)
    next_background.set_location(0, -screen.get_height())

    while IS_GAME_RUNNING:
        main_player_health_bar.draw_health_bar()
        screen.blit(main_player.get_image(), main_player.get_rect())
        screen.blit(enemy.get_image(), enemy.get_rect())
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
