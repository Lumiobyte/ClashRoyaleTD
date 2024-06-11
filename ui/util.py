import pygame
from classes import *
from constants import *
from assets import Image, AnimatedImage


class InputManager:

    def __init__(self):

        self.clicked = False
        self.starting_pos = Point(0, 0)

    def update(self, mouse, keyboard):
        pass

    def get_drag_dist(self):
        if self.clicked:
            pass
        else:
            return Point(0, 0)


def write(screen, font, colour, location, text, centered=False):
    if centered:
        text_render = font.render(text, True, colour)
        screen.blit(text_render, text_render.get_rect(center=location))
    else:
        screen.blit(font.render(text, True, colour), location)


class UITheme:
    BUTTON = [Colours.WHITE, Colours.LIGHT_GRAY]
    INFOBOX = [Colours.INFOBOX_GREY, Colours.INFOBOX_BORDER]


class ButtonType(enum.Enum):
    NORMAL = enum.auto()
    CHECKBOX = enum.auto()


# TODO: Allow buttons to be disabled and not clickable
class Button:
    def __init__(self, button_type: ButtonType, pos: Point, size: Point, title: pygame.Surface, colours: list,
                 images: list | None, actions: list):

        # TODO: Support auto button size: size set to None, automatically set size based on text
        # TODO: Fix or remove checkboxes?

        self.button_type = button_type
        self.pos = pos  # x, y of center
        self.size = size  # width, height
        self.title = title  # Should be a Surface with the rendered text
        self.colours = colours  # [Default BG, Hovered BG]
        self.images = images  # [Default IMG, Hovered IMG] or None if not used
        self.actions = actions  # List of functions

        self.preset_args = []  # List of preset arguments to be passed to actions

        self.auto_size = False
        self.hovered = False
        self.disabled = False

        self.button_rect = pygame.Rect((self.pos.x - self.size.x / 2), (self.pos.y - self.size.y / 2), self.size.x,
                                       self.size.y)

    def setup_args(self, preset_args):
        self.preset_args = preset_args
        return self

    def check(self, mouse_pos: tuple, clicked, action_args=None):

        if self.images:
            current_image = self.images[{True: 1, False: 0}[self.hovered]]
            collide_rect = pygame.Rect((self.pos.x - current_image.get_rect().width / 2),
                                       (self.pos.y - current_image.get_rect().height / 2),
                                       current_image.get_rect().width, current_image.get_rect().height)
        else:
            collide_rect = self.button_rect

        if collide_rect.collidepoint(mouse_pos) and not self.disabled:
            self.hovered = True

            if clicked:
                for i, action in enumerate(self.actions):
                    if self.button_type == ButtonType.CHECKBOX and i == 0:  # Checkbox specific logic - Do not use
                        result = action()
                        if result:
                            self.title = TextSize.SMALL_BOLD.render("X", True, Colours.BLACK)
                            # Always using smallbold does not account for varying button sizes
                            # Need to improve th checked indicator
                            pass
                        else:
                            self.title = None
                    else:

                        # TODO: Return results from action functions
                        if action_args:
                            action(*action_args)
                        elif self.preset_args:
                            action(*self.preset_args)
                        else:
                            action()

                return True

    def render(self, screen, delta):

        if self.images:
            if isinstance(self.images[{True: 1, False: 0}[self.hovered]], AnimatedImage):
                self.images[{True: 1, False: 0}[self.hovered]].tick(delta)
            self.images[{True: 1, False: 0}[self.hovered]].render(screen, self.pos, True)
        else:
            pygame.draw.rect(screen, self.colours[0] if not self.hovered else self.colours[1], self.button_rect)

        if self.button_type == ButtonType.CHECKBOX: # Currently deprecated
            # Interior colour does not account for the main colour being totally black
            top_offset = self.size.y / 8
            left_offset = self.size.x / 8
            interior_rect = pygame.Rect(self.button_rect.left + left_offset, self.button_rect.top + top_offset,
                                        self.size.x - left_offset * 2, self.size.y - top_offset * 2)
            pygame.draw.rect(screen,
                             self.darken_colour(self.colours[0]) if not self.hovered else self.darken_colour(
                                 self.colours[1]), interior_rect)

        if self.title:
            screen.blit(self.title, self.title.get_rect(center=(self.pos.x, self.pos.y)))

        if self.disabled:
            if self.images:
                pass  # TODO: Implement disabled grey-out for image buttons
            else:
                pygame.draw.rect(screen, Colours.RED, self.button_rect)

                # Using a second surface so it can be drawn with transparency, creating greyed-out effect
                disabled_effect = pygame.Surface((self.button_rect.width, self.button_rect.height))
                disabled_effect.set_alpha(64)
                disabled_effect.fill(Colours.RED)
                disabled_effect.blit(screen, (self.button_rect.left, self.button_rect.top))

                # TODO: Grey-out is not working

        self.hovered = False

    def update_title(self, new_title):

        self.title = new_title
        if self.auto_size:
            pass  # Update size

        pass

    def update_theme(self, new_theme):
        self.colours = new_theme

    def update_pos(self, new_pos):
        self.pos = new_pos

    def update_size(self, new_size):
        self.size = new_size

    def darken_colour(self, colour):
        return colour[0] - 40, colour[1] - 40, colour[2] - 40


