import math
from mvc.model.ominus import Ominus

# Screen width and height in pixels
SCREEN_W = 1024
SCREEN_H = 768


class Model:
	"""
		Model of the game. It contains the engine for
		managing the information of the game.
	"""

	# Incremental Player ID
	IPID = 0

	def __init__(self):
		self.game_field = (SCREEN_W, SCREEN_H)
		self.color = [255, 255, 255, 0]
		self.players = {}

	def add_player(self):
		player = Ominus(self.IPID, 100, 100, 0)
		self.players[self.IPID] = player
		print("Player with ID {} added.".format(self.IPID))
		self.IPID += 1

	def remove_player(self, id):
		del self.players[id]
		print("Removed player with ID {}.".format(id))


def _angle_to_radians(angle):
	return angle * math.pi / 180


def _radians_to_angle(rad):
	return rad * 180 / math.pi


def _get_distance(p1, p2):
	return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


if __name__ == "__main__":
	model = Model()
	model.add_player()
	model.add_player()
	model.add_player()
	model.remove_player(1)
