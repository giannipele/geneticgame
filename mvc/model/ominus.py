import ggutilities
from mvc.model.weapons import Weapon
from vec2d import vec2d

# Stepsize in degrees of the angle to turn the ominus
STEP_ANGLE = 5


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
        self.radius = 32
        self.speed = 5
        self.health = 50
        self.max_health = 50
        self.screen = screen
        self.weapon = Weapon()
        self.sight = Sight(self)

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
        self.sight.update()

    def backward(self):
        displacement = vec2d(-self.direction.x * self.speed, -self.direction.y * self.speed)
        self.pos += displacement
        self.check_border_collision()
        self.sight.update()

    # Right and left change the angle and the direction of the ominus
    def right(self):
        self.angle = (self.angle + STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)
        self.sight.update()

    def left(self):
        self.angle = (self.angle - STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)
        self.sight.update()

    def decrease_health(self, damage):
        self.health -= damage

    def check_border_collision(self):
        screen_bounds = (32, self.screen[0] - self.radius, self.radius, self.screen[1] - self.radius)
        if self.pos.x < screen_bounds[0]:
            self.pos.x = screen_bounds[0]
        elif self.pos.x > screen_bounds[1]:
            self.pos.x = screen_bounds[1]
        if self.pos.y < screen_bounds[2]:
            self.pos.y = screen_bounds[2]
        elif self.pos.y > screen_bounds[3]:
            self.pos.y = screen_bounds[3]

    def check_collision(self, ominus_list):
        collisions = []
        for o in ominus_list:
            if o.id == self.id:
                pass
            distance = ggutilities.get_distance(self.pos, o.pos)
            if distance <= 64:
                direction = vec2d(self.pos - o.pos)
                self.pos.x = self.pos.x + direction[0]
                self.pos.y = self.pos.y - direction[1]

    def attack(self):
        return self.weapon.shoot(self.id, self.angle, self.pos)


class Sight:
    def __init__(self, ominus, front_beams=(14, 140, 350), back_beams=(4, 90, 100)):
        self.ominus = ominus
        self.front_beams = front_beams
        self.back_beams = back_beams
        self.update()

    def update(self):
        self.beams = []
        start_angle = (self.ominus.angle - self.front_beams[1] / 2) % 360
        step_angle = self.front_beams[1] / self.front_beams[0]
        self.beams = [(b % 360, self.front_beams[2]) for b in range(int(start_angle), int(start_angle + self.front_beams[1]), int(step_angle))]

        start_angle = (self.ominus.angle + 180 - self.back_beams[1] / 2) % 360
        step_angle = self.back_beams[1] / self.back_beams[0]
        self.beams.extend([(b % 360, self.back_beams[2]) for b in range(int(start_angle), int(start_angle + self.back_beams[1]), int(step_angle))])
        '''for i in range(self.front_beams[0]):
            self.beams.append(ggutilities.angle_to_direction(start_angle + i * step_angle))

        start_angle = ((self.ominus.angle + 180) - self.back_beams[1] / 2) % 360
        step_angle = self.back_beams[1] / self.back_beams[0]
        for i in range(self.back_beams[0]):
            self.beams.append(ggutilities.angle_to_direction(start_angle + i * step_angle))'''


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
