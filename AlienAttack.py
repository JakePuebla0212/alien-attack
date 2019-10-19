import random
import os.path

import pygame
from pygame.locals import rect, QUIT, KEYDOWN, K_RIGHT, K_LEFT, K_SPACE, \
    K_ESCAPE, FULLSCREEN

from Alien import Alien
from Bomb import Bomb
from Explosion import Explosion
from Player import Player
from PlayerLives import PlayerLives
from Score import Score
from Shot import Shot
import Utility

if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

MAX_SHOTS = 2
ALIEN_ODDS = 22
BOMB_ODDS = 60
ALIEN_RELOAD = 12
SCREENRECT = rect(0, 0, 1024, 768)

main_directory = os.path.split(os.path.abspath(__file__))[0]


def main(winstyle=0):
    pass

    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 32, 2, 1024)

    pygame.init()

    winstyle = 0

    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)

    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    set_game_obj_images()

    pygame.mouse.set_visible(0)


def set_game_obj_images():
    player_image = Utility.load_image("player1.gif")

    Player.images = [player_image, pygame.transform.flip(player_image, 1, 0)]

    explosion_image = Utility.load_image("explosion.gif")

    Explosion.image = [explosion_image,
                pygame.transform.flip(explosion_image, 1, 1)]

    Alien.images = Utility.load.images(
            "alien1.gif", "alien2.gif", "alien3.gif")

    Bomb.images = [Utility.load_image("bomb.gif")]  
    
    Shot.images = [Utility.load_image("shot.gif")]


if (__name__ == "__main__"):
    main()