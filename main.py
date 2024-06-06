import sys
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

import pygame
from pygame.locals import *

pygame.init()

from constants import *
from classes import *
from assets import AssetManager

from ui import menus, util

import worlds


def get_new_screen():
    return pygame.display.set_mode((1920, 1080))


class Crtd:

    def __init__(self):
        self.running = True
        self.screen = get_new_screen()
        self.clock = pygame.time.Clock()
        self.frame_time = 0

        self.state_stack = [menus.HomeMenu(self)]

        self.assets = AssetManager()

        self.game_map = None

    def loop(self):

        events = pygame.event.get()

        # Game will respond to quit events in any situation
        # TODO: Better way to detect quitting from anywhere without iterating through whole events twice every frame?
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # LOGIC #####################################

        if self.state_stack:
            self.state_stack[-1].update(self.frame_time, events)

        # State stack should never be empty
        else:
            pass

        # RENDER ####################################

        if self.state_stack:
            self.state_stack[-1].render(self.frame_time, self.screen)

        # State stack should never be empty
        else:
            pass

        util.write(self.screen, util.TextSize.TINY, Colours.WHITE, (10, 1060), str(round(self.clock.get_fps(), 1)))

        pygame.display.flip()

        # Tick and get frame time
        self.frame_time = self.clock.tick(FPS)


if __name__ == "__main__":
    game = Crtd()
    while game.running:
        game.loop()
