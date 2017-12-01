from vec2d import vec2d


class Bullet:
	def __init__(self, pos, direction, speed):
		self.pos = pos
		self.init_pos = pos
		self.direction = direction
		self.speed = speed

	def move(self):
		displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
		self.pos += displacement


