import random

import numpy as np


MOVES_TO_IDX = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
IDX_TO_MOVE = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
MAX_EPISODES = 180
SWITCH_EPISODES = 90


class QLearning:
    def __init__(self, num_states, num_actions, agent, snake, apple, learning_rate=1, discount_factor=1.0):
        self.q_table = np.zeros((num_states, num_actions))
        self.num_states = num_states
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

        for i in range(MAX_EPISODES):
            self.agent.x = self.snake.x.copy()
            self.agent.y = self.snake.y.copy()
            while not self.agent.has_reached_reward(self.apple):
                """ 
                first N numbers of switch_episodes always go into this if statement first, to generate a proper move
                and populate the q_table, in the else statement just pick an already learned route and use it 
                """
                if random.random() > 0.5 or i < SWITCH_EPISODES:
                    moves = self.agent.compute_possible_moves(direction, rect, initial_state)
                    if not moves:
                        break
                    random.shuffle(moves)
                    idx = MOVES_TO_IDX[moves[0]]
                    direction = moves[0]
                else:
                    s = self.agent.state_for_agent()
                    idx = np.argmax(self.q_table[s])
                    direction = IDX_TO_MOVE[int(idx)]

                st = self.agent.state_for_agent()
                at = idx
                score = self.agent.move_for_q_learning(direction, self.apple)
                rt = score
                st1 = self.agent.state_for_agent()
                if 0 < st <= self.num_states or 0 < st1 <= self.num_states:
                    self.update(st, at, rt, st1)
