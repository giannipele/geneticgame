import ggutilities
from mvc.model.weapons import Weapon
from vec2d import vec2d

# Stepsize in degrees of the angle to turn the ominus
STEP_ANGLE = 9


class Ominus:
    """
         An ominus is a player of the game. This class contains
        all the settings and actions of the Ominus.
    """

    def __init__(self, id, x, y, angle, screen=None):
        self.id = id
        self.pos = vec2d(x, y)
        self.angle = angle
        self.direction = ggutilities.angle_to_direction(angle)
        self.speed = 5
        self.health = 50
        self.max_health = 50
        self.screen = screen
        self.weapon = Weapon()

    # Print the internal status of the ominus
    def print(self):
        print("Ominus {} status:".format(self.id))
        print("position: ({}, {})".format(self.pos.x, self.pos.y))
        print("angle: {}".format(self.angle))
        print("------------------------\n")

    # Forward and backward compute the next position according to the
    # direction and the speed
    def forward(self):
        displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
        self.pos += displacement
        self.check_border_collision()

    def backward(self):
        displacement = vec2d(-self.direction.x * self.speed, -self.direction.y * self.speed)
        self.pos += displacement
        self.check_border_collision()

    # Right and left change the angle and the direction of the ominus
    def right(self):
        self.angle = (self.angle + STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)

    def left(self):
        self.angle = (self.angle - STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)

    def decrease_health(self, damage):
        self.health -= damage

    def check_border_collision(self):
        screen_bounds = (32, self.screen[0] - 32, 32, self.screen[1] - 32)
        if self.pos.x < screen_bounds[0]:
            self.pos.x = screen_bounds[0]
        elif self.pos.x > screen_bounds[1]:
            self.pos.x = screen_bounds[1]
        if self.pos.y < screen_bounds[2]:
            self.pos.y = screen_bounds[2]
        elif self.pos.y > screen_bounds[3]:
            self.pos.y = screen_bounds[3]

    def attack(self):
        return self.weapon.shoot(self.id, self.angle, self.pos)


if __name__ == "__main__":
    ominus = Ominus(0, 97, 82, 77)
    ominus.print()
    ominus.forward()
    ominus.print()
    ominus.backward()
    ominus.print()
    ominus.right()
    ominus.print()
    ominus.left()
    ominus.print()
