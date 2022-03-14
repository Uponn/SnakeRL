import pygame
import random

SIZE = 10


class Apple:
    def __init__(self, board, borders):
        self.board = board
        self.borders = borders
        self.apple = pygame.Surface((SIZE, SIZE))
        self.apple.fill(pygame.color.Color('red'))
        self.x, self.y = 30, 30

    # initial spawn of apple
    def spawn(self):
        self.board.blit(self.apple, (self.x, self.y))

    def respawn(self, snake_x, snake_y):
        self.x, self.y = self.generate_random_coords()
        if self.apple_in_snake(snake_x, snake_y):
            self.respawn(snake_x, snake_y)
        else:
            self.board.blit(self.apple, (self.x, self.y))

    def get_apple_coordinates(self):
        return [self.x, self.y]

    def generate_random_coords(self):
        self.x = random.randrange(self.borders.rect.x, self.borders.get_width(), SIZE)
        self.y = random.randrange(self.borders.rect.y, self.borders.get_height(), SIZE)
        return self.x, self.y

    def apple_in_snake(self, snake_x, snake_y):
        for i in range(0, len(snake_x)):
            if self.x == snake_x[i] \
                    and self.y == snake_y[i]:
                return True
        return False
