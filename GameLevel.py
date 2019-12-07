import pygame
from pygame.locals import Color

class GameLevel(pygame.sprite.Sprite):
    level = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(None, 48)
        self.font.set_bold(1)
        self.color = Color("red")
        self.last_level = -1

        self.update()

        self.rect = self.image.get_rect().move(450, 5)


    def update(self):
        if self.level != self.last_level:
            self.last_level = self.level

            label = "Level: %d" % self.level

            self.image = self.font.render(label, 0, self.color)