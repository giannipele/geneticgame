import time
import ggutilities
from mvc.model.bullet import Bullet
import random as rand


class Weapon:
    """
        The weapon of the Ominus.
    """

    def __init__(self):
        self.power = 400
        self.damage = 3
        self.ratio = 0.1
        self.precision = 7
        self.last_shot = time.time()

    def shoot(self, pid, angle, pos):
        now = time.time()
        if now - self.last_shot > self.ratio:
            self.last_shot = now
            direction = _compute_randrange_direction(self.precision, angle)
            return Bullet(pid, pos.x, pos.y, direction, self.damage, self.power)


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

    return ggutilities.angle_to_direction(rand_angle)

