import pygame
from pygame.locals import Color


class Score(pygame.sprite.Sprite):
    # points scored for hitting aliens are stored in this variable
    score_points = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(None, 48)
        self.font.set_italic(1)
        self.color = Color("white")
        self.last_score = -1

        self.update()

        # place at top left corner of screen
        self.rect = self.image.get_rect().move(20, 5)

    def update(self):
        if (self.score_points != self.last_score):
            self.last_score = self.score_points

            score_message = "Score: %d" % self.score_points

            self.image = self.font.render(score_message, 0, self.color)
