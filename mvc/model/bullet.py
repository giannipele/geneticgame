from vec2d import vec2d
import math


class Bullet:
	def __init__(self, pid, x, y, direction, speed):
		self.pid = pid
		self.pos = vec2d(x, y)
		self.init_pos = vec2d(x, y)
		self.direction = direction
		self.speed = speed
		self.gone = False

	def move(self):
		displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
		self.pos += displacement
		distance = _get_distance(self.init_pos, self.pos)
		if distance > 100:
			self.gone = True


# Get ditstance between two points
def _get_distance(p1, p2):
	return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


