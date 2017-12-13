import time
import ggutilities
from mvc.model.bullet import Bullet
import random as rand


class Weapon:
    """
        The weapon of the Ominus.
    """

    def __init__(self):
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.power = 3
        self.ratio = 0.5
        self.last_shot = time.time()
        self.precision = 16
=======
        self.power = 200
        self.damage = 10
        self.ratio = 0.05
        self.last_shot = time.time()
        self.precision = 20
>>>>>>> changes before start adding the collisions part

    def shoot(self, pid, angle, pos):
        now = time.time()
        if now - self.last_shot > self.ratio:
            self.last_shot = now
            direction = _compute_randrange_direction(self.precision, angle)
            return Bullet(pid, pos.x, pos.y, direction, 20, self.damage, self.power)


def _compute_randrange_direction(precision, angle):
    half_prec = int(precision/2)
    max_angle = angle + half_prec
    min_angle = angle - half_prec
    rand_angle = angle
    if max_angle == min_angle or precision == 1:
        rand_angle = angle
    elif max_angle % 360 < min_angle:
        rand_angle = (rand.uniform(min_angle, angle + precision)) % 360
    elif min_angle < max_angle:
        rand_angle = rand.uniform(min_angle, max_angle)

<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
    return ggutilities.angle_to_direction(rand_angle)
=======
    return _angle_to_direction(rand_angle)


# Convert the angle to the x,y direction
def _angle_to_direction(angle):
    radians = angle * math.pi / 180
    vx = math.cos(radians)
    vy = math.sin(radians)
    return vec2d((vx, vy)).normalized()
>>>>>>> changes before start adding the collisions part
