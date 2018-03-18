import ggutilities
from vec2d import vec2d


class Wall:
    def __init__(self, id, x, y, width, height, angle):
        """
        Wall object of the game. A wall cannot be crossed by ominus and bullets,
        and they are squared blocks.
        :param id:
        :param x:
        :param y:
        :param width:
        :param height:
        :param angle:
        """
        self.id = id
        self.pos = vec2d(x, y)
        self.width = width
        self.height = height
        self.angle = angle

    def check_collision(self, ominus_players):
        """
        Check the collisions of the ominus with the wall, if it does move the ominus
        :param ominus_players: list of the ominus in the game
        :return: list of ominus hitting the wall
        """
        collisions = []
        for o in ominus_players:
            # res = [TOP, LEFT, BOTTOM, RIGHT]
            res = [ggutilities.line_intersect_circle(o.pos, o.radius, (self.pos, (self.pos.x + self.width, self.pos.y))),
                   ggutilities.line_intersect_circle(o.pos, o.radius, (self.pos, (self.pos.x, self.pos.y + self.height))),
                   ggutilities.line_intersect_circle(o.pos, o.radius, ((self.pos.x, self.pos.y + self.height), (self.pos.x + self.width, self.pos.y + self.height))),
                   ggutilities.line_intersect_circle(o.pos, o.radius, ((self.pos.x + self.width, self.pos.y), (self.pos.x + self.width, self.pos.y + self.height)))]
            i = 0
            for r in res:
                if r[0]:
                    collisions.append(o)
                    if i == 0:
                        o.pos.y = r[1][1] - 32
                        break
                    elif i == 1:
                        o.pos.x = r[1][0] - 32
                        break
                    elif i == 2:
                        o.pos.y = self.pos.y + self.height + 32
                        break
                    elif i == 3:
                        o.pos.x = self.pos.x + self.width + 32
                        break
                i += 1
        return collisions



