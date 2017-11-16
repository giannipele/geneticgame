
class Ominus:
	"""
	 	An ominus is a player of the game. This class contains
		all the settings and actions of the Ominus.
	"""

	def __init__(self, id, x, y, direction):
		self.id = id
		self.x = x
		self.y = y
		self.direction = direction

	def print(self):
		print("Omnibus status:")
		print("x: {}".format(self.x))
		print("y: {}".format(self.y))
		print("direction: {}".format(self.direction))



