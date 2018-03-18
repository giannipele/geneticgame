import time
import ggutilities
from mvc.model.bullet import Bullet
import random as rand
import math


class Weapon:
    """
        The weapon of the Ominus.
    """

    def __init__(self):
        self.power = 400
        self.damage = 2
        self.ratio = 0.1
        self.precision = 7
        self.last_shot = time.time()

    def shoot(self, pid, angle, pos):
        """
        Shot a bullet in the direction pointed by the ominus.
        :param pid: Id of the ominus
        :param angle: angle of the ominus
        :param pos: x,y position of the ominus
        :return: created Bullet object
        """
        now = time.time()
        if now - self.last_shot > self.ratio:
            self.last_shot = now
            direction = _compute_randrange_direction(self.precision, angle - 3)
            centerx = pos.x + 30 * math.cos(ggutilities.angle_to_radians(angle + 90))
            centery = pos.y + 30 * math.sin(ggutilities.angle_to_radians(angle + 90))
            return Bullet(pid, centerx, centery, direction, self.damage, self.power)


def _compute_randrange_direction(precision, angle):
    """
    Introduce random noise in the direction of the shot, to make the ominus less accurate.
    :param precision: percentage of the precision of the ominus
    :param angle: angle of generation of the noise
    :return: a random direction within a certain range
    """
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

