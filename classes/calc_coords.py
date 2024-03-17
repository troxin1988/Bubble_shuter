from consts import *


class CalcCoords:
    """Класс рассчитывает координаты шаров"""
    x = y = None

    @staticmethod
    def get_abs_coord(row, col):
        """Расчет координат относительно экрана"""
        x = col * (BALL_RADIUS + 1) * 2 + row % 2 * BALL_RADIUS + 2
        y = row * (BALL_RADIUS * 2 - 6)
        return x, y

    @staticmethod
    def get_rel_coord(x, y):
        """Расчет координат относительно матрицы поля"""
        row = round(y / (BALL_RADIUS * 2 - 6))
        col = round((x - row % 2 * BALL_RADIUS - 2) / ((BALL_RADIUS + 1) * 2))
        # Иногда функция рассчитывает j таким образом,
        # что он находится за пределами поля. Возвращаем назад в поле
        if col > FIELD_WIDTH - 1:
            col = FIELD_WIDTH - 1
        if col < 0:
            col = 0
        return row, col

    def set_abs_coord(self, x, y):
        """Установка новых (правильных) координат в ячейках поля"""
        row, col = self.get_rel_coord(x, y)
        self.x, self.y = self.get_abs_coord(row, col)
