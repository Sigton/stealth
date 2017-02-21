import game as g


class Menu:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        self.game = g.Game(display, clock)

    def run(self):

        self.game.run()
