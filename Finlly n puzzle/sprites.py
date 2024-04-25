import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGCOLOUR)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILESIZE < self.game.game_size * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < self.game.game_size * TILESIZE


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, width, height):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = text
        self.font = pygame.font.SysFont("Consolas", 30)
        font_surface = self.font.render(self.text, True, BLACK)
        self.image.fill(WHITE)
        self.font_size = self.font.size(self.text)
        draw_x = (width / 2) - self.font_size[0] / 2
        draw_y = (height / 2) - self.font_size[1] / 2
        self.image.blit(font_surface, (draw_x, draw_y))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen, font_size):
        font = pygame.font.SysFont("Consolas", font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))
