from mvc.model.bullet import Bullet
import time


class Weapon:
	"""
		The weapon of the Ominus.
	"""

	def __init__(self):
		self.power = 10
		self.ratio = 0.05
		self.last_shot = time.time()

	def shoot(self, pid, direction, pos):
		now = time.time()
		#print(now - self.last_shot)
		if now - self.last_shot > self.ratio:
			self.last_shot = now
			return Bullet(pid, pos.x, pos.y, direction, 10)


