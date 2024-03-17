from math import floor


class Burst:
    """Горящий шар"""

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.num_img = 0.0
        self.to_erase = False

    def draw(self, game_screen, burst_img):
        game_screen.background.blit(burst_img[floor(self.num_img)], (self.x, self.y))
        if self.num_img < 7:
            self.num_img += 0.075
            # self.num_img += 0.2
        else:
            self.to_erase = True


class Bursts:
    """Коллекция горящих шаров"""

    def __init__(self):
        self.lst = []

    def __iter__(self):
        yield from self.lst

    def __getitem__(self, item):
        return self.lst[item]

    def __len__(self):
        return len(self.lst)

    def draw(self, game_screen, burst_img):
        for ball in self:
            ball.draw(game_screen, burst_img)
            if ball.to_erase:
                self.lst.remove(ball)
