import pygame
# explosion module, importing Explosion class
from Explosion import Explosion


class Bomb(pygame.sprite.Sprite):
    # class variables
    y_velocity = 9  # change in y-axis.  going in positive direction
    images = []

    def __init__(self, alien):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        # positioning the bomb at the alien
        # ship location
        self.rect = self.image.get_rect(
            midbottom=alien.rect.move(0, 5).midbottom)

    def update(self):
        # drop the bomb!! pass in an x velocity and y velocity
        self.rect.move_ip(0, self.y_velocity)

        # blow up bomb, if it hits the ground
        # where y is 470
        if (self.rect.bottom >= 750):
            Explosion(self)

            self.kill()
