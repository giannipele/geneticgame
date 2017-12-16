import ggutilities

from vec2d import vec2d

SPEED = 30


class Bullet:
    """
        Element that causes damage to another Ominus.
    """

    def __init__(self, pid, x, y, direction, damage, power):
        self.pid = pid
        self.pos = vec2d(x, y)
        self.init_pos = vec2d(x, y)
        self.direction = direction
        self.damage = damage
        self.gone = False
        self.destroy_after = power

    def move(self):
        displacement = vec2d(self.direction.x * SPEED, self.direction.y * SPEED)
        self.pos += displacement
        distance = ggutilities.get_distance(self.init_pos, self.pos)
        if distance > self.destroy_after:
            self.gone = True

    def check_collision(self, ominus_list):
        collisions = []
        for o in ominus_list:
            if o.id == self.pid:
                continue
            if not self.gone:
                distance = ggutilities.get_distance(self.pos, o.pos)
                if distance < 30:
                    o.decrease_health(self.damage)
                    collisions.append(o)
                    self.gone = True

        return collisions


