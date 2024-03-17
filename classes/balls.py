from consts import *
from classes.calc_coords import CalcCoords
from math import atan2, cos, sin, sqrt
from functions import find_neighbors
from random import choice


class Ball(CalcCoords):
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.row = self.col = 0
        self.color = color
        self.flag = False

    def __eq__(self, other):
        if type(other) is Ball:
            return self.color == other.color

    def get_neighbors(self, field):
        neighbors = []
        find_neighbors(field=field, row=self.row, col=self.col, lst=neighbors)
        return neighbors

    def draw(self, game_screen, ball_img):
        game_screen.background.blit(ball_img[self.color], (self.x, self.y))


class Player(Ball):
    """Шар, готовый к выстрелу"""

    def __init__(self, x, y, color):
        super().__init__(x, y, color)

        self.is_touched = False
        self.dx = 0
        self.dy = 0

    @property
    def is_flying(self) -> bool:
        return self.dx != 0 or self.dy != 0

    def draw(self, game_screen, ball_img):
        game_screen.background.blit(ball_img[self.color], (self.x, self.y))

    def shut(self, mouse_pos: tuple):
        mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
        angle = atan2(mouse_y - self.y - BALL_RADIUS, mouse_x - self.x - BALL_RADIUS)
        self.dx = cos(angle)
        self.dy = sin(angle)

    def move(self, game):
        self.x += 7 * self.dx
        self.y += 7 * self.dy
        if self.x >= GAME_WIDTH - BALL_RADIUS * 2 or self.x <= 0:
            self.dx = -self.dx
        if self.y <= 0:
            self.dy = -self.dy
        self.check_touch(game.field)

    def check_touch(self, field):
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j] and \
                        sqrt((field[i][j].x - self.x) ** 2 + (field[i][j].y - self.y) ** 2) <= BALL_RADIUS * 2 - 10:
                    self.set_abs_coord(self.x, self.y)
                    self.is_touched = True
