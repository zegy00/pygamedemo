import pygame
from threading import Thread


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
        is_game_running = True

        if type(self).__name__ == "Player":
            while is_game_running:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    is_game_running = False
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self._current_weapon.shoot(self._fire_direction)
        else:
            while is_game_running:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    is_game_running = False
                self._current_weapon.shoot(self._fire_direction)
