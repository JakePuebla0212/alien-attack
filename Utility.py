import os.path

import pygame

# root of this aliens project on the disk
main_directory = os.path.split(os.path.abspath(__file__))[0]


def load_image(file_name):
    """
    loads an image, prepares it for play
    """

    file_path_name = os.path.join(main_directory, "data", file_name)

    try:
        surface = pygame.image.load(file_path_name)
    except pygame.error:
        raise SystemExit('Could not load image')
        # raise SystemExit('Could not load image "%s" %s' %
        #                  (file_path_name, pygame.get_error()))

    return surface.convert()


def load_images(*file_names):
    """
    loading animation (multiple images for same sprite)
    """
    images = []

    for file_name in file_names:
        # we call load_image ^^^^^ above this function
        image = load_image(file_name)

        images.append(image)

    return images


class DummySound:
    def play(self):
        pass


def load_sound(file_name):
    # if pygame's mixer (sound) functionality isn't available
    # then return an empty DummySound object
    if (pygame.mixer is None):
        print("Utility - load_sound(), system found pygame mixer disabled.")

        return DummySound()

    file_name = os.path.join(main_directory, 'data', file_name)

    try:
        # retrieve a pygame sound object
        sound = pygame.mixer.Sound(file_name)

        return sound
    except pygame.error:
        print('Warning, unable to load, %s' % file_name)

    return DummySound()
