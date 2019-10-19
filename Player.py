import pygame


class Player(pygame.sprite.Sprite):
    """
        This is the tank
    """
    speed = 10
    bounce = 24

    # gun tube not in center of sprite
    gun_offset = -11

    images = []

    def __init__(self, screen_rectangle):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.SCREENRECT = screen_rectangle

        self.image = self.images[0]

        self.rect = self.image.get_rect(midbottom=self.SCREENRECT.midbottom)

        self.reloading = 0
        self.origtop = self.rect.top

        # which direction the tank is facing
        self.facing = -1

    def move(self, direction):
        if (direction is not None):
            self.facing = direction

        # moves rectangle (tank) in-place
        # move_ip(change_in_x, change_in_y)
        self.rect.move_ip(self.facing * self.speed, 0)

        # moves one rectangle into another
        # pygame managing game objects in game screen
        self.rect = self.rect.clamp(self.SCREENRECT)

        # if we're going left, show left-facing tank image, vice versa
        if self.facing < 0:
            self.image = self.images[0]
        elif self.facing > 0:
            self.image = self.images[1]

        self.rect.top = self.origtop - (self.rect.left//self.bounce % 2)

    def get_gun_position(self):
        """
            returns the position of the gun, so shot can go out from
            current location of gun tube
        """
        gun_position = self.facing*self.gun_offset + self.rect.centerx

        return gun_position, self.rect.top
