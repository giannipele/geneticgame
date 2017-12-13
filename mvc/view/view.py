import math
import os
import ggutilities
from glob import glob
import pygame
from pygame import Color

BG_COLOR = 30, 145, 50
PLAYERS_COLORS = ['Red', 'Blue']


class View:
    def __init__(self, model):
        self.model = model
        self.SCREEN_W, self.SCREEN_H = model.get_screen_size()
        self.quit = False
        self.sprite_group = pygame.sprite.Group()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_W, self.SCREEN_H), 0, 32)
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.ominus_sprites = [OminusSprite(self.screen, o, PLAYERS_COLORS[o.id]) for o in self.model.get_players()]
=======
        self.ominus_sprites = [OminusSprite(self.screen, o) for o in self.model.get_players()]
>>>>>>> changes before start adding the collisions part
        for o in self.ominus_sprites:
            self.sprite_group.add(o)

    def tick(self):
        deads = []
        self.screen.fill(BG_COLOR)
        for b in self.model.bullets:
            self.sprite_group.add(BulletSprite(self.screen, b))
        for sprite in self.sprite_group:
            if sprite.check_death():
                deads.append(sprite)
            else:
                sprite.update()
                sprite.blit()

        for sprite in deads:
            self.sprite_group.remove(sprite)
        pygame.display.flip()

    def quit(self):
        self.quit = True


class OminusSprite(pygame.sprite.Sprite):
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
    def __init__(self, screen, ominus, color):
=======
    def __init__(self, screen, ominus):
>>>>>>> changes before start adding the collisions part
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.ominus = ominus
        self.angle = ominus.angle
        self.pos = ominus.pos
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.images = _load_images("mvc/view/Elements/{}Player/".format(color))
        self.image = self.images[ominus.angle]
=======
        self.image = pygame.image.load("mvc/view/Elements/RedPlayer/" + str(self.angle) + ".png")
>>>>>>> changes before start adding the collisions part
        self.rect = self.image.get_rect()
        self.weapon_sprite = WeaponSprite(screen, ominus.weapon, ominus.pos, ominus.angle)

    def update(self):
        self.rect = self.image.get_rect().move(self.ominus.pos.x - self.rect.width / 2,
                                               self.ominus.pos.y - self.rect.height / 2)
        self.angle = self.ominus.angle
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.image = self.images[self.angle]
        self.weapon_sprite.update(self.rect, self.angle)

    def blit(self):
        self.weapon_sprite.blit()
        self.blit_health_bar()
        self.screen.blit(self.image, self.rect)

    def blit_health_bar(self):
        start_rad_green = 3 * (math.pi / 4) - ggutilities.angle_to_radians(self.angle)
        stop_rad_green = 5 * (math.pi / 4) - (
                (self.ominus.max_health - self.ominus.health) * math.pi / 100) - ggutilities.angle_to_radians(
=======
        self.image = pygame.image.load("mvc/view/Elements/RedPlayer/" + str(self.angle) + ".png")
        self.weapon_sprite.update(self.rect, self.angle)

    def blit_health_bar(self):
        start_rad_green = 3 * (math.pi / 4) - _angle_to_radians(self.angle)
        stop_rad_green = 5 * (math.pi / 4) - (
        (self.ominus.max_health - self.ominus.health) * math.pi / 100) - _angle_to_radians(
>>>>>>> changes before start adding the collisions part
            self.angle)
        pygame.draw.arc(self.screen, Color('green'), (self.pos.x - self.rect.width / 2,
                                                      self.pos.y - self.rect.height / 2, self.rect.width,
                                                      self.rect.height),
                        start_rad_green, stop_rad_green, 4)
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        stop_rad_red = 5 * (math.pi / 4) - ggutilities.angle_to_radians(self.angle)
=======
        stop_rad_red = 5 * (math.pi / 4) - _angle_to_radians(self.angle)
>>>>>>> changes before start adding the collisions part
        pygame.draw.arc(self.screen, Color('red'), (self.pos.x - self.rect.width / 2,
                                                    self.pos.y - self.rect.height / 2, self.rect.width,
                                                    self.rect.height),
                        stop_rad_green, stop_rad_red, 4)

<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
=======
    def blit(self):
        self.weapon_sprite.blit()
        self.blit_health_bar()
        self.screen.blit(self.image, self.rect)

>>>>>>> changes before start adding the collisions part
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
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.images = _load_images("mvc/view/Elements/Spear/")
        self.image = self.images[angle]
=======
        self.image = pygame.image.load("mvc/view/Elements/Spear/" + str(self.angle) + ".png")
>>>>>>> changes before start adding the collisions part
        self.rect = self.image.get_rect()

    def update(self, rect, angle):
        spear_rect = rect.copy()
        spear_rect.width = spear_rect.height = 50
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        spear_rect.centerx = rect.centerx + 30 * math.cos(ggutilities.angle_to_radians(angle + 90))
        spear_rect.centery = rect.centery + 30 * math.sin(ggutilities.angle_to_radians(angle + 90))
        self.rect = spear_rect
        self.image = self.images[angle]
=======
        spear_rect.centerx = rect.centerx + 30 * math.cos(_angle_to_radians(angle + 90))
        spear_rect.centery = rect.centery + 30 * math.sin(_angle_to_radians(angle + 90))
        self.rect = spear_rect
        self.image = pygame.image.load("mvc/view/Elements/Spear/" + str(angle) + ".png")
>>>>>>> changes before start adding the collisions part

    def blit(self):
        self.screen.blit(self.image, self.rect)


class BulletSprite(pygame.sprite.Sprite):
    def __init__(self, screen, bullet):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.bullet = bullet
<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
        self.image = pygame.image.load("bullet.png")
=======
        self.image = pygame.image.load("pinkcreep_0.png")
>>>>>>> changes before start adding the collisions part
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


<<<<<<< d4107b6dd6f1de37ec47cb5450f5bfe21467d885
def _load_images(folder):
    imgs_list = glob(folder + "*")
    images = {}
    for image in imgs_list:
        filename = os.path.basename(image)
        id = int(filename[:-4])
        images[id] = pygame.image.load(image)
    return images
=======
# Convert angle into radians
def _angle_to_radians(angle):
    return angle * math.pi / 180
>>>>>>> changes before start adding the collisions part
