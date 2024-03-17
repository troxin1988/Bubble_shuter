from consts import *

from random import choice, randint

from classes.balls import Ball
from classes.burst_balls import Burst
from classes.calc_coords import CalcCoords

from functions import find_neighbors


class Field(CalcCoords):
    """
    Игровое поле с шарами. Этот класс отвечает за размещение, удаление и рисование шаров
    """

    def __init__(self):
        self.matrix = [[None] * FIELD_WIDTH for _ in range(FIELD_HEIGHT)]
        self.future_ball = Ball(GAME_WIDTH // 2 + BALL_RADIUS * 3, GAME_HEIGHT - BALL_RADIUS * 2, choice(COLORS))
        self.lst_flags = []
        self.lst_to_check = set()
        self.timer = 0
        self.timer_seek = 0
        self.fill()

    def __iter__(self):
        yield from self.matrix

    def __getitem__(self, item):
        return self.matrix[item]

    def __len__(self):
        return len(self.matrix)

    def fill(self):
        """"Заполнение поля случайными шарами"""
        for row in range(10):
            for col in range(FIELD_WIDTH):
                coord_x, coord_y = self.get_abs_coord(row, col)
                self[row][col] = Ball(coord_x, coord_y, choice(COLORS))
                self[row][col].row = row
                self[row][col].col = col

    def draw(self, game_screen, ball_img):
        """Вывод поля на экран"""
        self.timer += self.timer_seek
        for row in range(len(self)):
            for col in range(len(self[row])):
                if isinstance(self[row][col], Ball):
                    self[row][col].draw(game_screen, ball_img)

        # Рисует будущий шар
        self.future_ball.draw(game_screen, ball_img)

    def new_balls(self, game):
        lst = [False] * FIELD_WIDTH

        numbers_balls = NEW_BALLS
        while numbers_balls > 0:
            col = randint(0, FIELD_WIDTH - 1)
            if lst[col] == True:
                continue
            row = 0
            while isinstance(self[row][col], Ball):
                row += 1
            coord_x, coord_y = self.get_abs_coord(row, col)
            self[row][col] = Ball(coord_x, coord_y, choice(COLORS))
            self[row][col].row = row
            self[row][col].col = col
            lst[col] = True
            if row == FIELD_HEIGHT - 2:
                game.status = "gameover"
            numbers_balls -= 1

    def set_flags(self, game, row, col):
        find_neighbors(field=game.field, row=row, col=col, lst=self.lst_flags, prichina="color_ball")

    def drop(self, game):
        """Удаляет отмеченные шары из матрицы (если их 3 или больше) и создает взрывы"""
        if len(self.lst_flags) < 3:
            for row, col in self.lst_flags:
                self[row][col].flag = False
            self.lst_flags.clear()
            game.count_shuts -= 1
            return

        for row, col in self.lst_flags:
            game.bursts.lst.append(Burst(self[row][col].x, self[row][col].y))
            game.sound_explosion.play()
            self.lst_to_check.update(self[row][col].get_neighbors(game.field))
            self[row][col] = None

            game.game_screen.draw()
        game.points += len(self.lst_flags)
        self.lst_flags.clear()
        self.timer_seek = 1

    def reset_free_ball(self, game):
        temp = set()
        temp.update(self.lst_to_check)

        for _ in range(15):
            self.lst_to_check.update(temp)
            temp.clear()
            for row, col in self.lst_to_check:
                if self[row][col] and self.is_free_ball(game.field, row, col):
                    ball_x = self[row][col].x
                    ball_y = self[row][col].y
                    game.bursts.lst.append(Burst(ball_x, ball_y))
                    game.sound_explosion.play()
                    temp.update(self[row][col].get_neighbors(game.field))
                    self[row][col] = None
                    game.points += 2
            self.lst_to_check.clear()

    def is_free_ball(self, field, row, col):
        """
        Проверяет свободен ли шар из списка.
        Не спрашивай почему работает. Я не знаю :)
        """
        find_neighbors(field=field, row=row, col=col, lst=self.lst_flags, prichina="free_ball")
        for coord_i, coord_j in self.lst_flags:
            if coord_i == 0:
                for i in self:
                    for ball in i:
                        if ball:
                            ball.flag = False
                self.lst_flags.clear()
                return False
        self.lst_flags.clear()
        return True
