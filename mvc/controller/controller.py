import pygame

FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3


class Controller:
	def __init__(self, model, view):
		self.model = model
		self.view = view

	def run(self):
		clock = pygame.time.Clock()
		register_clock = pygame.time.get_ticks()
		quit = False

		while not quit:
			time_passed = clock.tick(50)
			if pygame.time.get_ticks() - register_clock > 1000:
				register_clock = pygame.time.get_ticks()
			key = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
			if key[pygame.K_ESCAPE]:
				quit = True
			if key[pygame.K_DOWN]:
				self.model.move_player(BACKWARD)
			elif key[pygame.K_UP]:
				self.model.move_player(FORWARD)
			if key[pygame.K_RIGHT]:
				self.model.move_player(RIGHT)
			elif key[pygame.K_LEFT]:
				self.model.move_player(LEFT)
			#elif key[pygame.K_SPACE]:
			#	self.model.decrease_health()
			self.view.tick()
