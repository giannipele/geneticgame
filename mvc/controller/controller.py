import pygame

FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3

PLAYER_1 = 1
PLAYER_2 = 2


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        """
        Maintain the clock of the game and act as listener of the events
        of the inputs. Clock is spreaded to the model and the view.
        :return:
        """
        clock = pygame.time.Clock()
        register_clock = pygame.time.get_ticks()
        quit = False

        while not quit:
            # Framerate of the game
            clock.tick(50)
            if pygame.time.get_ticks() - register_clock > 1000:
                register_clock = pygame.time.get_ticks()
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
            if key[pygame.K_ESCAPE]:
                quit = True

            if key[pygame.K_UP]:
                self.model.move_player(PLAYER_1, FORWARD)
            elif key[pygame.K_DOWN]:
                self.model.move_player(PLAYER_1, BACKWARD)
            if key[pygame.K_RIGHT]:
                self.model.move_player(PLAYER_1, RIGHT)
            elif key[pygame.K_LEFT]:
                self.model.move_player(PLAYER_1, LEFT)
            if key[pygame.K_k]:
                self.model.attack(PLAYER_1)

            if key[pygame.K_w]:
                self.model.move_player(PLAYER_2, FORWARD)
            elif key[pygame.K_s]:
                self.model.move_player(PLAYER_2, BACKWARD)
            if key[pygame.K_d]:
                self.model.move_player(PLAYER_2, RIGHT)
            elif key[pygame.K_a]:
                self.model.move_player(PLAYER_2, LEFT)
            if key[pygame.K_c]:
                self.model.attack(PLAYER_2)

            #if key[pygame.K_SPACE]:
                #self.model.decrease_health()

            self.view.tick()
            self.model.tick()
