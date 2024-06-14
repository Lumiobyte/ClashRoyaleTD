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

        self.game_map = worlds.load_map(game, map_meta)

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


class EditorView(state.State):
    def __init__(self, game, map_meta):
        state.State.__init__(self, game)

        self.game_map = worlds.load_map(game, map_meta, True)

        self.buttons = [
            util.Button(util.ButtonType.NORMAL, Point(1740, 560), Point(200, 80),
                        util.TextSize.MINOR_BOLD.render("Move All", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.select_tool]).setup_args([0]),  # Move All
            util.Button(util.ButtonType.NORMAL, Point(1740, 440), Point(80, 80), None,
                        [Colours.BUTTON, Colours.BUTTON_HOVER],
                        [game.assets.get('image.empty'), game.assets.get('image.empty')],
                        [self.select_tool]).setup_args([1]),  # Empty Tile
            util.Button(util.ButtonType.NORMAL, Point(1680, 200), Point(80, 80), None,
                        [Colours.BUTTON, Colours.BUTTON_HOVER],
                        [game.assets.get('image.start'), game.assets.get('image.start')],
                        [self.select_tool]).setup_args([2]),  # Start Tile
            util.Button(util.ButtonType.NORMAL, Point(1800, 200), Point(80, 80), None,
                        [Colours.BUTTON, Colours.BUTTON_HOVER],
                        [game.assets.get('image.path'), game.assets.get('image.path')],
                        [self.select_tool]).setup_args([3]),  # Path Tile
            util.Button(util.ButtonType.NORMAL, Point(1680, 320), Point(80, 80), None,
                        [Colours.BUTTON, Colours.BUTTON_HOVER],
                        [game.assets.get('image.placeable'), game.assets.get('image.placeable')],
                        [self.select_tool]).setup_args([4]),  # Defense Tile
            util.Button(util.ButtonType.NORMAL, Point(1800, 320), Point(80, 80), None,
                        [Colours.BUTTON, Colours.BUTTON_HOVER],
                        [game.assets.get('image.king'), game.assets.get('image.king')],
                        [self.select_tool]).setup_args([5]),  # King Tile


            util.Button(util.ButtonType.NORMAL, Point(1740, 805), Point(200, 80),
                        util.TextSize.MINOR_BOLD.render("VERIFY", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Verify button
            util.Button(util.ButtonType.NORMAL, Point(1740, 905), Point(200, 80),
                        util.TextSize.MINOR_BOLD.render("SAVE", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Save button
            util.Button(util.ButtonType.NORMAL, Point(1740, 1005), Point(200, 80),
                        util.TextSize.MINOR_BOLD.render("EXIT", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Exit button
            util.Button(util.ButtonType.NORMAL, Point(1905, 15), Point(30, 30),
                        util.TextSize.SMALL_BOLD.render("?", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Help button

        ]

        self.map_grabbed = False

        self.tool_selected = None  # When tool selected, cannot pan, and drag click will spread the tile over many.
        self.mouse_gc = GridCoordinate(0, 0)

    def select_tool(self, tool):
        if tool == self.tool_selected:
            self.tool_selected = None
        else:
            self.tool_selected = tool

    def update(self, delta_time, events):

        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_gc = self.game_map.get_gridcoordinate(Point(*mouse_pos))

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                clicked = True

            if event.type == KEYDOWN:
                if event.key == K_PLUS:
                    pass  # Process zoom in
                if event.key == K_MINUS:
                    pass  # Process zoom out
                if event.key == K_SPACE:
                    self.tool_selected = None

        # Map panning
        if self.map_grabbed:
            if pygame.mouse.get_pressed()[0]:
                if self.tool_selected == 0:
                    self.game_map.move_all(Point(*pygame.mouse.get_rel()))
                else:
                    self.game_map.pan_viewport_by(Point(*pygame.mouse.get_rel()))
            else:
                self.map_grabbed = False

        # Map interaction
        if clicked and self.game_map.viewport_area.collidepoint(mouse_pos):
            if self.tool_selected is None or self.tool_selected == 0:  # Pan map or move all tool
                self.map_grabbed = True
                pygame.mouse.get_rel()  # Priming read for get_rel to prevent extraneous values
                self.game_map.reset_move_all()
            else:  # Tile placement tools
                tile_type = TileType(self.tool_selected)
                self.game_map.set_tile(self.mouse_gc, tile_type)

        # Buttons
        for button in self.buttons:
            button.check(mouse_pos, clicked)

    def render(self, delta_time, surface):

        surface.fill(Colours.BLACK)

        self.game_map.render(surface)
        self.game_map.render_grid(surface, Colours.WHITE)
        self.game_map.highlight_tile(surface, self.mouse_gc)

        # Side Panel
        pygame.draw.rect(surface, Colours.ACCENT, pygame.Rect(1540, 0, 370, 1080))
        pygame.draw.rect(surface, Colours.PANEL_DARKGREY, pygame.Rect(1550, 0, 370, 1080))

        # Text
        util.write(surface, util.TextSize.MED_BOLD, Colours.WHITE, (1740, 75), "TILES", True)
        if self.tool_selected is not None:
            util.write(surface, util.TextSize.SMALL, Colours.WHITE, (1740, 680), "Press space to pan map", True)

        # Buttons

        if self.tool_selected is not None:
            outline_rect = self.buttons[self.tool_selected].button_rect.inflate(8, 8)
            pygame.draw.rect(surface, Colours.DARK_GREEN, outline_rect)

        for button in self.buttons:
            button.render(surface, delta_time)