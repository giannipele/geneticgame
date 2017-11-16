import math
from vec2d import vec2d

# Stepsize in degrees of the angle to turn the ominus
STEP_ANGLE = 9


class Ominus:
	"""
	 	An ominus is a player of the game. This class contains
		all the settings and actions of the Ominus.
	"""

	# Incremental Player ID
	IPID = 0

	def __init__(self, x, y, angle):
		self.id = self.IPID
		self.IPID += 1
		self.pos = vec2d(x, y)
		self.angle = angle
		self.direction = _angle_to_direction(angle)
		self.speed = 5

	def print(self):
		print("Omnibus status:")
		print("position: ({}, {})".format(self.pos.x, self.pos.y))
		print("angle: {}".format(self.angle))
		print("------------------------\n")

	def forward(self):
		displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
		self.pos += displacement

	def backward(self):
		displacement = vec2d(-self.direction.x * self.speed, -self.direction.y * self.speed)
		self.pos += displacement

	def right(self):
		self.angle = (self.angle + STEP_ANGLE) % 360
		self.direction = _angle_to_direction(self.angle)

	def left(self):
		self.angle = (self.angle - STEP_ANGLE) % 360
		self.direction = _angle_to_direction(self.angle)


def _angle_to_direction(angle):
	radians = angle * math.pi / 180
	vx = math.cos(radians)
	vy = math.sin(radians)
	return vec2d((vx, vy)).normalized()


def _angle_to_radians(angle):
	return angle * math.pi / 180


def _radians_to_angle(rad):
	return rad * 180 / math.pi


def _get_distance(p1, p2):
	return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


if __name__ == "__main__":
	ominus = Ominus(100, 100, 90)
	ominus.print()
	ominus.forward()
	ominus.print()
	ominus.backward()
	ominus.print()
	ominus.right()
	ominus.print()
	ominus.left()
	ominus.print()


