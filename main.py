import pygame
import sys
import os

from abc import ABC, abstractmethod
from random import choice
from math import atan2, pi

from consts import *

from classes.field import Field
from classes.balls import Player, Ball
from classes.burst_balls import Bursts
from classes.menu import Menu

pygame.init()
display = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
clock = pygame.time.Clock()

ball_img = {}
for color in COLORS:
    source_burst_img = ["src", f"{color}.png"]
    source = os.path.join(*source_burst_img)
    ball_img[color] = pygame.image.load(source).convert_alpha()

burst_img = []
for i in range(8):
    source_burst_img = ["src", "burst", f"burst{i}.png"]
    source = os.path.join(*source_burst_img)
    burst_img.append(pygame.image.load(source).convert_alpha())

sounds = ["shut", "explosion", "touch"]
sounds_wav = {}
for sound in sounds:
    source_sound = ["snd", f"{sound}.wav"]
    source = os.path.join(*source_sound)
    sounds_wav[sound] = pygame.mixer.Sound(source)


class Mouse:
    x = y = None

    def draw(self):
        self.x, self.y = self.get_pos()
        if 0 <= self.x <= GAME_WIDTH and 0 <= self.y <= GAME_HEIGHT:
            self.x -= 10
            self.y -= 10

    def get_pos(self):
        return pygame.mouse.get_pos()


class DrawScreen(ABC):
    @staticmethod
    @abstractmethod
    def concrete_draw():
        pass


class DrawPlay(DrawScreen):
    @staticmethod
    def concrete_draw():
        game.mouse.draw()
        game.bursts.draw(game.game_screen, burst_img)


class DrawGameOver(DrawScreen):
    text = pygame.font.SysFont('Arial Black', 90)
    text_game_over = text.render("ПОТРАЧЕНО", False, "white")

    @staticmethod
    def concrete_draw():
        game.game_screen.background.blit(DrawGameOver.text_game_over, (100, 200))


class GameScreen:
    """Игровой экран"""

    def __init__(self, draw_screen: DrawScreen):
        self.color = (0, 200, 255)
        self.rect = (GAME_WIDTH, GAME_HEIGHT)
        self.background = pygame.Surface(self.rect)
        self.bg = pygame.image.load(os.path.join("src", "background.png")).convert_alpha()
        # Паттерн Strategy для смены отображения экрана
        self.concrete_draw = draw_screen.concrete_draw

    def set_draw_screen(self, draw_screen: DrawScreen):
        self.concrete_draw = draw_screen.concrete_draw

    def draw(self):
        game.game_screen.background.blit(game.game_screen.bg, (0, 0))
        game.field.draw(game.game_screen, ball_img)
        self.concrete_draw()
        game.player.draw(game.game_screen, ball_img)
        game.gun.draw()
        display.blit(game.game_screen.background, (10, 10))
        game.menu.draw(display)


class Gun:
    def __init__(self):
        self.gun_img = pygame.image.load(os.path.join("src", "gun.png")).convert_alpha()
        self.x = GAME_WIDTH // 2
        self.y = GAME_HEIGHT - 10

    def rotate(self, mouse_pos: tuple):
        mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
        rel_x, rel_y = mouse_x - self.x - 10, mouse_y - self.y
        angle = (180 / pi) * -atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.gun_img, int(angle))
        self.rect = self.image.get_rect(center=(self.x, self.y - 32))

    def draw(self):
        game.game_screen.background.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.create_menu()
        self.game_screen = GameScreen(DrawPlay())
        self.mouse = Mouse()
        self.gun = Gun()
        self.field = Field()
        self.bursts = Bursts()
        self.player = Player(GAME_WIDTH // 2 - BALL_RADIUS, GAME_HEIGHT - BALL_RADIUS * 2, self.field.future_ball.color)
        self.field.future_ball.color = choice(COLORS)

        self.status = "play"
        self.count_shuts = SHUTS
        self.points = 0
        self.text = pygame.font.SysFont('Comic Sans MS', 60)
        self.sound_explosion = sounds_wav["explosion"]

    def create_menu(self):
        self.menu = Menu(880, 300, 247, 500)
        self.menu.add_button(25, "Новая игра", self.new_game)
        self.menu.add_button(65, "Выход", self.exit_game)

    def new_game(self):
        self.__init__()

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def gameover(self):
        self.game_screen.set_draw_screen(DrawGameOver())

    def play(self):
        if self.field.timer >= 90:
            self.field.reset_free_ball(self)
            self.field.timer = 0
            self.field.timer_seek = 0
        if self.player.is_flying:
            self.player.move(self)
            if self.player.y > SCR_HEIGHT:
                self.player = Player(GAME_WIDTH // 2 - BALL_RADIUS, GAME_HEIGHT - BALL_RADIUS * 2,
                                     game.field.future_ball.color)
        if self.player.is_touched:
            sounds_wav["touch"].play()
            i, j = self.player.get_rel_coord(self.player.x, self.player.y)
            self.field[i][j] = Ball(self.player.x, self.player.y, self.player.color)
            self.field[i][j].row = i
            self.field[i][j].col = j
            if i == FIELD_HEIGHT - 2:
                self.status = "gameover"

            self.field.set_flags(self, i, j)
            self.field.drop(self)
            if self.count_shuts == 0:
                self.field.new_balls(game)
                self.count_shuts = SHUTS

            future_color = self.field.future_ball.color
            self.player = Player(GAME_WIDTH // 2 - BALL_RADIUS, GAME_HEIGHT - BALL_RADIUS * 2, future_color)
            self.field.future_ball.color = choice(COLORS)

        self.gun.rotate(self.mouse.get_pos())

    def start(self):
        while True:
            display.fill((146, 84, 11))
            text_points = self.text.render(f"{str(self.points).zfill(7)}", False, (255, 255, 255))
            display.blit(text_points, (880, 200))

            if self.status == "play":
                self.play()
            elif self.status == "gameover":
                self.gameover()

            self.game_screen.draw()

            pygame.display.update()

            for event in pygame.event.get():
                for button in self.menu.buttons:
                    button.handle_mouse_event(event.type, self.mouse.get_pos())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if 0 <= self.mouse.x <= GAME_WIDTH and 0 <= self.mouse.y <= GAME_HEIGHT:
                            if not self.player.is_flying:
                                sounds_wav["shut"].play()
                                self.player.shut(self.mouse.get_pos())

            clock.tick(160)


if __name__ == "__main__":
    game = Game()
    game.start()
