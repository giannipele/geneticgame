import random as rand
from mvc.model.config import Config
from mvc.model.ominus import Ominus
from mvc.model.wall import Wall

# Screen width and height in pixels
SCREEN_W = 1024
SCREEN_H = 700

FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3

STEP_ANGLE = 9


class Model:
    """
        Model of the game. It contains the engine for
        managing the information of the game.
    """

    # Incremental Player ID
    IPID = 0

    def __init__(self):
        self.game_field = (SCREEN_W, SCREEN_H)
        self.bg_color = [255, 255, 255, 0]
        self.players = {}
        self.bullets = []
        self.wall_blocks = []
        self.config = Config()

    @staticmethod
    def get_screen_size():
        return SCREEN_W, SCREEN_H

    def tick(self):
        bullets = []
        for b in self.bullets:
            if not b.gone:
                bullets.append(b)
        self.bullets = bullets
        for b in self.bullets:
            b.move()
            collisions = b.check_collision(self.get_players())

        '''for o in self.players.values():
            o.check_collision(self.get_players())'''

        for w in self.wall_blocks:
            collisions = w.check_collision(self.get_players())
            #print("Wall {} collided with object {}".format(w.id, [o.id for o in collisions]))
            '''for c in collisions:
                print ("Bullet collided with sprite {}".format(c.id))'''

        deads = []
        for p in self.players.values():
            if p.health <= 0:
                deads.append(p.id)
        for id in deads:
            self.remove_player(id)

    def create_terrain(self):
        self.wall_blocks = []
        left_wall = Wall(1, 0, 0, 25, SCREEN_H, 0)
        right_wall = Wall(3, SCREEN_W - 25, 0, 25, SCREEN_H, 0)
        top_wall = Wall(0, 25, 0, SCREEN_W - 50, 25, 0)
        bottom_wall = Wall(2, 25, SCREEN_H - 25, SCREEN_W - 50, 25, 0)
        self.wall_blocks.append(left_wall)
        self.wall_blocks.append(right_wall)
        self.wall_blocks.append(top_wall)
        self.wall_blocks.append(bottom_wall)

    def attack(self, pid):
        for p in self.players.values():
            if p.id == pid - 1:
                bullet = p.attack()
                if bullet is not None:
                    self.bullets.append(bullet)

    def add_player(self):
        x = rand.randint(30, SCREEN_W - 30)
        y = rand.randint(30, SCREEN_H - 30)
        angle = rand.randrange(0, 360, STEP_ANGLE)
        player = Ominus(self.IPID, x, y, angle, screen=(SCREEN_W, SCREEN_H))
        self.IPID += 1
        self.players[player.id] = player
        print("Player with ID {} added.".format(player.id))

    def remove_player(self, id):
        del self.players[id]
        print("Removed player with ID {}.".format(id))

    def get_players(self):
        return [p for p in self.players.values()]

    def move_player(self, pid, direction):
        # Players IDS of the controller : [1,2,3,4]
        for p in self.players.values():
            if p.id == pid - 1:
                if direction == FORWARD:
                    p.forward()
                elif direction == BACKWARD:
                    p.backward()
                elif direction == LEFT:
                    p.left()
                elif direction == RIGHT:
                    p.right()
                break

    def get_walls(self):
        return [w for w in self.wall_blocks]

if __name__ == "__main__":
    model = Model()
    model.add_player()
    model.add_player()
    model.add_player()
    model.remove_player(1)
