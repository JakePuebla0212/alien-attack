import pygame


class Explosion(pygame.sprite.Sprite):
    default_life = 12
    animation_cycle = 3
    images = []

    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        # put the explosion on top of alien/tank
        self.rect = self.image.get_rect(center=actor.rect.center)

        # assign class variable value to instance variable
        self.current_life = self.default_life

    def update(self):
        """
            explosion will last 12 frames (default life)
        """
        self.current_life = self.current_life - 1

        # advance to next image for explosion animation
        self.image = self.images[self.current_life//self.animation_cycle % 2]

        if (self.current_life <= 0):
            # hide explosion object
            self.kill()
