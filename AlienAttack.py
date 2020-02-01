import random
import os.path

import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, K_RIGHT, K_LEFT, K_SPACE, \
    K_ESCAPE, FULLSCREEN

from Alien import Alien
from Bomb import Bomb
from Explosion import Explosion
from GameLevel import GameLevel
from Player import Player
from PlayerLives import PlayerLives
from Score import Score
from Shot import Shot
import Utility

if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

MAX_SHOTS = 2
ALIEN_ODDS = 22
BLACK = (0, 0, 0)
BOMB_ODDS = 80
ALIEN_RELOAD = 12
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
SCREENRECT = Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

main_directory = os.path.split(os.path.abspath(__file__))[0] 


def main(winstyle=0):
    
    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 32, 2, 1024)

    pygame.init()

    winstyle = 0

    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)

    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    set_game_obj_images()

    pygame.mouse.set_visible(0)

    background_tile_image = Utility.load_image("background.gif")

    background = pygame.Surface(SCREENRECT.size)

    for x_position in range(0, SCREENRECT.width,
                            background_tile_image.get_width()):
                            
        background.blit(background_tile_image, (x_position, 0))

    screen.blit(background, (0, 0))

    pygame.display.flip()

    set_game_sound()

    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    all_game_rects = pygame.sprite.RenderUpdates()

    
    

    Player.containers = all_game_rects
    Alien.containers = aliens, all_game_rects
    Shot.containers = shots, all_game_rects
    Bomb.containers = bombs, all_game_rects
    Explosion.containers = all_game_rects
    Score.containers = all_game_rects
    Score.score_points = 0
    PlayerLives.containers = all_game_rects
    PlayerLives.lives = 5
    GameLevel.containers = all_game_rects
    GameLevel.level = 1

    Alien(SCREENRECT)

    if (pygame.font is not None):
        all_game_rects.add(Score())
        all_game_rects.add(PlayerLives())
        all_game_rects.add(GameLevel())

    clock = game_loop(all_game_rects, screen, background, shots, aliens, bombs, winstyle, bestdepth, FULLSCREEN)

    game_over(screen, clock)


def quit_game():
    if (pygame.mixer is not None):
        pygame.mixer.music.fadeout(1000)

        pygame.time.wait(1000)

        pygame.quit()

def set_game_sound():
    if pygame.mixer and not pygame.mixer.get_init():
        print("Warning, no sound")
        pygame.mixer = None

    if pygame.mixer:
        music = os.path.join(main_directory, "data", "house_lo.wav")

        pygame.mixer.music.load(music)

        pygame.mixer.music.set_volume(.2)

        pygame.mixer.music.play(-1)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)

    return textSurface, textSurface.get_rect()

def button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2), (y+(h/2))))

    screen.blit(textSurf, textRect)

