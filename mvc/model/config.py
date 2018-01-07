

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
