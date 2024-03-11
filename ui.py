import pygame


def write(screen, font, colour, location, text, centered=False):
    if centered:
        text_render = font.render(text, True, colour)
        screen.blit(text_render, text_render.get_rect(center=location))
    else:
        screen.blit(font.render(text, True, colour), location)


class TextSize:
    TINY = pygame.font.Font("assets/fonts/segoe/segoe-ui.ttf", 16)
    SMALL = pygame.font.Font("assets/fonts/segoe/segoe-ui.ttf", 24)
    SMALL_BOLD = pygame.font.Font("assets/fonts/segoe/segoe-ui-bold.ttf", 24)
    MEDIUM = pygame.font.Font("assets/fonts/segoe/segoe-ui.ttf", 32)
    LARGE = pygame.font.Font("assets/fonts/segoe/segoe-ui.ttf", 32)
    MED_BOLD = pygame.font.Font("assets/fonts/segoe/segoe-ui-bold.ttf", 48)
    LARGE_BOLD = pygame.font.Font("assets/fonts/segoe/segoe-ui-bold.ttf", 64)
