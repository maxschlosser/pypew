import pyxel


class App:
    """
    The main game class. Provides some setup and runs pyxel.
    """

    def __init__(self):
        """
        Initialize pyxel and the game objects. Finally, run pyxel.
        """
        pyxel.init(160, 120, caption="pypew", fps=25)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(pyxel.COLOR_CYAN)

App()
