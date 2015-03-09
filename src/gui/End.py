import pygame
import spritesheet

from pygame.locals import *
from pygame.font import *


class endMenu:
    def __init__(self, Ventana, Clock, Gui):
        self.Ventana = Ventana
        self.Clock = Clock
        self.Gui = Gui

        self.Ganador = -1

        self.running = True

        self.x = Ventana.get_size()[0]
        self.y = Ventana.get_size()[1]

        #Imagenes de fin de juego
        self.ImgGanaRoja = pygame.image.load("../img/GanaR1068.png")
        self.RectR = self.ImgGanaRoja.get_rect()
        self.RectR.x = (self.x - self.RectR.width) / 2
        self.RectR.y = 0

        self.ImgGanaNegra = pygame.image.load("../img/GanaN1068.png")
        self.RectN = self.ImgGanaNegra.get_rect()
        self.RectN.x = (self.x - self.RectN.width) / 2
        self.RectN.y = 0

        self.ImgEmpate = pygame.image.load("../img/Empate1068.png")
        self.RectE = self.ImgEmpate.get_rect()
        self.RectE.x = (self.x - self.RectE.width) / 2
        self.RectE.y = 0

        self.FondoFinal = pygame.image.load("../img/Final1068.png").convert()

        self.BtnFinJuegoSheet = spritesheet.spritesheet("../img/SalirFinal.png")
        self.BtnFinJuegoImages = self.BtnFinJuegoSheet.load_strip((0, 0, 202, 202), 2)
        self.BtnFinJuego = self.BtnFinJuegoImages[0]
        self.RectFin = self.BtnFinJuego.get_rect()
        self.RectFin.x = self.x / 2 + 15
        self.RectFin.y = self.y - 210

        self.BtnNuevoJuegoSheet = spritesheet.spritesheet("../img/PlayFinal.png")
        self.BtnNuevoJuegoImages = self.BtnNuevoJuegoSheet.load_strip((0, 0, 202, 202), 2)
        self.BtnNuevoJuego = self.BtnNuevoJuegoImages[0]
        self.RectNuevo = self.BtnNuevoJuego.get_rect()
        self.RectNuevo.x = self.x / 2 - 217
        self.RectNuevo.y = self.y - 210

    def DibujarFondo(self):
        pass

    def DibujarGanador(self):
        self.Ventana.blit(pygame.transform.smoothscale(self.FondoFinal, (self.x, self.y)), (0, 0))

        if self.Ganador == 2:
            self.Ventana.blit(self.ImgGanaNegra, (self.RectN.x, self.RectN.y))
        elif self.Ganador == 1:
            self.Ventana.blit(self.ImgGanaRoja, (self.RectR.x, self.RectR.y))
        elif self.Ganador == 3:
            self.Ventana.blit(self.ImgEmpate, (self.RectE.x, self.RectE.y))

        self.Ventana.blit(self.BtnFinJuego, (self.RectFin.x, self.RectFin.y))
        self.Ventana.blit(self.BtnNuevoJuego, (self.RectNuevo.x, self.RectNuevo.y))

    def setGanador(self, G):
        if G == "Rojas":
            self.Ganador = 1
        elif G == "Negras":
            self.Ganador = 2
        else:
            self.Ganador = 3

    def on_render(self):
        self.DibujarGanador()
        pygame.display.flip()

    def on_event(self, event):
        #Si ya termino el juego habilito los botones de la pantalla de fin de juego
        if event.type == MOUSEBUTTONDOWN:
            if self.Ganador != -1:
                #print self.RectFin
                #print self.RectNuevo
                if self.RectFin.collidepoint(event.pos):
                    self.BtnFinJuego = self.BtnFinJuegoImages[1]
                    self.BtnFinJuego = self.BtnFinJuegoImages[0]
                    self.Gui.RenderThread.running = False
                    self.Gui.Escena.running = False
                    self.running = False
                elif self.RectNuevo.collidepoint(event.pos):
                    self.BtnNuevoJuego = self.BtnNuevoJuegoImages[1]
                    self.BtnNuevoJuego = self.BtnNuevoJuegoImages[0]
                    self.Gui.CambiarEscena(self.Gui.mainMenu)

    def on_execute(self):
        while(self.running):
            self.Clock.tick(30)
            for event in pygame.event.get():
                self.on_event(event)
