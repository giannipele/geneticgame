import pygame
from pygame import Color, Rect
from pygame.sprite import Sprite
from vec2d import vec2d
import math
from glob import glob
import os



class Weapon(Sprite):
	"""A sprite that is shooted by the Creep, used to hit
	   another player
	"""

	def __init__(self, screen, angle, init_position):
		Sprite.__init__(self)
		self.screen = screen
		self.init_position = vec2d(init_position)
		self.direction = _angle_to_direction(angle)
		self.angle = angle
		self.pos = vec2d(init_position)
		self.image = pygame.image.load("bullet.png")
		self.rect = self.image.get_rect()
		self.speed = 15

	def blitme(self):
		self.rect = self.image.get_rect().move(
			self.pos.x - self.rect.width / 2,
			self.pos.y - self.rect.height / 2)
		self.screen.blit(self.image, self.rect)
		pygame.draw.rect(self.screen, (255, 0, 255), self.rect)

	def update(self, time_passed):
		displacement = vec2d(
			self.direction.x * self.speed,
			self.direction.y * self.speed)
		self.pos += displacement
		shot_range = self._get_distance(self.pos, self.init_position)
		if shot_range > 50:
			self.kill()

	def _get_distance(self, pos1, pos2):
		return math.sqrt(math.pow(pos1.x - pos2.x, 2) + math.pow(pos1.y - pos2.y, 2))


class Sight(pygame.Surface):
	def __init__(self, parent, width, height):
		super(Sight, self).__init__((width, height))
		self.width = width
		self.height = height
		self.parent = parent
		self.ro = math.atan(width/height)
		self.p = math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2))

	def update_coordinates(self, x, y, angle):
		self.x = int(x + (36 + (self.height/2)) * math.cos(_angle_to_radians(angle)))
		self.y = int(y + (36 + (self.height/2)) * math.sin(_angle_to_radians(angle)))
		self.angle = angle

	def update(self):
		angle2 = math.pi - self.ro
		angle3 = math.pi + self.ro
		angle4 = -self.ro
		x1 = int(self.x + self.p * math.cos(self.ro + _angle_to_radians(self.angle)))
		y1 = int(self.y + self.p * math.sin(self.ro + _angle_to_radians(self.angle)))
		x2 = int(self.x + self.p * math.cos(angle2 + _angle_to_radians(self.angle)))
		y2 = int(self.y + self.p * math.sin(angle2 + _angle_to_radians(self.angle)))
		x3 = int(self.x + self.p * math.cos(angle3 + _angle_to_radians(self.angle)))
		y3 = int(self.y + self.p * math.sin(angle3 + _angle_to_radians(self.angle)))
		x4 = int(self.x + self.p * math.cos(angle4 + _angle_to_radians(self.angle)))
		y4 = int(self.y + self.p * math.sin(angle4 + _angle_to_radians(self.angle)))
		#pygame.draw.circle(self.parent, (255, 255, 255), (self.x, self.y), 10)
		#pygame.draw.circle(self.parent, (255, 255, 255), (x1, y1), 10)
		#pygame.draw.circle(self.parent, (255, 255, 255), (x2, y2), 10)
		pygame.draw.polygon(self.parent, (255, 255, 255), [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], 1)


