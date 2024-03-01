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

    tiles = pygame.sprite.Group()
    tiles.add(worlds.Tile(TileType.START, pygame.Vector2(800, 800)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        # Update

        tiles.update()

        # Draw

        screen.fill(Colours.BLACK)

        tiles.draw(screen)

        ui.write(screen, ui.TextSize.MEDIUM, Colours.WHITE, (500, 500), "game", True)

        pygame.display.flip()
        frame_time = clock.tick(FPS)


main()
