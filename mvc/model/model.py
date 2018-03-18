import random as rand
from mvc.model.config import Config
from mvc.model.ominus import Ominus
from mvc.model.wall import Wall

# Screen width and height in pixels
SCREEN_W = 1600
SCREEN_H = 900

FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3

STEP_ANGLE = 4


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
        """

        :return: Screen width, screen size
        """
        return SCREEN_W, SCREEN_H

    def tick(self):
        """
        Set the clocks of the game. All the MVC components update at this clock.
        :return:
        """
        bullets = []
        for b in self.bullets:
            if not b.gone:
                bullets.append(b)
        self.bullets = bullets
        for b in self.bullets:
            b.move()
            b.check_ominus_collision(self.get_players())
            b.check_wall_collision(self.get_walls())

        for w in self.wall_blocks:
            w.check_collision(self.get_players())

#        for p in self.get_players():
 #           p.check_sight_collision(self.get_players(), self.get_walls())

        deads = []
        for p in self.players.values():
            if p.health <= 0:
                deads.append(p.id)
        for id in deads:
            self.remove_player(id)

    def create_terrain(self):
        """
        Generate a random terrain with walls generated with certain probability.
        :return:
        """
        self.wall_blocks = []
        left_wall = Wall(1, 0, 0, 25, SCREEN_H, 0)
        right_wall = Wall(3, SCREEN_W - 25, 0, 25, SCREEN_H, 0)
        top_wall = Wall(0, 25, 0, SCREEN_W - 50, 25, 0)
        bottom_wall = Wall(2, 25, SCREEN_H - 25, SCREEN_W - 50, 25, 0)
        self.wall_blocks.append(left_wall)
        self.wall_blocks.append(right_wall)
        self.wall_blocks.append(top_wall)
        self.wall_blocks.append(bottom_wall)

        id = 4
        for i in range(4):
            x = 150 + (SCREEN_W - 50)/4 * i
            for j in range(6):
                y = 25 + (SCREEN_H - 50)/6 * j
                probability = rand.uniform(0, 100)
                if probability <= 50:
                    self.wall_blocks.append(Wall(id, x, y, rand.randint(40, 150), rand.randint(40,180), 0))
                    id += 1

    def attack(self, pid):
        """
        Call the attack() function of the player that is attacking.
        :param pid: Id of the player passed from the controller.
        :return:
        """
        for p in self.players.values():
            if p.id == pid - 1:
                bullet = p.attack()
                if bullet is not None:
                    self.bullets.append(bullet)

    def add_player(self):
        """
        Add another player to the game.
        :return:
        """
        x = rand.randint(30, SCREEN_W - 30)
        y = rand.randint(30, SCREEN_H - 30)
        angle = rand.randrange(0, 360, STEP_ANGLE)
        player = Ominus(self.IPID, x, y, angle, screen=(SCREEN_W, SCREEN_H))
        self.IPID += 1
        self.players[player.id] = player
        print("Player with ID {} added.".format(player.id))

    def remove_player(self, id):
        """
        Remove a player from the game.
        :param id: Id of the player to remove.
        :return:
        """
        del self.players[id]
        print("Removed player with ID {}.".format(id))

    def get_players(self):
        """

        :return: List of players.
        """
        return [p for p in self.players.values()]

    def move_player(self, pid, direction):
        """
        Move a player in a certain direction.
        :param pid: Id of the player
        :param direction: vector of the direction to move
        :return:
        """
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
        """

        :return: List of the walls inside the game
        """
        return [w for w in self.wall_blocks]


if __name__ == "__main__":
    model = Model()
    model.add_player()
    model.add_player()
    model.add_player()
    model.remove_player(1)
