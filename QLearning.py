import random

import numpy as np


MOVES_TO_IDX = {'up': 0, 'down': 1, 'left': 2, 'right': 3}


class QLearning:
    def __init__(self, num_states, num_actions, agent, snake, apple, learning_rate=0.1, discount_factor=1.0):
        self.q_table = np.zeros((num_states, num_actions))
        self.a = learning_rate
        self.g = discount_factor
        self.agent = agent
        self.snake = snake
        self.apple = apple

    def update(self, st, at, rt, st1):
        self.q_table[st, at] = (1 - self.a) * self.q_table[st, at] + self.a * (rt + self.g * np.max(self.q_table[st1]))

    def reset_q_table(self):
        self.q_table.fill(0)

    def populate_q_table(self, rect):
        initial_state = self.snake.get_state_for_whole_body()
        direction = 'right'
        for i in range(1000):
            self.agent.x = self.snake.x.copy()
            self.agent.y = self.snake.y.copy()
            flag = True
            while flag:
                st = self.agent.state_for_agent()
                moves = self.agent.compute_possible_moves(direction, rect, initial_state)
                if not moves:
                    break
                random.shuffle(moves)
                at = MOVES_TO_IDX[moves[0]]
                direction = moves[0]
                score = self.agent.move_for_q_learning(direction, self.apple)
                rt = score
                st1 = self.agent.state_for_agent()
                self.update(st, at, rt, st1)
                if self.agent.x[0] == self.apple.get_apple_coordinates()[0] and self.agent.y[0] == \
                        self.apple.get_apple_coordinates()[1]:
                    break
