import pygame
from pygame import surface
from gui.gui import Gui

# Constantes para la grafica
WIDTH = 950
HEIGHT = 750

def seticon(iconname):
    """
    give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel

    the window icon will be set to the bitmap, but the black pixels will be full alpha channel

    can only be called once after pygame.init() and before some window = pygame.display.set_mode()
    """
    icon = surface.Surface((32, 32))
    icon.set_colorkey((0, 0, 0))  # and call that color transparant
    # must be 32x32, black is transparant
    rawicon = pygame.image.load(iconname)
    for i in range(0, 32):
        for j in range(0, 32):
            icon.set_at((i, j), rawicon.get_at((i, j)))
    pygame.display.set_icon(icon)  # set wind


def main():
    """
    Launches the game
    """
    pygame.init()

    seticon("../img/icon.png")
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Juego de damas")

    # Reloj para controlar el tiempo
    clock = pygame.time.Clock()

    Gui(window, clock)


if __name__ == "__main__":
    main()
