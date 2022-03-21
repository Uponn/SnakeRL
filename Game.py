import sys
import random

import pygame
import numpy as np

from Apple import Apple
from Borders import Borders
from Snake import Snake
from SnakeRL import Agent
from Text import Text
from QLearning import QLearning


SIZE = 10
PADDING = 40
FPS = 1
MIN_WIDTH_LIMIT = 100
MIN_HEIGHT_LIMIT = 100
MOVES_TO_IDX = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
IDX_TO_MOVES = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}


class Game:
    def __init__(self):
        if int(sys.argv[1]) < MIN_WIDTH_LIMIT and int(sys.argv[1]) / MIN_WIDTH_LIMIT != 0 \
                and int(sys.argv[2]) < MIN_HEIGHT_LIMIT and int(sys.argv[2]) / MIN_HEIGHT_LIMIT != 0:
            raise Exception('x and y should be more than 100 and should be divisible to 100')
        pygame.init()
        self.direction = 'right'
        self.going = True
        self.fps = FPS
        self.score = 0
        self.x = int(sys.argv[1]) + PADDING
        self.y = int(sys.argv[2]) + PADDING
        self.type = sys.argv[3].lower() if len(sys.argv) >= 4 else None
        self.board = pygame.display.set_mode((self.x, self.y))
        self.borders = Borders(self.board, int(sys.argv[1]), int(sys.argv[2]))
        self.apple = Apple(self.board, self.borders)
        self.snake = Snake(self.board)
        self.text = Text(self.board)
        if self.type == 'rl':
            self.agent = Agent(self.board)
            self.q = QLearning(int(self.x / 10) ** 2, 4, self.agent, self.snake, self.apple)
            self.q.populate_q_table(self.borders.draw_borders())
        if self.type == 'a*':
            pass

    def play(self):
        clock = pygame.time.Clock()
        while self.going:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.going = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != 'right':
                        self.direction = 'left'
                    if event.key == pygame.K_RIGHT and self.direction != 'left':
                        self.direction = 'right'
                    if event.key == pygame.K_UP and self.direction != 'down':
                        self.direction = 'up'
                    if event.key == pygame.K_DOWN and self.direction != 'up':
                        self.direction = 'down'
                    if event.key == pygame.K_r and self.fps == 0:
                        self.reset_game()
            self.board.fill(pygame.color.Color('green'))
            rect = self.borders.draw_borders()
            self.apple.spawn()
            if self.is_rl():
                st = self.snake.current_state_snake(self.snake)
                self.direction = IDX_TO_MOVES[int(np.argmax(self.q.q[st]))]
            self.snake.move(self.direction, rect, self.apple, self.q, self)
            pygame.display.flip()

    def increment_score(self):
        self.score += 1

    def game_won(self):
        self.text.display_game_won()
        self.fps = 0

    # def game_over(self):
    #     self.text.display_game_over()
        # time.sleep(50)


    # def reset_game(self):
    #     self.direction = 'right'
    #     self.fps = FPS
    #     self.score = 0
    #     self.snake.reset_length()
    #     self.snake.set_initial_coords()
    #     self.apple.generate_random_coords()
    #     self.play()

    def get_fps(self):
        return self.fps

    def get_snake_body_positions(self):
        return self.x, self.y

    def get_board_width(self):
        return self.x

    def get_percent(self):
        board = (self.board.get_width() - PADDING) / SIZE * (self.board.get_height() - PADDING) / SIZE
        percent = (board - (board - self.snake.get_length())) / board * 100
        return percent

    def is_rl(self):
        return True if self.type == 'rl' else False