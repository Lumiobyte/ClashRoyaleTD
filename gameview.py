import pygame
from pygame.locals import *

import state
import worlds
from ui import util
from constants import *
from classes import *


class TestGameView(state.State):
    def __init__(self, game, map_meta):
        state.State.__init__(self, game)

        self.game_map = worlds.load_map(map_meta)

    def update(self, delta_time, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.game_map:
                    self.game_map.pan_viewport(Point(*pygame.mouse.get_pos()))

                print(pygame.mouse.get_pos())
                print(pygame.mouse.get_rel())

            if event.type == KEYDOWN:
                if event.key == K_p:
                    self.exit_state()

    def render(self, delta_time, surface):

        # Update

        # Draw
        surface.fill(Colours.BLACK)

        self.game_map.render(surface)

        pygame.draw.rect(surface, Colours.PANEL_DARKGREY, pygame.Rect(1550, 0, 370, 1080))

        if self.game_map:
            util.write(surface, util.TextSize.LARGE_BOLD, Colours.WHITE, (1580, 100), "Defenses", False)

            pygame.draw.rect(surface, Colours.LIGHT_GREEN, pygame.Rect(1580, 220, 80, 80))
            pygame.draw.rect(surface, Colours.LIGHT_GREEN, pygame.Rect(1580, 400, 80, 80))
            pygame.draw.rect(surface, Colours.LIGHT_GREEN, pygame.Rect(1700, 220, 80, 80))
            pygame.draw.rect(surface, Colours.LIGHT_GREEN, pygame.Rect(1700, 400, 80, 80))

            util.write(surface, util.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to pan map", False)

        else:
            util.write(surface, util.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to load map 'basic'",
                       False)
