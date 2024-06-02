import pygame
from pygame.locals import *

import state
from ui import util
from constants import *


class HomeMenu(state.MenuState):

    def __init__(self, crtd):
        state.MenuState.__init__(self, crtd)

    def update(self, delta_time, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_k:
                    self.exit_state()

    def render(self, surface):
        surface.fill(Colours.LIGHT_GRAY)
        util.write(surface, TextSize.MEDIUM, Colours.RED, (500, 500), "blah", True)
