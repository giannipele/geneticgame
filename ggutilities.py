import math
from vec2d import vec2d
import numpy as np


# Convert the angle to the x,y direction
def angle_to_direction(angle):
    radians = angle * math.pi / 180
    vx = math.cos(radians)
    vy = math.sin(radians)
    return vec2d((vx, vy)).normalized()


# Convert angle into radians
def angle_to_radians(angle):
    return angle * math.pi / 180


# Convert radians into angle
def _radians_to_angle(rad):
    return rad * 180 / math.pi


# Get ditstance between two points
def get_distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


# Return True if the segment passes inside the circle, false otherwise
def intersect(Q, r, segment):
    P1 = vec2d(segment[0])
    V = vec2d(segment[1]) - vec2d(P1)

    a = V.dot([V.x, V.y])
    l = P1 - Q
    b = 2 * V.dot([l.x, l.y])
    c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r ** 2

    disc = b ** 2 - 4 * a * c
    if disc < 0:
        return False, None

    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return False, None

    t = max(0, min(1, - b / (2 * a)))
    return True, P1 + t * V


def isInside(pos, x, y, w, h):
    if x <= pos.x <= x + w and y < pos.y < y + h:
        return True
    return False

