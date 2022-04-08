import sys

import pygame


SIZE = 10
SNAKE_LENGTH = 3
NUM_STATES = int(int(sys.argv[1]) / 10)


class Snake:
    def __init__(self, board, apple):
        self.board = board
        self.apple = apple
        self.snake = pygame.Surface((SIZE, SIZE))
        self.rect = None

        self.length = SNAKE_LENGTH
        self.x = []
        self.y = []
        self.set_initial_coords()

    def spawn(self):
        self.draw()

    def set_initial_coords(self):
        self.x = [40, 30, 20]
        self.y = [30, 30, 30]

    def reset_length(self):
        self.length = SNAKE_LENGTH

    def move(self, direction, rect, game, q_learning, mode):
        # take the position of the next element
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if direction == 'right':
            self.x[0] += SIZE
        if direction == 'left':
            self.x[0] -= SIZE
        if direction == 'up':
            self.y[0] -= SIZE
        if direction == 'down':
            self.y[0] += SIZE

        # check if the head of the snake is on the current location of the spawned apple
        if self.__has_eaten_apple():
            self.apple.respawn(self.x, self.y)
            if q_learning is not None:
                q_learning.reset_q_table()
                q_learning.populate_q_table(rect)
            self.__increase_size()
            game.increment_score()

        # checks for border collision
        if self.__border_collision(rect) and mode is None:
            game.game_over()

        # checks for snake collision in itself
        if self.__body_collision() and mode is None:
            game.game_over()

        if game.get_fps() != 0:
            self.draw()

    def __has_eaten_apple(self):
        return True \
            if self.x[0] == self.apple.get_apple_coordinates()[0] and self.y[0] == self.apple.get_apple_coordinates()[1] \
            else False

    def __border_collision(self, rect):
        if self.x[0] > rect.width + SIZE or self.x[0] <= rect.x - SIZE \
                or self.y[0] > rect.height + SIZE or self.y[0] <= rect.y - SIZE:
            return True

    def __body_collision(self):
        if self.x[0] in self.x[1:] and self.y[0] in self.y[1:]:
            return True
        return False

    # increase size of sname and append the new part at the end of the snake
    def __increase_size(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    # draw each snake piece in the next box with the updated coords
    def draw(self):
        for i in range(self.length):
            self.board.blit(self.snake, (self.x[i], self.y[i]))

    def get_length(self):
        return self.length

    def current_state_snake(self):
        return int(((self.x[0] - 20) / 10) + ((self.y[0] - 20) / 10) * NUM_STATES)

    def get_state_for_whole_body(self):
        result = []
        for x, y in zip(self.x, self.y):
            result.append(int(((x - 20) / 10) + ((y - 20) / 10) * NUM_STATES))
        return result

    def get_head_coords(self):
        return self.x[0], self.y[0]

    def get_whole_body_coords(self):
        return [(x, y) for x, y in zip(self.x, self.y)]
