class GameState:

    def __init__(self, game):
        self.game = game
        self.prev_state = None


class State:

    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time, events):
        pass

    def render(self, delta_time, surface):
        pass

    def on_enter(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        #self.game.state_switch = True Probably not necessary?

    def exit_state(self):
        self.game.state_stack.pop()
        self.game.state_switch = True
