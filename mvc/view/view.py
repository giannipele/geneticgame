import math
import os
import ggutilities
from glob import glob
import pygame
from pygame import Color

VIEW_ROOT_DIR = "mvc/view/"
BG_COLOR = (30, 145, 50)
WALL_COLOR = (128, 128, 128)
PLAYERS_COLORS = ['Red', 'Blue']


class View:
    def __init__(self, model):
        self.model = model
        self.SCREEN_W, self.SCREEN_H = model.get_screen_size()
        self.quit = False
        self.agent_group = pygame.sprite.Group()
        self.terrain_group = pygame.sprite.Group()

    def run(self):
        """
        Initialize the view with all the components, according to the model.
        :return:
        """
        pygame.init()
        pygame.display.set_caption("Genetic Game")
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), 0, 32)

        self.ominus_sprites = [OminusSprite(self.screen, o, PLAYERS_COLORS[o.id]) for o in self.model.get_players()]
        for o in self.ominus_sprites:
            self.agent_group.add(o)

        self.wall_sprites = [WallSprite(self.screen, w) for w in self.model.get_walls()]
        for w in self.wall_sprites:
            self.terrain_group.add(w)

    def tick(self):
        """
        Called by the controller to refresh the content of the view.
        :return:
        """
        deads = []
        self.screen.fill(BG_COLOR)
        for b in self.model.bullets:
            self.agent_group.add(BulletSprite(self.screen, b))
        for sprite in self.agent_group:
            if sprite.check_death():
                deads.append(sprite)
            else:
                sprite.update()
                sprite.blit()

        for w in self.terrain_group:
            w.blit()

        for sprite in deads:
            self.agent_group.remove(sprite)

        pygame.display.flip()

    def quit(self):
        """
        Close the window and exit.
        :return:
        """
        self.quit = True


class OminusSprite(pygame.sprite.Sprite):
    def __init__(self, screen, ominus, color):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.ominus = ominus
        self.angle = ominus.angle
        self.pos = ominus.pos
        self.images = _load_images(VIEW_ROOT_DIR + "Elements/{}PlayerComplete/".format(color))
        self.image = self.images[ominus.angle]
        self.rect = self.image.get_rect()
        self.weapon_sprite = WeaponSprite(screen, ominus.weapon, ominus.pos, ominus.angle)
        self.sight = True

    def update(self):
        self.rect = self.image.get_rect().move(self.ominus.pos.x - self.rect.width / 2,
                                               self.ominus.pos.y - self.rect.height / 2)
        self.angle = self.ominus.angle
        self.image = self.images[self.angle]
        self.weapon_sprite.update(self.rect, self.angle)

    def blit(self):
        self.weapon_sprite.blit()
        self.blit_health_bar()
        if self.sight:
            self.blit_sight()
        self.screen.blit(self.image, self.rect)

    def blit_health_bar(self):
        start_rad_green = 3 * (math.pi / 4) - ggutilities.angle_to_radians(self.angle)
        stop_rad_green = 5 * (math.pi / 4) - (
                (self.ominus.max_health - self.ominus.health) * math.pi / 100) - ggutilities.angle_to_radians(
            self.angle)
        pygame.draw.arc(self.screen, Color('green'), (self.pos.x - self.rect.width / 2,
                                                      self.pos.y - self.rect.height / 2, self.rect.width,
                                                      self.rect.height),
                        start_rad_green, stop_rad_green, 4)
        stop_rad_red = 5 * (math.pi / 4) - ggutilities.angle_to_radians(self.angle)
        pygame.draw.arc(self.screen, Color('red'), (self.pos.x - self.rect.width / 2,
                                                    self.pos.y - self.rect.height / 2, self.rect.width,
                                                    self.rect.height),
                        stop_rad_green, stop_rad_red, 4)

    def blit_sight(self):
        for b in self.ominus.sight.beams:
            x = int(self.rect.centerx + b[1] * math.cos(ggutilities.angle_to_radians(b[0])))
            y = int(self.rect.centery + b[1] * math.sin(ggutilities.angle_to_radians(b[0])))
            pygame.draw.line(self.screen, [255, 128, 12], self.rect.center, (x,y))

    def check_death(self):
        if self.ominus.health <= 0:
            return True
        else:
            return False


class WeaponSprite(pygame.sprite.Sprite):
    def __init__(self, screen, weapon, pos, angle):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.weapon = weapon
        self.angle = angle
        self.pos = pos
        self.images = _load_images(VIEW_ROOT_DIR + "Elements/SpearComplete/")
        self.image = self.images[angle]
        self.rect = self.image.get_rect()

    def update(self, rect, angle):
        spear_rect = rect.copy()
        spear_rect.width = spear_rect.height = 50
        spear_rect.centerx = rect.centerx + 30 * math.cos(ggutilities.angle_to_radians(angle + 90))
        spear_rect.centery = rect.centery + 30 * math.sin(ggutilities.angle_to_radians(angle + 90))
        self.rect = spear_rect
        self.image = self.images[angle]

    def blit(self):
        self.screen.blit(self.image, self.rect)


class BulletSprite(pygame.sprite.Sprite):
    def __init__(self, screen, bullet):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.bullet = bullet
        self.image = pygame.image.load(VIEW_ROOT_DIR + "Elements/Bullets/squarebullet.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.image.get_rect().move(self.bullet.pos.x - self.rect.width / 2,
                                               self.bullet.pos.y - self.rect.height / 2)

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def check_death(self):
        if self.bullet.gone:
            return True
        else:
            return False


class WallSprite(pygame.sprite.Sprite):
    def __init__(self, screen, wall):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.wall = wall
        self.rect = pygame.Rect(wall.pos[0], wall.pos[1], wall.width, wall.height)

    def blit(self):
        pygame.draw.rect(self.screen, WALL_COLOR, self.rect)


def _load_images(folder):
    imgs_list = glob(folder + "*")
    images = {}
    for image in imgs_list:
        filename = os.path.basename(image)
        id = int(filename[:-4])
        images[id] = pygame.image.load(image)
    return images