class Creep(Sprite):
	""" A creep sprite that bounces off walls and changes its
        direction from time to time.
    """

	def __init__(
			self, screen, imgs_filename, init_position,
			angle_direction, speed, health, team, shots, all_sprites, team_color):
		""" Create a new Creep.

            screen:
                The screen on which the creep lives (must be a
                pygame Surface object, such as pygame.display)

            img_filaneme:
                Image file for the creep.

            init_position:
                A vec2d or a pair specifying the initial position
                of the creep on the screen.

            init_direction:
                A vec2d or a pair specifying the initial direction
                of the creep. Must have an angle that is a
                multiple of 45 degres.

            speed:
                Creep speed, in pixels/millisecond (px/ms)
        """
		Sprite.__init__(self)
		self.screen = screen
		self.images = self._load_images(imgs_filename)
		self.spear_images = self._load_images("spear_images/")
		self.pos = vec2d(init_position)
		self.angle = angle_direction
		self.direction = _angle_to_direction(angle_direction)
		self.speed = speed
		self.image = self.images[self.angle]
		self.rect = self.image.get_rect()
		self.health = health
		self.max_health = health
		self.team = team
		self.shots = shots
		self.all_sprites = all_sprites
		self.last_shot = 0.0
		self.team_color = team_color
		self.sight = Sight(self.screen, 400, 300)

	def blitme(self):
		""" Blit the creep onto the screen that was provided in
		the constructor.
	"""
		# The creep image is placed at self.pos.
		# To allow for smooth movement even when the creep rotates
		# and the image size changes, its placement is always
		# centered.
		#
		self.rect = self.image.get_rect().move(
			self.pos.x - self.rect.width / 2,
			self.pos.y - self.rect.height / 2)
		# When the image is rotated, its size is changed.
		# We must take the size into account for detecting
		# collisions with the walls.
		#

		bounds_rect = self.screen.get_rect().inflate(
			-self.rect.width, -self.rect.height)

		if self.pos.x < bounds_rect.left:
			self.pos.x = bounds_rect.left
		elif self.pos.x > bounds_rect.right:
			self.pos.x = bounds_rect.right
		if self.pos.y < bounds_rect.top:
			self.pos.y = bounds_rect.top
		elif self.pos.y > bounds_rect.bottom:
			self.pos.y = bounds_rect.bottom

		# Health semi circle always on the back of the sprite
		self.update_health_bar()
		# Draw creep's spear
		self.update_spear()

		#self.update_sight()
		self.update_sight_vectors()
		#pygame.draw.rect(self.screen, (255,255,255), Rect((self.sight.x, self.sight.y), (self.sight.width, self.sight.height)))
		self.screen.blit(self.image, self.rect)

	def update(self, time_passed):
		""" Handles Keys """
		key = pygame.key.get_pressed()
		if self.team_color == 'red':
			if key[pygame.K_DOWN]:  # down key
				self.action('MOVE_BACK', time_passed)
			elif key[pygame.K_UP]:  # up key
				self.action('MOVE_FORWARD', time_passed)
			if key[pygame.K_RIGHT]:  # right key
				self.action('TURN_RIGHT', time_passed)
			elif key[pygame.K_LEFT]:  # left key
				self.action('TURN_LEFT', time_passed)
			elif key[pygame.K_SPACE]:
				self.action('SHOOT', time_passed)
		elif self.team_color == 'blue':
			if key[pygame.K_s]:  # down key
				self.action('MOVE_BACK', time_passed)
			elif key[pygame.K_w]:  # up key
				self.action('MOVE_FORWARD', time_passed)
			if key[pygame.K_d]:  # right key
				self.action('TURN_RIGHT', time_passed)
			elif key[pygame.K_a]:  # left key
				self.action('TURN_LEFT', time_passed)
			elif key[pygame.K_c]:
				self.action('SHOOT', time_passed)

	def action(self, action, time_passed):
		if action == 'MOVE_BACK':  # down key
			displacement = vec2d(
				-self.direction.x * self.speed * time_passed,
				-self.direction.y * self.speed * time_passed)
			self.pos += displacement
		elif action == 'MOVE_FORWARD':  # up key
			displacement = vec2d(
				self.direction.x * self.speed * time_passed,
				self.direction.y * self.speed * time_passed)
			self.pos += displacement
		if action == 'TURN_RIGHT':  # right key
			self.angle = (self.angle + 9) % 360
			self.direction = _angle_to_direction(self.angle)
			self.image = self.images[self.angle]
		elif action == 'TURN_LEFT':  # left key
			self.angle = (self.angle - 9) % 360  # move left
			self.direction = _angle_to_direction(self.angle)
			self.image = self.images[self.angle]
		elif action == 'SHOOT':
			if pygame.time.get_ticks() - self.last_shot > 500:
				self.shoot()

	def shoot(self):
		self.last_shot = pygame.time.get_ticks()
		bullet = Weapon(self.screen, self.angle, (self.pos.x, self.pos.y))
		self.shots.add(bullet)
		self.all_sprites.add(bullet)

	def decrease_health(self, damage):
		self.health -= damage
		print(self.health)
		if self.health < 1:
			self.kill()

	def update_health_bar(self):
		start_rad_green = 3 * (math.pi / 4) - _angle_to_radians(self.angle)
		stop_rad_green = 5 * (math.pi / 4) - ((self.max_health - self.health) * math.pi / 100) - _angle_to_radians(
			self.angle)
		pygame.draw.arc(self.screen, Color('green'), (self.pos.x - self.rect.width / 2,
													  self.pos.y - self.rect.height / 2, self.rect.width,
													  self.rect.height),
						start_rad_green, stop_rad_green, 4)
		stop_rad_red = 5 * (math.pi / 4) - _angle_to_radians(self.angle)
		pygame.draw.arc(self.screen, Color('red'), (self.pos.x - self.rect.width / 2,
													self.pos.y - self.rect.height / 2, self.rect.width,
													self.rect.height),
						stop_rad_green, stop_rad_red, 4)

	def update_spear(self):
		spear_rect = self.rect.copy()
		spear_rect.width = spear_rect.height = 50
		spear_rect.centerx = self.rect.centerx + 30 * math.cos(_angle_to_radians(self.angle + 90))
		spear_rect.centery = self.rect.centery + 30 * math.sin(_angle_to_radians(self.angle + 90))
		self.screen.blit(self.spear_images[self.angle], spear_rect)

	def update_sight(self):
		self.sight.update_coordinates(self.rect.centerx, self.rect.centery, self.angle)
		self.sight.update()

	def update_sight_vectors(self):
		start_angle = (self.angle - 36) % 360
		for v in range(0, 9):
			x = int(self.rect.centerx + 300 * math.cos(_angle_to_radians(start_angle)))
			y = int(self.rect.centery + 300 * math.sin(_angle_to_radians(start_angle)))
			pygame.draw.line(self.screen, (255, 255, 255), self.rect.center, (x, y))
			start_angle = (start_angle + 9) % 360

	def get_pixel(self):
		print(self.screen.get_at((100, 100)))

	def _load_images(self, folder):
		imgs_list = glob(folder + "*")
		images = {}
		for image in imgs_list:
			filename = os.path.basename(image)
			id = int(filename[:-4])
			images[id] = pygame.image.load(image)
		return images

	def check_distance(self, team):
		for sprite in team:
			distance = _get_distance(self.rect.center, sprite.rect.center)
			if distance < 300:
				radians = math.atan2(self.rect.centerx - sprite.rect.centerx, self.rect.centery - sprite.rect.centery)
				angle = _radians_to_angle(radians) % 360
				print(angle)
				#print (self.angle)




def _angle_to_direction(angle):
	radians = angle * math.pi / 180
	vx = math.cos(radians)
	vy = math.sin(radians)
	return vec2d((vx, vy)).normalized()


def _angle_to_radians(angle):
	return angle * math.pi / 180


def _radians_to_angle(rad):
	return rad * 180 / math.pi


def _get_distance(p1, p2):
	return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
