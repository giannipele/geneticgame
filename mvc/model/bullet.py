import ggutilities

from vec2d import vec2d

SPEED = 40


class Bullet:
    """
        Element that causes damage to another Ominus. Bullet is shot by a weapon.
    """

    def __init__(self, pid, x, y, direction, damage, power):
        self.pid = pid
        self.pos = vec2d(x, y)
        self.init_pos = vec2d(x, y)
        self.direction = direction
        self.damage = damage
        self.gone = False
        self.destroy_after = power

    def move(self):
        """
        Move forward the bullet.
        :return:
        """
        displacement = vec2d(self.direction.x * SPEED, self.direction.y * SPEED)
        self.pos += displacement
        distance = ggutilities.get_distance(self.init_pos, self.pos)
        if distance > self.destroy_after:
            self.gone = True

    def check_ominus_collision(self, ominus_list):
        """
        Check all the collisions with all the ominus, If it touches and ominus,
        the health of the ominus is decreased and the bullet is gone.
        :param ominus_list: List of the ominus of the game
        :return: List of the ominus the bullet hits
        """
        collisions = []
        for o in ominus_list:
            if o.id == self.pid:
                continue
            if not self.gone:
                distance = ggutilities.get_distance(self.pos, o.pos)
                if distance < 30:
                    o.decrease_health(self.damage)
                    collisions.append(o)
                    self.gone = True
        return collisions

    def check_wall_collision(self, wall_list):
        """
        Check the collision with the walls in the game. If it touches a wall,
        the bullet disappears.
        :param wall_list: List of the walls in the game, except the borders
        :return: List of all the walls the bullet hits
        """
        collisions = []
        for w in wall_list:
            if not self.gone:
                is_inside = ggutilities.point_inside_rect(self.pos, w.pos.x, w.pos.y, w.width, w.height)
                if is_inside:
                    collisions.append(w)
                    self.gone = True
        return collisions


