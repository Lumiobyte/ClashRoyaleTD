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

        self.ui_state_stack = [menus.HomeMenu(self)]

        self.assets = AssetManager()

        self.game_map = None

    def temp_screen(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.game_map:
                    self.game_map.pan_viewport(Point(*pygame.mouse.get_pos()))
                else:
                    self.game_map = worlds.load_map(worlds.get_offline_map_list()[0])

                print(pygame.mouse.get_pos())
                print(pygame.mouse.get_rel())

        # Update

        # Draw
        self.screen.fill(Colours.BLACK)

        # game_map.render(screen)

        pygame.draw.rect(self.screen, Colours.PANEL_DARKGREY, pygame.Rect(1550, 0, 370, 1080))

        if self.game_map:
            util.write(self.screen, util.TextSize.LARGE_BOLD, Colours.WHITE, (1580, 100), "Defenses", False)

            pygame.draw.rect(self.screen, Colours.LIGHT_GREEN, pygame.Rect(1580, 220, 80, 80))
            pygame.draw.rect(self.screen, Colours.LIGHT_GREEN, pygame.Rect(1580, 400, 80, 80))
            pygame.draw.rect(self.screen, Colours.LIGHT_GREEN, pygame.Rect(1700, 220, 80, 80))
            pygame.draw.rect(self.screen, Colours.LIGHT_GREEN, pygame.Rect(1700, 400, 80, 80))

            util.write(self.screen, util.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to pan map", False)
        else:
            util.write(self.screen, util.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to load map 'basic'",
                       False)

        pygame.display.flip()

    def loop(self):

        events = pygame.event.get()

        # Game will respond to quit events in any situation
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # LOGIC #####################################

        # Menus
        if self.ui_state_stack:
            self.ui_state_stack[-1].update(self.frame_time, events)

        # In Game
        else:
            self.temp_screen(events)

        # RENDER ####################################

        # Menus
        if self.ui_state_stack:
            self.ui_state_stack[-1].render(self.screen)

        # In Game
        else:
            pass  # No proper game function yet

        pygame.display.flip()

        # Tick and get frame time
        self.frame_time = self.clock.tick(FPS)


if __name__ == "__main__":
    game = Crtd()
    while game.running:
        game.loop()
