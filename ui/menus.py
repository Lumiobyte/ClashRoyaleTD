import pygame
from pygame.locals import *

import state
import gameview
from ui import util
from constants import *


# TODO: Load the game into the state stack instead of just emptying it. That ain't how a stack works

class HomeMenu(state.State):

    def __init__(self, crtd):
        state.State.__init__(self, crtd)

        self.buttons = [

        ]

    def update(self, delta_time, events):

        # Tick any object as necessary

        for event in events:

            if event.type == KEYDOWN:
                if event.key == K_k:
                    gameview.TestGameView(self.game).enter_state()


            if event.type == MOUSEBUTTONDOWN:
                pass

    def process_buttons(self, click, pos):

        for button in self.buttons:
            button.pro


    def render(self, delta_time, surface):

        surface.fill(Colours.BLACK)
        util.write(surface, TextSize.LARGE_BOLD, Colours.RED, (H_CENTER, 200), "CRTD", True)

        for button in self.buttons:
            button.render()
