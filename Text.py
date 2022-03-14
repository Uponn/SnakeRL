import pygame


TEXT_FONT = 20


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