def game_over(screen, clock):
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    green = (77, 206, 30)
    white = (255, 255, 255)
    red = (255, 0, 0)
    is_game_over = True

    pygame.mouse.set_visible(1)

    while is_game_over is True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_game()

        screen.fill(white)

        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Game Over", largeText)
        TextRect.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        score_text = "Score:" + str(Score.score_points)

        scoreSurf, scoreRect = text_objects(score_text, largeText)

        scoreRect.center = ((DISPLAY_WIDTH/4), (DISPLAY_HEIGHT/4))
        
        screen.blit(scoreSurf, scoreRect)

        level_text = "Level:" + str(GameLevel.level)

        levelSurf, levelRect = text_objects(level_text, largeText)

        levelRect.center = ((DISPLAY_WIDTH * .75), (DISPLAY_HEIGHT/4))
        
        screen.blit(levelSurf, levelRect)

        mouse = pygame.mouse.get_pos()

        button(screen, "Start Over", 150, 450, 100, 50, green, bright_green, main)

        button(screen, "Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def game_loop(all_game_rects, screen, background, shots, aliens, bombs, winstyle, bestdepth, FULLSCREEN):

    clock = pygame.time.Clock()
    player = Player(SCREENRECT)

    alienreload = ALIEN_RELOAD

    boom_sound = Utility.load_sound("boom.wav")

    shoot_sound = Utility.load_sound("car_door.wav")



    while (player.alive() is True):

        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            elif event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    if not FULLSCREEN:
                        print("Changing to Fullscreen")

        all_game_rects.clear(screen, background)

        all_game_rects.update()

        handle_player_input(player, shots, shoot_sound)

        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            alienreload = ALIEN_RELOAD

            Alien(SCREENRECT)

        # todo: drop bomb at different altitudes
        last_alien = aliens.sprites()[-1]
        first_alien = aliens.sprites()[0]

        if len(aliens.sprites()) > 1:
            second_alien = aliens.sprites()[1]
        
        if len(aliens.sprites()) > 2:
            third_alien = aliens.sprites()[2]

        if len(aliens.sprites()) > 3:
            fourth_alien = aliens.sprites()[3]

        if len(aliens.sprites()) > 4:
            fifth_alien = aliens.sprites()[4]
        
        if len(aliens.sprites()) > 5:
            sixth_alien = aliens.sprites()[5]
          
           if GameLevel.level == 2:
            if last_alien is not None and last_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(last_alien)

        if GameLevel.level == 3:
            if last_alien is not None and last_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(last_alien)

        if GameLevel.level == 4:
            if last_alien is not None and last_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(last_alien)

        if GameLevel.level == 5:
            if sixth_alien is not None and sixth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(sixth_alien)

        if GameLevel.level == 6:
            if sixth_alien is not None and sixth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(sixth_alien)

        if GameLevel.level == 7:
            if sixth_alien is not None and sixth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(sixth_alien) 

        if GameLevel.level == 8:
            if sixth_alien is not None and sixth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(sixth_alien)

        if GameLevel.level == 9:
            if sixth_alien is not None and sixth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(sixth_alien)

        if GameLevel.level == 10:
            if fifth_alien is not None and fifth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(fifth_alien)

        if GameLevel.level == 11:
            if fifth_alien is not None and fifth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(fifth_alien)

        if GameLevel.level == 12:
            if fourth_alien is not None and fourth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(fourth_alien)
 
        if GameLevel.level == 13:
            if fourth_alien is not None and fourth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(fourth_alien)

        if GameLevel.level == 14:
            if fourth_alien is not None and fourth_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(fourth_alien)

        if GameLevel.level == 15:
            if third_alien is not None and third_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(third_alien)

        if GameLevel.level == 16:
            if third_alien is not None and third_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(third_alien)

        if GameLevel.level == 17:
            if second_alien is not None and second_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(second_alien)

        if GameLevel.level == 18:
            if second_alien is not None and second_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(second_alien)

        if GameLevel.level == 19:
            if second_alien is not None and second_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(second_alien)

        if GameLevel.level == 20:
            if first_alien is not None and first_alien.rect.y > 50 and not int(random.random() * BOMB_ODDS):
                Bomb(first_alien)

        


        detect_collisions(player, aliens, shots, bombs, boom_sound)

        is_dirty = all_game_rects.draw(screen)
        pygame.display.update(is_dirty)

        clock.tick(40)

    return clock

def check_player_life(player):
    if (PlayerLives.lives < 1):
        player.kill()

def handle_player_input(player, shots, shoot_sound):
    keystate = pygame.key.get_pressed()

    direction = keystate[K_RIGHT] - keystate[K_LEFT]

    player.move(direction)

    firing = keystate[K_SPACE]

    if not player.reloading and firing and len(shots) < MAX_SHOTS:
        Shot(player.get_gun_position())
        shoot_sound.play()

    player.reloading = firing

def detect_collisions(player, aliens, shots, bombs, boom_sound):
    for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
        boom_sound.play()
        Explosion(alien)

        Score.score_points = Score.score_points + 1

        check_game_level(Score.score_points)

    for bomb in pygame.sprite.spritecollide(player, bombs, 1):
        boom_sound.play()

        Explosion(player)
        Explosion(bomb)

        PlayerLives.lives = PlayerLives.lives - 1

        check_player_life(player)

    for bomb in pygame.sprite.groupcollide(shots, bombs, 1, 1).keys():
        boom_sound.play()
        bomb.kill()
        Explosion(bomb)

def check_game_level(score):
    if(GameLevel.level == 1 and score > 9):
        GameLevel.level = 2
    elif(GameLevel.level == 2 and score > 19):
        GameLevel.level = 3
    elif(GameLevel.level == 3 and score > 29):
        GameLevel.level = 4
    elif(GameLevel.level == 4 and score > 39):
        GameLevel.level = 5
    elif(GameLevel.level == 5 and score > 54):
        GameLevel.level = 6
    elif(GameLevel.level == 6 and score > 69):
        GameLevel.level = 7
    elif(GameLevel.level == 7 and score > 84):
        GameLevel.level = 8
    elif(GameLevel.level == 8 and score > 99):
        GameLevel.level = 9
    elif(GameLevel.level == 9 and score > 114):
        GameLevel.level = 10
    elif(GameLevel.level == 10 and score > 134):
        GameLevel.level = 11
    elif(GameLevel.level == 11 and score > 154):
        GameLevel.level = 12
    elif(GameLevel.level == 12 and score > 174):
        GameLevel.level = 13
    elif(GameLevel.level == 13 and score > 194):
        GameLevel.level = 14
    elif(GameLevel.level == 14 and score > 214):
        GameLevel.level = 15
    elif(GameLevel.level == 15 and score > 239):
        GameLevel.level = 16
    elif(GameLevel.level == 16 and score > 264):
        GameLevel.level = 17
    elif(GameLevel.level == 17 and score > 289):
        GameLevel.level = 18
    elif(GameLevel.level == 18 and score > 314):
        GameLevel.level = 19
    elif(GameLevel.level == 19 and score > 339):
        GameLevel.level = 20
    
def set_game_obj_images():
    player_image = Utility.load_image("player1.gif")

    Player.images = [player_image, pygame.transform.flip(player_image, 1, 0)]

    explosion_image = Utility.load_image("explosion1.gif")

    Explosion.images = [explosion_image,
                pygame.transform.flip(explosion_image, 1, 1)]

    Alien.images = Utility.load_images(
            "alien1.gif", "alien2.gif", "alien3.gif")

    Bomb.images = [Utility.load_image("bomb.gif")]  
    
    Shot.images = [Utility.load_image("shot.gif")]

    icon = pygame.transform.scale(Alien.images[0], (32, 32))

    pygame.display.set_icon(icon)

    pygame.display.set_caption("Alien Attack")


if (__name__ == "__main__"):
    main()