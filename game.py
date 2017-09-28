import pygame
import sys
from random import randint, randrange
from creep import Creep


def main():
	# Game parameters
	SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
	BG_COLOR = 30, 145, 50

	pygame.init()
	screen = pygame.display.set_mode(
				(SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
	clock = pygame.time.Clock()

	# Initialize sprites Group
	all_sprites = pygame.sprite.Group()
	red_team = pygame.sprite.Group()
	red_shots = pygame.sprite.Group()
	blue_team = pygame.sprite.Group()
	blue_shots = pygame.sprite.Group()

	'''red_creep = Creep(screen,
						"red_player_images/",
						(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)),
						randrange(0, 360, 9),
						0.18, 50, red_team, red_shots, all_sprites, 'red')'''
	red_creep = Creep(screen,
					  "red_player_images/",
					  (400, 400),
					  0,
					  0.18, 50, red_team, red_shots, all_sprites, 'red')
	blue_creep = Creep(screen,
						"blue_player_images/",
						(400,300),
						45,
						0.18, 50, blue_team, blue_shots, all_sprites, 'blue')
	all_sprites.add(red_creep)
	all_sprites.add(blue_creep)
	red_team.add(red_creep)
	blue_team.add(blue_creep)

	# The main game loop
	#
	register_clock = pygame.time.get_ticks()
	quit = False
	while not quit:
		# Limit frame speed to 50 FPS
		#
		time_passed = clock.tick(50)

		if pygame.time.get_ticks() - register_clock > 1000:
			register_clock = pygame.time.get_ticks()
			#red_creep.get_pixel()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True

		# Redraw the background
		screen.fill(BG_COLOR)

		check_bullet_collisions(red_shots, blue_team)
		check_bullet_collisions(blue_shots, red_team)
		# Check_creeps_collision(red_team, blue_team)
		# Check_players_gone(red_team, blue_team)

		for red_sprite in red_team:
			red_sprite.check_distance(blue_team)
		# Update and redraw all creeps
		for sprite in all_sprites:
			sprite.update(time_passed)
			sprite.blitme()

		pygame.display.flip()

	sys.exit()


def check_bullet_collisions(shots, team):
	for shot in shots:
		hits = pygame.sprite.spritecollide(shot, team, False)
		if hits:
			for hit in hits:
				ming = min((hit.angle - 60), (hit.angle + 60))
				maxg = max((hit.angle - 60), (hit.angle + 60))
				if ming < shot.angle < maxg:
					hit.decrease_health(20)
				else:
					hit.decrease_health(5)
			shot.kill()

def check_creeps_collision(team1, team2):
	print('method "check_creeps_collision" Not implemented yet.')

def check_player_gone(red, blue):
	print('method "check_players_gone" Not implemented yet.')

if __name__ == "__main__":
	main()
