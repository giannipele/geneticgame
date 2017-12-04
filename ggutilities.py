import math
from vec2d import vec2d


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