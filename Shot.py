import pygame


class Shot(pygame.sprite.Sprite):
    """
        emanates from gun tube of tank
    """
    # missile fired upwards. Y gets smaller
    y_velocity = -11
    images = []

    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        # put shot on tank gun tube
        self.rect = self.image.get_rect(midbottom=tank)

    def update(self):
        # move missile upward
        self.rect.move_ip(0, self.y_velocity)

        # if missile hits top of screen, destroy
        if (self.rect.top <= 0):
            self.kill()