class ZoomAnimation:

    # TODO: Should support different zooms e.g. linear, lerp, ease in/out via either lambda functions or some setting variable. Also support reversing

    def __init__(self, frames: int, frame_length: float):

        self.frames = frames
        self.frame_length = frame_length

        self.scale_per_frame = 1 / frames

        self.current_frame = 0
        self.time_until_next = self.frame_length

        self.playing = False

    def play(self, size: Point, delta):
        if not self.playing:
            self.playing = True
            self.current_frame = 0

        self.time_until_next -= delta

        if self.time_until_next <= 0:
            if self.current_frame < self.frames:
                self.current_frame += 1
            elif self.current_frame >= self.frames:
                self.playing = False

        scale_fact = self.scale_per_frame * self.current_frame
        return size * scale_fact

    def play_reverse(self, size: Point, delta):
        pass


class InfoBox:
    def __init__(self, size: Point, pos: Point, data: dict, animation: ZoomAnimation):

        self.size = size
        self.scaled_size = self.size

        self.pos = pos  # Will probably just be screen center most of the time

        self.data = data
        # Data format
        # "colour": colour of the infobox
        # "text": list containing tuples of (text object, Point coordinates, centered boolean)
        # "images": list containing tuples of (Image or AnimatedImage object, Point coordinates)
        # "shapes": list containing rects, spheres, etc.
        # "startup_functions": functions only run in open()
        # "functions": references to functions which can be called by this infobox
        # "funcdata": a list of any data needed to be referenced by those functions
        # "buttons": a list of Button objects which can be iterated through to run .process() and .render() on each

        self.animation = animation

        self.newly_opened = True  # Tells the infobox that it just switched from closed to open state

        self.mouse_pos = Point(1280, 720)

    def adjust_cursor(self, mouse_pos):
        return Point(mouse_pos.x - (self.scaled_size.x / 2),
                     mouse_pos.y - (self.scaled_size.y / 2))

    def blit_text(self, dest, text, location, centered=False):
        if centered:
            dest.blit(text, text.get_rect(center=location))
        else:
            dest.blit(text, location)

    def redefine_data(self, data_type, new_data):
        self.data[data_type] = new_data

    def open(self, delta):

        # TODO: Implement newly_opened for infoboxes?
        self.newly_opened = True  # This is later set to false in main function, after the dimming overlay is rendered
        self.animation.play(self.size, delta)

    def process(self, mouse_pos: Point, clicks, keys):

        if self.animation and self.animation.playing:  # Wait until animation is finished before accepting inputs
            return

        # Process all inputs
        self.mouse_pos = self.adjust_cursor(mouse_pos) * (self.size.x / self.scaled_size.x)

        data_buttons = self.data.get("buttons")
        if data_buttons:
            for btn in data_buttons:
                btn.check(self.mouse_pos.tuple(), clicks[0])

    def render(self, screen, delta):

        infobox_surface = pygame.Surface((self.size.x, self.size.y))

        final_size = self.scaled_size
        if self.animation and self.animation.playing:
            final_size = self.animation.play(self.scaled_size, delta)

        # Rendering
        infobox_surface.fill(Colours.BLACK)
        offset = 5
        pygame.draw.rect(infobox_surface, Colours.INFOBOX_BORDER,
                         pygame.Rect(offset, offset, self.size.x - offset * 2, self.size.y - offset * 2))
        pygame.draw.rect(infobox_surface, self.data["colour"],
                         pygame.Rect(offset * 2, offset * 2, self.size.x - offset * 4, self.size.y - offset * 4))

        data_buttons = self.data.get("buttons")

        if data_buttons:
            for btn in data_buttons:
                btn.render(infobox_surface, delta)

        data_text = self.data.get("text")
        if data_text:
            for item in data_text:
                self.blit_text(infobox_surface, item[0], item[1].tuple(), item[2])

        # Scale and blit surface
        infobox_surface = pygame.transform.scale(infobox_surface, final_size.tuple())

        blit_pos = (self.pos.x - (infobox_surface.get_width() / 2), self.pos.y - (infobox_surface.get_height() / 2))
        screen.blit(infobox_surface, blit_pos)

        return pygame.Rect(*blit_pos, self.scaled_size.x, self.scaled_size.y)  # Rect of screen area that was updated
