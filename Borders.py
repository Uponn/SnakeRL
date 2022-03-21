import pygame


class Borders:
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y
        self.rect = self.draw_borders()

    def draw_borders(self):
        return pygame.draw.rect(self.board, pygame.color.Color('black'), pygame.Rect(20, 20, self.x, self.y), 2)

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height