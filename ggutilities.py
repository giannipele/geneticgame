import math
from vec2d import vec2d


def angle_to_direction(angle):
    """
    Convert the angle to the normalized x,y direction,
    :param angle:
    :return:
    """
    radians = angle * math.pi / 180
    vx = math.cos(radians)
    vy = math.sin(radians)
    return vec2d((vx, vy)).normalized()


def angle_to_radians(angle):
    """
    Convert an angle into radians.
    :param angle:
    :return: radians
    """
    return angle * math.pi / 180


def _radians_to_angle(rad):
    """
    Convert radians into angle
    :param rad:
    :return: angle
    """
    return rad * 180 / math.pi


def get_distance(p1, p2):
    """
    Calculate the distance of two points.
    :param p1: point 1
    :param p2: point 2
    :return: euclidean distance of the two points
    """
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def line_intersect_circle(Q, r, segment):
    """
    Verifies if a line crosses a circle.
    :param Q:
    :param r:
    :param segment:
    :return: true if the segment passes inside the circle, false otherwise.
    """
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


def point_inside_rect(pos, x, y, w, h):
    """
    Verifies if a line crosses a rectangle.
    :param pos:
    :param x:
    :param y:
    :param w:
    :param h:
    :return: true if a point is inside a rectangular, false otherwise
    """
    if x <= pos.x <= x + w and y <= pos.y <= y + h:
        return True
    return False

