class GameState:

    def __init__(self, game):
        self.game = game
        self.prev_state = None


class MenuState:

    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time, events):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.ui_state_stack) > 1:
            self.prev_state = self.game.ui_state_stack[-1]
        self.game.ui_state_stack.append(self)

    def exit_state(self):
        self.game.ui_state_stack.pop()
