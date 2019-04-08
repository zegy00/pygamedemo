from gameobject import dynamic_game_object
from health import destructible
from weapons import offensive


class Actor(dynamic_game_object.DynamicGameObject, destructible.Destructible, offensive.Offensive):
    def __init__(self, image_file, surface, health, damage, fire_direction, speed, weapon):
        dynamic_game_object.DynamicGameObject.__init__(self, image_file=image_file, surface=surface, speed=speed)
        destructible.Destructible.__init__(self, health=health)
        offensive.Offensive.__init__(self, damage=damage, fire_direction=fire_direction, weapon=weapon)
