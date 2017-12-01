from mvc.model.ominus import Ominus
import random as rand

# Screen width and height in pixels
SCREEN_W = 1024
SCREEN_H = 700

FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3


class Model:
	"""
		Model of the game. It contains the engine for
		managing the information of the game.
	"""

	# Incremental Player ID
	IPID = 0

	def __init__(self):
		self.game_field = (SCREEN_W, SCREEN_H)
		self.bg_color = [255, 255, 255, 0]
		self.players = {}
		self.bullets = []

	@staticmethod
	def get_screen_size():
		return SCREEN_W, SCREEN_H

	def tick(self):
		for bullet in self.bullets:
			print("ciao")

		#self.check_collisions()

	def attack(self):
		for p in self.players.values():
			p.attack()


	def add_player(self):
		x = rand.randint(30, SCREEN_W - 30)
		y = rand.randint(30, SCREEN_H - 30)
		angle = rand.randrange(0, 360, 9)
		player = Ominus(self.IPID, x, y, angle, screen=(SCREEN_W, SCREEN_H))
		self.IPID += 1
		self.players[player.id] = player
		print("Player with ID {} added.".format(player.id))

	def remove_player(self, id):
		del self.players[id]
		print("Removed player with ID {}.".format(id))

	def get_players(self):
		return [p for p in self.players.values()]

	def move_player(self, direction):
		for p in self.players.values():
			if direction == FORWARD:
				p.forward()
			elif direction == BACKWARD:
				p.backward()
			elif direction == LEFT:
				p.left()
			elif direction == RIGHT:
				p.right()

	def decrease_health(self):
		deads = []
		for p in self.players.values():
			p.decrease_health(5)
			if p.health <= 0:
				deads.append(p.id)
		for dead in deads:
			del self.players[dead]


if __name__ == "__main__":
	model = Model()
	model.add_player()
	model.add_player()
	model.add_player()
	model.remove_player(1)
