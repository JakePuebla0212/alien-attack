import pygame
from pygame.locals import Color


class PlayerLives(pygame.sprite.Sprite):
    lives = 5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(None, 48)
        self.font.set_bold(1)
        self.color = Color("red")
        self.last_lives = -1

        self.update()

        self.rect = self.image.get_rect().move(850, 5)

    def update(self):
        if self.lives != self.last_lives:
            self.last_lives = self.lives

            label = "Lives: %d" % self.lives

            self.image = self.font.render(label, 0, self.color)