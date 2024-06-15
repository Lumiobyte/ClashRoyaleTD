import pygame
from pygame.locals import *
import math

import state
import gameview
import worlds
import misc
from ui import util
from constants import *
from classes import *


class HomeMenu(state.State):

    def __init__(self, crtd):
        state.State.__init__(self, crtd)

        self.buttons = [
            util.Button(util.ButtonType.NORMAL, Point(H_CENTER, 800), Point(300, 150),
                        util.TextSize.SMALL_BOLD.render("PLAY", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [MapSelectMenu(self.game).enter_state])
        ]

    def update(self, delta_time, events):

        # Tick any object as necessary

        clicked = False
        for event in events:

            if event.type == KEYDOWN:
                if event.key == K_k:
                    gameview.TestGameView(self.game).enter_state()


            if event.type == MOUSEBUTTONDOWN:
                clicked = True

        self.process_buttons(pygame.mouse.get_pos(), clicked)

    def process_buttons(self, pos, clicked):

        for button in self.buttons:
            button.check(pos, clicked)


    def render(self, delta_time, surface):

        surface.fill(Colours.BLACK)
        util.write(surface, TextSize.MEGA_BOLD, Colours.RED, (H_CENTER, 200), "CRTD", True)

        for button in self.buttons:
            button.render(surface, delta_time)


class MapSelectMenu(state.State):
    def __init__(self, crtd):
        state.State.__init__(self, crtd)

        self.crtd = crtd

        # TODO: Scroll buttons use images
        self.buttons = [
            util.Button(util.ButtonType.NORMAL, Point(160, 1005), Point(150, 80),
                        util.TextSize.MINOR_BOLD.render("BACK", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Back button
            util.Button(util.ButtonType.NORMAL, Point(700, 1005), Point(190, 80),
                        util.TextSize.MINOR_BOLD.render("GET MAPS", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Download maps button
            util.Button(util.ButtonType.NORMAL, Point(920, 1005), Point(190, 80),
                        util.TextSize.MINOR_BOLD.render("REFRESH", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.refresh_offline_maps]),  # Refresh map list button
            util.Button(util.ButtonType.NORMAL, Point(1140, 1005), Point(190, 80),
                        util.TextSize.MINOR_BOLD.render("CREATE MAP", True, Colours.BLACK),
                        [Colours.BUTTON, Colours.BUTTON_HOVER], None, [self.exit_state]),  # Create map button
        ]

        # Buttons which need special processing are checked separately
        self.play_button = util.Button(util.ButtonType.NORMAL, Point(1760, 1005), Point(150, 80), util.TextSize.MINOR_BOLD.render("PLAY", True, Colours.BLACK), [Colours.BUTTON, Colours.BUTTON_HOVER], None, [])
        self.edit_button = util.Button(util.ButtonType.NORMAL, Point(1580, 1005), Point(150, 80), util.TextSize.MINOR_BOLD.render("EDIT", True, Colours.BLACK), [Colours.BUTTON, Colours.BUTTON_HOVER], None, [])

        self.offline_maps = worlds.get_offline_map_list()

        self.scroll_offset = 0
        self.scroll_limit = 500
        self.manual_scroll_dist = 100
        self.visible_bounds = (160, 920)

        self.map_card_rects = []
        self.hovered_index = None
        self.selected_index = None
        self.generate_map_card_rects()

        self.scrollbar_grabbed = False
        self.scrollbar_rect = None
        self.set_scrollbar_rect()

    def on_enter(self):
        self.refresh_offline_maps()

    def refresh_offline_maps(self):
        self.offline_maps = worlds.get_offline_map_list()

    def update(self, delta_time, events):
        # TODO: Test with a mouse scroll wheel

        # Iterate events
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        for event in events:

            if event.type == MOUSEWHEEL:
                mult = math.exp(abs(event.precise_y) / 3)  # misc.para_multiplier(abs(event.precise_y), 0, 2)
                self.scroll_offset = misc.clamp(self.scroll_offset + (10 * -event.precise_y * mult), 0, self.scroll_limit)

                self.generate_map_card_rects()
                self.set_scrollbar_rect()

            elif event.type == MOUSEBUTTONDOWN:
                clicked = True

        # Mouse interaction for map cards
        map_hovered = False
        for i, card_rect in enumerate(self.map_card_rects):
            if (160 < mouse_pos[1] < 920) and card_rect.collidepoint(mouse_pos):
                self.hovered_index = i
                if clicked:
                    self.selected_index = i

                map_hovered = True
                break

        if not map_hovered:
            self.hovered_index = None

        # Check buttons
        for button in self.buttons:
            button.check(mouse_pos, clicked)

        if self.selected_index is not None:
            if self.play_button.check(mouse_pos, clicked):
                # gameview.TestGameView(self.crtd, self.offline_maps[self.selected_index]).enter_state()
                pass
            if self.edit_button.check(mouse_pos, clicked) and self.offline_maps[self.selected_index].editable:
                loaded_map = worlds.load_map(self.crtd, self.offline_maps[self.selected_index], True)
                if isinstance(loaded_map, str):
                    print(loaded_map)
                    # Set current info box to a messagebox with message of the above.
                else:
                    gameview.EditorView(self.crtd, loaded_map).enter_state()

        if self.scrollbar_grabbed:
            if pygame.mouse.get_pressed()[0]:
                self.scroll_offset = misc.clamp(self.scroll_offset + (pygame.mouse.get_rel()[1] / self.calculate_scrollbar_scaling()), 0, self.scroll_limit)
                self.generate_map_card_rects()
                self.set_scrollbar_rect()
            else:
                self.scrollbar_grabbed = False

        if self.scrollbar_rect.collidepoint(mouse_pos) and clicked:
            self.scrollbar_grabbed = True
            pygame.mouse.get_rel()  # Prime get_rel so that scrollbar won't jump next frame

    def generate_map_card_rects(self):
        # Generate rects indicating the locations of map info cards in the map selector
        # Only regenerate upon scroll movement

        num_cards = len(self.offline_maps)
        current_corner_y = 200

        card_rects = []
        for i in range(num_cards):
            card_corner_x = [H_CENTER - 600, H_CENTER + 100][i % 2]  # Flip-flop between left and right column
            card_corner_y = current_corner_y - self.scroll_offset

            card_rects.append(pygame.Rect(card_corner_x, card_corner_y, 500, 400))  # Card size is 500 x 400

            if i < num_cards - 1: # Do not increment if this is the last card
                current_corner_y += (450 * (i % 2))  # Only increment every second card - two cards per row

        self.map_card_rects = card_rects
        self.scroll_limit = current_corner_y - 200


    def calculate_scrollbar_scaling(self):
        return 740 / (self.scroll_limit + 740)

    def set_scrollbar_rect(self):
        scaling = self.calculate_scrollbar_scaling()

        sc_height = 740 * scaling
        sc_y_offset = 0 + (self.scroll_offset * scaling)

        self.scrollbar_rect = pygame.Rect(1870, 170 + sc_y_offset, 40, sc_height)

    def render_map_cards(self, surface):
        for i, meta in enumerate(self.offline_maps):
            card_rect = self.map_card_rects[i]

            if card_rect.bottom < self.visible_bounds[0] or card_rect.top > self.visible_bounds[1]:
                continue  # Do not render if no part of the card is visible

            # Hover/select highlight
            if i == self.selected_index:
                pygame.draw.rect(surface, Colours.GREEN, card_rect.inflate(15, 15))
            elif i == self.hovered_index:
                pygame.draw.rect(surface, Colours.DARK_GREEN, card_rect.inflate(15, 15))

            pygame.draw.rect(surface, Colours.WHITE, card_rect)
            surface.blit(meta.thumb, (card_rect.left, card_rect.top))

            util.write(surface, TextSize.MINOR_BOLD, Colours.BLACK, (card_rect.left + 20, card_rect.top + 310), meta.name)
            util.write(surface, TextSize.SMALL, Colours.BLACK, (card_rect.left + 20, card_rect.top + 350), "by " + meta.author)

    def render(self, delta_time, surface):

        surface.fill(Colours.BLACK)

        # Map Cards
        self.render_map_cards(surface)

        # Panels
        pygame.draw.rect(surface, Colours.PANEL_DARKGREY, pygame.Rect(1860, 0, 60, 1080))  # Scrollbar panel
        pygame.draw.rect(surface, Colours.ACCENT, pygame.Rect(0, 920, 1920, 150))
        pygame.draw.rect(surface, Colours.PANEL_DARKGREY, pygame.Rect(0, 930, 1920, 150))
        pygame.draw.rect(surface, Colours.ACCENT, pygame.Rect(0, 10, 1920, 150))
        pygame.draw.rect(surface, Colours.PANEL_DARKGREY, pygame.Rect(0, 0, 1920, 150))

        # Scrollbar
        pygame.draw.rect(surface, Colours.BUTTON_HOVER if self.scrollbar_grabbed else Colours.BUTTON, self.scrollbar_rect)

        # Text
        util.write(surface, TextSize.MEGA_BOLD, Colours.ACCENT, (H_CENTER, 80), "MAPS", True)

        # TODO: Don't render buttons if no map selected, instead replace with a text saying "Select a map"

        # Buttons
        for button in self.buttons:
            button.render(surface, delta_time)

        self.play_button.render(surface, delta_time)

        if self.selected_index is not None:
            self.edit_button.disabled = not self.offline_maps[self.selected_index].editable

            self.edit_button.render(surface, delta_time)

            # TODO: Should render some symbol on the map card if it has origin=online
