import threading

from pygame.locals import *
from pygame.font import *
from pygame.display import *

from Juego import *
from Start import *
from End import *

#Necesitamos un lock para llamara a la rutina de dibujado, esto es por un problema con el threading
#la sdl y python
#http://archives.seul.org/pygame/users/Jun-2006/msg00017.html
Lock = threading.Lock()


class RenderGame(threading.Thread):
    def __init__(self, Escena):
        threading.Thread.__init__(self)
        self.Escena = Escena
        self.DibujaFondo = True
        self.running = True

    def run(self):
        while True:
            if self.running:
                if self.DibujaFondo:
                    self.Escena.Escena.DibujarFondo()
                    self.DibujaFondo = False
                Lock.acquire()
                self.Escena.on_render()
                Lock.release()
            else:
                if not self.running:
                    break


class Gui:
    def __init__(self, Ventana, Clock):
        self.Ventana = Ventana
        self.Clock = Clock

        self.RenderThread = RenderGame(self)

        self.mainMenu = MainMenu(Ventana, Clock, self)
        self.endMenu = endMenu(Ventana, Clock, self)
        self.tablero = TableroGrafico(Ventana, Clock, self)

        self.Escena = self.mainMenu

        self.RenderThread.start()
        self.Escena.on_execute()

    def CambiarEscena(self, Escena):
        self.Escena.running = False
        self.Escena = Escena
        self.RenderThread.DibujaFondo = True
        self.Escena.running = True
        self.Escena.on_execute()

    def on_render(self):
        self.Escena.on_render()
