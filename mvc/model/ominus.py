import ggutilities
from mvc.model.weapons import Weapon
from vec2d import vec2d

# Stepsize in degrees of the angle to turn the ominus
STEP_ANGLE = 4


class Ominus:
    """
         An ominus is a player of the game. This class contains
        all the settings and actions of the Ominus.
    """

    def __init__(self, id, x, y, angle, screen=None):
        """
        Create an ominus object.
        :param id:  id of the Ominus
        :param x: x position
        :param y: y position
        :param angle: direction angle
        :param screen: pair of screen_w, screen_h
        """
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
        """
        Print the status of the ominus.
        :return:
        """
        print("Ominus {} status:".format(self.id))
        print("position: ({}, {})".format(self.pos.x, self.pos.y))
        print("angle: {}".format(self.angle))
        print("------------------------\n")

    # Forward and backward compute the next position according to the
    # direction and the speed
    def forward(self):
        """
        Move the ominus forward according to its direction.
        :return:
        """
        displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
        self.pos += displacement
        self.check_border_collision()
        self.sight.update()

    def backward(self):
        """
        Move the ominus in the opposite direction it is pointing at
        :return:
        """
        displacement = vec2d(-self.direction.x * self.speed, -self.direction.y * self.speed)
        self.pos += displacement
        self.check_border_collision()
        self.sight.update()

    # Right and left change the angle and the direction of the ominus
    def right(self):
        """
        Rotate the ominus right.
        :return:
        """
        self.angle = (self.angle + STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)
        self.sight.update()

    def left(self):
        """
        Rotate the ominus left.
        :return:
        """
        self.angle = (self.angle - STEP_ANGLE) % 360
        self.direction = ggutilities.angle_to_direction(self.angle)
        self.sight.update()

    def decrease_health(self, damage):
        """
        Decrease the health of the ominus.
        :param damage: Damage to subtract to the health
        :return:
        """
        self.health -= damage

    def check_border_collision(self):
        """
        Prevent the ominus to exit the borders of the game.
        :return:
        """
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
        """
        Check the collision with all the other ominus.
        :param ominus_list: List of the ominus in the game
        :return: List of ominus id that are colliding
        """
        collisions = []
        for o in ominus_list:
            if o.id == self.id:
                pass
            distance = ggutilities.get_distance(self.pos, o.pos)
            if distance <= 64:
                direction = vec2d(self.pos - o.pos)
                self.pos.x = self.pos.x + direction[0]
                self.pos.y = self.pos.y - direction[1]
                collisions.append(o)
        return collisions

    def check_sight_collision(self):
        collisions = []

    def attack(self):
        """
        Perform an attack with the weapon.
        :return:
        """
        return self.weapon.shoot(self.id, self.angle, self.pos)


class Sight:
    """
    Define the sight of the ominus. The sight is implemented as a set of
    vectors that starts at the ominus center and spread around withing a certain angle and
    collide with objects.
    """
    def __init__(self, ominus, front_beams=(25, 140, 600), back_beams=(4, 90, 130)):
        self.ominus = ominus
        self.front_beams = front_beams
        self.back_beams = back_beams
        self.update()

    def update(self):
        # beams list contains all the beams of the ominus.
        self.beams = []

        # construct the front beams
        start_angle = (self.ominus.angle - self.front_beams[1] / 2) % 360
        step_angle = self.front_beams[1] / self.front_beams[0]
        self.beams = [(b % 360, self.front_beams[2]) for b in range(int(start_angle), int(start_angle + self.front_beams[1]), int(step_angle))]

        # construct the back beams
        start_angle = (self.ominus.angle + 180 - self.back_beams[1] / 2) % 360
        step_angle = self.back_beams[1] / self.back_beams[0]
        self.beams.extend([(b % 360, self.back_beams[2]) for b in range(int(start_angle), int(start_angle + self.back_beams[1]), int(step_angle))])


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
