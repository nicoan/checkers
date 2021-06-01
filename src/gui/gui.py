import threading
from juego import TableroGrafico
from start import MainMenu
from end import EndMenu

# Necesitamos un lock para llamara a la rutina de dibujado, esto es por un problema con el threading
# la sdl y python
# http://archives.seul.org/pygame/users/Jun-2006/msg00017.html
LOCK = threading.Lock()

class RenderGame(threading.Thread):
    def __init__(self, escena):
        threading.Thread.__init__(self)
        self.escena = escena
        self.dibuja_fondo = True
        self.running = True

    def run(self):
        while True:
            if self.running:
                if self.dibuja_fondo:
                    self.escena.escena.dibujar_fondo()
                    self.dibuja_fondo = False
                LOCK.acquire()
                self.escena.on_render()
                LOCK.release()
            else:
                if not self.running:
                    break


class Gui(object):
    def __init__(self, ventana, clock):
        self.ventana = ventana
        self.clock = clock

        self.render_thread = RenderGame(self)

        self.main_menu = MainMenu(ventana, clock, self)
        self.end_menu = EndMenu(ventana, clock, self)
        self.tablero = TableroGrafico(ventana, clock, self)

        self.escena = self.main_menu

        self.render_thread.start()
        self.escena.on_execute()

    def cambiar_escena(self, escena):
        self.escena.running = False
        self.escena = escena
        self.render_thread.dibuja_fondo = True
        self.escena.running = True
        self.escena.on_execute()

    def on_render(self):
        self.escena.on_render()
