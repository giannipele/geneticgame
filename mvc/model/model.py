import random as rand

from mvc.model.ominus import Ominus

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
            for c in collisions:
                print ("Bullet collided with sprite {}".format(c.id))

        deads = []
        for p in self.players.values():
            if p.health <= 0:
                deads.append(p.id)
        for id in deads:
            self.remove_player(id)

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


class Config:
    def __init__(self):
        with open("settings", 'r') as fsett:
            for l in fsett:
                l = l.strip()
                if l.startswith('#'):
                    continue
                else:
                    infos = l.split("=")
                    if infos[0] == 'STEP_ANGLE':
                        self.step_angle = int(infos[1])
                    elif infos[0] == 'WEAPON_POWER':
                        self.weapon_power = int(infos[1])
                    elif infos[0] == 'WEAPON_DAMAGE':
                        self.weapon_damage = int(infos[1])
                    elif infos[0] == 'WEAPON_RATIO':
                        self.weapon_ratio = float(infos[1])
                    elif infos[0] == 'WEAPON_PRECISION':
                        self.weapon_precision = int(infos[1])

    def print(self):
        print ("##### Configuration of the game ##### \n"
               "Step Angle : " + str(self.step_angle) + "\n"
               "Weapon Power : " + str(self.weapon_power) + "\n"
               "Weapon Damage : " + str(self.weapon_damage) + "\n"
               "Weapon Ratio : " + str(self.weapon_ratio) + "\n"
               "Weapon Precision : " + str(self.weapon_precision) + "\n")


if __name__ == "__main__":
    model = Model()
    model.add_player()
    model.add_player()
    model.add_player()
    model.remove_player(1)
