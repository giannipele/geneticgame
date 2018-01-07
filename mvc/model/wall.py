import ggutilities
from vec2d import vec2d


class Wall:
    def __init__(self, id, x, y, width, height, angle):
        self.id = id
        self.pos = vec2d(x, y)
        self.width = width
        self.height = height
        self.angle = angle

    def check_collision(self, ominus_players):
        collisions = []
        for o in ominus_players:
            # res = [TOP, LEFT, BOTTOM, RIGHT]
            res = [ggutilities.intersect(o.pos, o.radius, (self.pos, (self.pos.x + self.width, self.pos.y))),
                   ggutilities.intersect(o.pos, o.radius, (self.pos, (self.pos.x, self.pos.y + self.height))),
                   ggutilities.intersect(o.pos, o.radius, ((self.pos.x, self.pos.y + self.height), (self.pos.x + self.width, self.pos.y + self.height))),
                   ggutilities.intersect(o.pos, o.radius, ((self.pos.x + self.width, self.pos.y), (self.pos.x + self.width, self.pos.y + self.height)))]
            i = 0
            for r in res:
                if r[0]:
                    collisions.append(o)
                    if i == 0:
                        o.pos.y = r[1][1] - 32
                    elif i == 1:
                        o.pos.x = r[1][0] - 32
                    elif i == 2:
                        o.pos.y = self.pos.y + self.height + 32
                    elif i == 3:
                        o.pos.x = self.pos.x + self.width + 32
                i += 1
        return collisions


