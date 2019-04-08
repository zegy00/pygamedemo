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
