import sys

import pygame
from pygame.locals import *

import ctypes

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

from constants import *
import ui
import worlds
import assets


def setup():
    return pygame.display.set_mode((1920, 1080))


def main():
    screen = setup()
    clock = pygame.time.Clock()
    frame_time = 0

    game_map = None


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if game_map:
                    game_map.pan_viewport(pygame.Vector2(pygame.mouse.get_pos()))
                else:
                    game_map = worlds.load_map(worlds.get_offline_map_list()[0])

                print(pygame.mouse.get_pos())
                print(pygame.mouse.get_rel())

        # Update

        game_map.update()

        # Draw
        screen.fill(Colours.BLACK)

        game_map.render(screen)

        pygame.draw.rect(screen, Colours.PANEL_DARKGREY, pygame.Rect(1550, 0, 370, 1080))

        if game_map:
            ui.write(screen, ui.TextSize.LARGE_BOLD, Colours.WHITE, (1580, 100), "Defenses", False)

            pygame.draw.rect(screen, Colours.LIGHT_GREEN, pygame.Rect(1580, 220, 80, 80))
            pygame.draw.rect(screen, Colours.LIGHT_GREEN, pygame.Rect(1580, 400, 80, 80))
            pygame.draw.rect(screen, Colours.LIGHT_GREEN, pygame.Rect(1700, 220, 80, 80))
            pygame.draw.rect(screen, Colours.LIGHT_GREEN, pygame.Rect(1700, 400, 80, 80))


            ui.write(screen, ui.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to pan map", False)
        else:
            ui.write(screen, ui.TextSize.MEDIUM, Colours.WHITE, (1560, 900), "Click to load map 'basic'", False)


        pygame.display.flip()
        frame_time = clock.tick(FPS)


main()
