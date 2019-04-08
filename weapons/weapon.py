import pygame


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
