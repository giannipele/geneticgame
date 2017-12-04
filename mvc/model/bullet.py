import ggutilities

from vec2d import vec2d

DESTROY_AFTER = 400


class Bullet:
    """
        Element that causes damage to another Ominus.
    """

    def __init__(self, pid, x, y, direction, speed, damage):
        self.pid = pid
        self.pos = vec2d(x, y)
        self.init_pos = vec2d(x, y)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.gone = False

    def move(self):
        displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
        self.pos += displacement
        distance = ggutilities.get_distance(self.init_pos, self.pos)
        if distance > DESTROY_AFTER:
            self.gone = True

