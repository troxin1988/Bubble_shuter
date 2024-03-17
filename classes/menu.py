import pygame
import os


class Menu:
    def __init__(self, x, y, width, height):
        self.button_img = [
            pygame.image.load(os.path.join("src", "button", "button1.png")).convert_alpha(),
            pygame.image.load(os.path.join("src", "button", "button2.png")).convert_alpha()
        ]

        self.x, self.y = x, y
        self.rect = (width, height)
        self.surface = pygame.Surface(self.rect, pygame.SRCALPHA)
        self.buttons = []

    def add_button(self, padding_txt=0, text="", on_click=lambda x: None):
        x = 0
        y = len(self.buttons) * (62 + 10)
        padding_x = self.x
        padding_y = self.y + y
        self.buttons.append(Button(x, y, padding_x, padding_y, padding_txt, text, on_click))

    def draw(self, surface):
        for button in self.buttons:
            button.draw(self.surface, self.button_img)

        surface.blit(self.surface, (875, 300))


class Button:
    def __init__(self, x, y, padding_x, padding_y, padding_txt=0, text="", on_click=lambda x: None):
        self.x = x
        self.y = y
        self.padding_txt = padding_txt
        self.text = text
        self.state = 0
        self.rect = pygame.rect.Rect(padding_x, padding_y, 247, 62)
        self.text_color = "black"

        self.btn_text = pygame.font.SysFont('Arial Black', 30)
        self.text_btn = self.btn_text.render(self.text, False, self.text_color)
        self.on_click = on_click

    def draw(self, surface, img):
        surface.blit(img[self.state], (self.x, self.y))
        surface.blit(self.text_btn, (self.x + self.padding_txt, self.y + 7))

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            self.text_btn = self.btn_text.render(self.text, False, "white")
        else:
            self.text_btn = self.btn_text.render(self.text, False, "black")
            self.state = 0

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 1

    def handle_mouse_up(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 0
            self.on_click()
