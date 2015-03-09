#!/usr/bin/python

#-----------------------------------------------------------------------------
#                               Juego de damas
#                --------------------------------------------------
# Rios Alejo
# Eyherabide Natalia
# Antinori Nicolas
#-----------------------------------------------------------------------------

import sys

sys.path.append("./engine")
from TableroMM import *

sys.path.append("./gui")
from Gui import *
from Start import *

#Constantes para la grafica
ancho = 950
alto = 750


def seticon(iconname):
    """
    give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel
    
    the windowicon will be set to the bitmap, but the black pixels will be full alpha channel
     
    can only be called once after pygame.init() and before somewindow = pygame.display.set_mode()
    """
    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))#and call that color transparant
    rawicon=pygame.image.load(iconname)#must be 32x32, black is transparant
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)#set wind

def main():

    pygame.init()

    #Ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    seticon("../img/icon.png")
    Ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
    pygame.display.set_caption("Juego de damas")


    #Reloj para controlar el tiempo
    Clock = pygame.time.Clock()

    Gui(Ventana, Clock)


if __name__ == "__main__":
    main()
