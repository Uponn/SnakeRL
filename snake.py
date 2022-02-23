import sys
import random
import numpy as np

import pygame


SIZE = 10
PADDING = 40
FPS = 1
MIN_WIDTH_LIMIT = 100
MIN_HEIGHT_LIMIT = 100
SNAKE_LENGTH = 5
SNAKE_COORDINATES = 30
TEXT_FONT = 20


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
        self.board = pygame.display.set_mode((self.x, self.y))
        self.borders = Borders(self.board, int(sys.argv[1]), int(sys.argv[2]))
        self.apple = Apple(self.board, self.borders)
        self.snake = Snake(self.board)
        self.text = Text(self.board)

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
            # self.direction = moves[0]
            score = self.snake.move(self.direction, rect, self.apple, self)
            self.text.display_score(self.score)
            self.text.display_percents(self.get_percent())
            pygame.display.flip()

    def increment_score(self):
        self.score += 1

    def game_won(self):
        self.text.display_game_won()
        self.fps = 0

    def game_over(self):
        self.text.display_game_over()
        # time.sleep(50)


    def reset_game(self):
        self.direction = 'right'
        self.fps = FPS
        self.score = 0
        self.snake.reset_length()
        self.snake.set_initial_coords()
        self.apple.generate_random_coords()
        self.play()

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


class Snake:
    def __init__(self, board):
        self.board = board
        self.snake = pygame.Surface((SIZE, SIZE))
        self.rect = None

        self.length = SNAKE_LENGTH
        self.x = []
        self.y = []
        self.set_initial_coords()

    def set_initial_coords(self):
        self.x = [SNAKE_COORDINATES] * self.length
        self.y = [SNAKE_COORDINATES] * self.length

    def reset_length(self):
        self.length = SNAKE_LENGTH

    def compute_possible_moves(self, direction, rect):
        directions = ['up', 'down', 'left', 'right']
        ban_reverse = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        if self.x[0] > rect.width:
            directions.remove('right')
        if self.x[0] <= self.x[0] <= rect.x:
            directions.remove('left')
        if self.y[0] > rect.height:
            directions.remove('down')
        if self.y[0] <= rect.y:
            directions.remove('up')

        if ban_reverse[direction] in directions:
            directions.remove(ban_reverse[direction])

        # for direction in directions:
        #     if direction == 'left':
        #         if self.x[0] - 10 in self.x[1:] and self.y[0] in self.y[1:]:
        #             directions.remove('left')
        #     if direction == 'right':
        #         if self.x[0] + 10 == self.x[1:] and self.y[0] in self.y[1:]:
        #             directions.remove('right')
        #     if direction == 'up':
        #         if self.y[0] - 10 == self.y[1:] and self.x[0] in self.x[1:]:
        #             directions.remove('up')
        #     if direction == 'down':
        #         if self.y[0] + 10 == self.y[1:] and self.x[0] in self.x[1:]:
        #             directions.remove('down')
        # print(directions)
        return directions

    def move(self, direction, rect, apple, game):
        # print('x', self.x)
        # print('y', self.y)
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
        if self.x[0] == apple.get_apple_coordinates()[0] and self.y[0] == apple.get_apple_coordinates()[1]:
            apple.respawn(self.x, self.y)
            self.increase_size()
            game.increment_score()

        # checks for border collision
        if self.border_collision(rect):
            game.game_over()

        # checks for snake collision in itself
        if self.body_collision():
            game.game_over()

        if game.get_fps() != 0:
            self.draw()

        return 10 if self.x[0] == apple.get_apple_coordinates()[0] and self.y[0] == apple.get_apple_coordinates()[1] else -1

    def border_collision(self, rect):
        if self.x[0] > rect.width + SIZE or self.x[0] <= rect.x - SIZE \
                or self.y[0] > rect.height + SIZE or self.y[0] <= rect.y - SIZE:
            return True

    def body_collision(self):
        for i in range(1, self.length):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True

    # increase size of sname and append the new part at the end of the snake
    def increase_size(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    # draw each snake piece in the next box with the updated coords
    def draw(self):
        for i in range(self.length):
            self.board.blit(self.snake, (self.x[i], self.y[i]))

    def get_length(self):
        return self.length


class Apple:
    def __init__(self, board, borders):
        self.board = board
        self.borders = borders
        self.apple = pygame.Surface((SIZE, SIZE))
        self.apple.fill(pygame.color.Color('red'))
        self.x, self.y = self.generate_random_coords()

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


class Text:
    def __init__(self, board):
        self.board = board
        self.font = pygame.font.Font(pygame.font.get_default_font(), TEXT_FONT)

    def display_score(self, score):
        text_surf = self.font.render(f'Score is {score}', False, pygame.color.Color('white'))
        self.board.blit(text_surf, dest=(0, 0))

    def display_percents(self, percent):
        text_surf = self.font.render(f'Progress {percent:.2f}%', False, pygame.color.Color('white'))
        self.board.blit(text_surf, dest=(self.board.get_width() - 160, 0))

    def display_game_over(self):
        game_over = self.font.render('Game Over! Press "R" to Respawn', False, pygame.color.Color('white'))
        rect = game_over.get_rect()
        rect.center = self.board.get_rect().center
        self.board.blit(game_over, rect)

    def display_game_won(self):
        game_won = self.font.render('Game Won! Press "R" to start a new game', False, pygame.color.Color('white'))
        rect = game_won.get_rect()
        rect.center = self.board.get_rect().center
        self.board.blit(game_won, rect)


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


if __name__ == '__main__':
    game = Game()
    game.play()
