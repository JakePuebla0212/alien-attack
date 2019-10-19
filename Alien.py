import pygame
import random


class Alien(pygame.sprite.Sprite):
    # class level variables
    speed = 13
    animation_cycle = 12
    # this is the animation of the alien on the screen
    images = []

    def __init__(self, screen_rectangle):
        """
        this is the constructor! Gets called when class is initialized
        """
        pygame.sprite.Sprite.__init__(self, self.containers)

        # this is our game screen
        # instance variable
        # https://www.digitalocean.com/community/tutorials/understanding-class-and-instance-variables-in-python-3
        self.SCREENRECT = screen_rectangle

        # size the alien game object by using the first
        # image in the collection
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # determine which direction the alien will face/travel when
        # it first appears on screen
        self.direction_factor = random.choice((-1, 1))

        self.x_velocity = self.direction_factor * self.speed

        self.frame = 0

        if (self.x_velocity < 0):
            # if we're facing in a negative direction
            # let's start from the right-hand side
            self.rect.right = self.SCREENRECT.right

    def update(self):
        # let's move the alien left or right!!
        self.rect.move_ip(self.x_velocity, 0)

        # if alien is not on screen!
        if not self.SCREENRECT.contains(self.rect):
            # the alien has gone off screen,
            # let's make it come back on screen
            self.x_velocity = -self.x_velocity

            # let's drop the alien by the height of one alien
            # image to get closer to tank
            self.rect.top = self.rect.bottom + 1

            # this adds alien space ship rectangle back into rectangle \
            # SCREENRECT
            self.rect = self.rect.clamp(self.SCREENRECT)

        self.frame = self.frame + 1

        # flooring division:\
        # https://stackoverflow.com/questions/1535596/what-is-the-reason-for-having-in-python
        # 4.0 // 1.5 => 2.0
        self.image = self.images[self.frame//self.animation_cycle % 3]
