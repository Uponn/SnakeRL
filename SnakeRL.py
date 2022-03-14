import pygame


SIZE = 10
SNAKE_LENGTH = 3

class Agent:
    def __init__(self, board):
        self.board = board
        self.snake = pygame.Surface((SIZE, SIZE))
        self.rect = None

        self.length = SNAKE_LENGTH
        self.x = []
        self.y = []

        self.set_initial_coords()

    def set_initial_coords(self):
        self.x = [70, 60, 50]
        self.y = [30, 30, 30]

    def compute_possible_moves(self, direction, rect, initial_state):
        directions = ['up', 'down', 'left', 'right']
        reverse_direction = {
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

        if reverse_direction[direction] in directions:
            directions.remove(reverse_direction[direction])

        future_state_right = self.get_state_for_agent(self.x[0] + SIZE, self.y[0])
        if future_state_right in initial_state and 'right' in directions:
            directions.remove('right')
        future_state_left = self.get_state_for_agent(self.x[0] - SIZE, self.y[0])
        if future_state_left in initial_state and 'left' in directions:
            directions.remove('left')
        future_state_up = self.get_state_for_agent(self.x[0], self.y[0] - SIZE)
        if future_state_up in initial_state and 'up' in directions:
            directions.remove('up')
        future_state_down = self.get_state_for_agent(self.x[0], self.y[0] + SIZE)
        if future_state_down in initial_state and 'down' in directions:
            directions.remove('down')
        return directions

    def move_for_q_learning(self, direction, reward):
        score = -0.1
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

        if self.check_agent_on_reward(reward):
            score = 10

        return score

    def body_collision(self):
        if self.x[0] in self.x[1:] and self.y[0] in self.y[1:]:
            return True
        return False

    def state_for_agent(self):
        return int(((self.x[0] - 20) / 10) + ((self.y[0] - 20) / 10) * 10)

    def get_state_for_agent(self, x, y):
        return int(((x - 20) / 10) + ((y - 20) / 10) * 10)

    def check_agent_on_reward(self, reward):
        return True \
            if self.x[0] == reward.get_apple_coordinates()[0] and self.y[0] == reward.get_apple_coordinates()[1] \
            else False
