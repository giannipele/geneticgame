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

	def __init__(self):
		self.game_field = (SCREEN_W, SCREEN_H)
		self.color = [255, 255, 255, 0]
		self.players = {}

	def add_player(self):
		player = Ominus(100, 100, 0)
		self.players[player.id] = player
		print("Player with ID {} added.".format(player.id))

	def remove_player(self, id):
		del self.players[id]
		print("Removed player with ID {}.".format(id))


if __name__ == "__main__":
	model = Model()
	model.add_player()
	model.add_player()
	model.add_player()
	model.remove_player(1)
