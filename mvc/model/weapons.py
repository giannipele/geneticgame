from mvc.model.bullet import Bullet
import time


class Weapon:
	"""
		The weapon of the Ominus.
	"""

	def __init__(self):
		self.power = 10
		self.ratio = 1
		self.last_shot = time.time()
		self.counter = 0

	def shoot(self, pid, direction, pos):
		now = time.time()
		#print(now - self.last_shot)
		if now - self.last_shot > self.ratio:
			self.last_shot = now
			self.counter += 1
			#return Bullet(pid, )


