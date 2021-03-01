from random import randint

import pyxel
import math
from enum import IntEnum


class Ship:
    WIDTH = 5
    HEIGHT = 5

    def __init__(self, x, y):
        self.coords = [math.floor(x / 2 - self.WIDTH / 2), math.floor(y - 2 * self.HEIGHT)]

    def update(self):
        """
        Update the ship location. Most of the player input happens here.
        """
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            if self.coords[0] < pyxel.width - 15:
                self.coords[0] += 1
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            if self.coords[0] > 10:
                self.coords[0] -= 1
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            if self.coords[1] > pyxel.height - self.HEIGHT * 5:
                self.coords[1] -= 1
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            if self.coords[1] < pyxel.height - self.HEIGHT - 5:
                self.coords[1] += 1

    def draw(self):
        pyxel.blt(*self.coords, 0, 16, 0, 5, 5)


class Swarm:
    WIDTH = 8
    HEIGHT = 8

    def __init__(self, lines=None, coords=None):
        if coords is None:
            coords = [10, 10]
        if lines is None:
            lines = [[1, 1, 0, 1, 1], [0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]
        self.pattern = lines
        self.enemy_sprite = 0
        self.coords = coords
        self.direction = Swarm.Direction.RIGHT

    class Direction(IntEnum):
        RIGHT = 0
        LEFT = 1

    def kill(self, bullet_x, bullet_y):
        """
        Play sound and destroy enemy.
        :param bullet_x:
        :param bullet_y:
        :return:
        """
        x = math.floor((bullet_x - self.coords[0]) / 10)
        y = math.floor((bullet_y - self.coords[1]) / 10)
        pyxel.play(0, 0)
        self.pattern[y][x] = 0

    def update(self):
        if self.direction == 0:
            self.coords[0] += 1
            if self.coords[0] >= pyxel.width - ((max([len(line) for line in self.pattern])+1) * 10):
                self.coords[1] += 4
                self.direction = Swarm.Direction.LEFT
        else:
            self.coords[0] -= 1
            if self.coords[0] <= 10:
                self.coords[1] += 4
                self.direction = Swarm.Direction.RIGHT

    def draw(self):
        sprite_locations = [(0, 0), (8, 0), (0, 8), (8, 8)]
        sprite_index = math.floor(pyxel.frame_count / 5) % 4
        _, y = self.coords
        for line in self.pattern:
            x, _ = self.coords
            for enemy in line:
                if enemy == 1:
                    pyxel.blt(x, y, 0, *sprite_locations[sprite_index], Swarm.WIDTH, Swarm.HEIGHT)
                x += 10
            y += 10


class Bullet:
    def __init__(self, x, y):
        self.active = True
        self.HEIGHT = 2
        self.WIDTH = 1
        self.coords = [x + math.floor(Ship.WIDTH / 2), y - self.HEIGHT]
        self.velocity = 1

    def update(self):
        """
        Check for collision with anything. This will not destroy
        the bullet to ensure it's information is available until
        next update.
        """
        self.coords[1] -= self.velocity
        if pyxel.pget(*self.coords) != pyxel.COLOR_BLACK:
            App.swarm.kill(*self.coords)
            self.active = False
            return
        if self.coords[1] < 10:
            self.active = False

    def draw(self):
        if self.active:
            pyxel.rect(*self.coords, self.WIDTH, self.HEIGHT, pyxel.COLOR_PINK)


class App:
    """
    The main game class. Provides some setup and runs pyxel.
    """

    swarm = Swarm()

    def __init__(self):
        """
        Initialize pyxel and the game objects. Finally, run pyxel.
        """
        pyxel.init(160, 120, caption="pypew", fps=25)
        pyxel.load("assets/pypew.pyxres")
        self.ship = Ship(pyxel.width, pyxel.height)
        self.bullets = []
        self.bullet_delay = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        Update objects. Runs every frame before the draw method.
        Also checks for button presses that affect multiple objects
        or the game.
        """
        if self.bullet_delay > 0:
            self.bullet_delay -= 1
        self.ship.update()
        self.swarm.update()
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.bullet_delay == 0:
                self.bullets.append(Bullet(*self.ship.coords))
                pyxel.play(0, 1)
                self.bullet_delay = 10
        for bullet in self.bullets:
            if not bullet.active:
                self.bullets.remove(bullet)
            else:
                bullet.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """
        Draw objects. The last object drawn will be on top.
        :return:
        """
        pyxel.cls(0)
        self.ship.draw()
        self.swarm.draw()
        for bullet in self.bullets:
            bullet.draw()


App()
