import pygame
from pygame.font import Font
import spritesheet as spritesheet
from juego import reiniciar_tablero, FPS

N = 0
E1 = 0
E2 = 0

class BotonMenu(object):
    def __init__(self, imagen, width, height, x, y, ventana):
        self.btn_sheet = spritesheet.spritesheet(imagen)
        self.btn_images = self.btn_sheet.load_strip((0, 0, width, height), 2)
        self.btn = self.btn_images[0]
        self.btn_rect = self.btn.get_rect()
        self.btn_rect.x = x
        self.btn_rect.y = y
        self.pulsado = False
        self.ventana = ventana

    def pulsar(self):
        self.btn = self.btn_images[1]
        self.pulsado = True

    def soltar(self):
        self.btn = self.btn_images[0]
        self.pulsado = False

    def dibujar(self):
        (x, y) = (self.btn_rect.x, self.btn_rect.y)
        self.ventana.blit(self.btn, (x, y))


class MainMenu(object):
    def __init__(self, ventana, clock, gui):
        self.clock = clock
        self.ventana = ventana
        self.gui = gui
        self.equipo = None
        self.dificultad = None

        self.running = True
        self.error = 0
        self.alpha = 255

        self.x = ventana.get_size()[0] / 2
        self.y = ventana.get_size()[1] / 2

        # Escalamos directamente el fondo
        self.fondo = pygame.transform.smoothscale(pygame.image.load(
            "../img/FondoPresentacion.png").convert(), (self.x * 2, self.y * 2))

        # Botones
        self.btn_dos_jugadores = BotonMenu(
            "../img/BMenu2JUGADORES.png", 202, 202, self.x - 449, self.y - 217, ventana)
        self.btn_interm = BotonMenu(
            "../img/BMenuINTERMEDIO.png", 202, 202, self.x - 449, self.y + 15, ventana)
        self.btn_inicial = BotonMenu(
            "../img/BMenuINICIAL.png", 202, 202, self.x - 217, self.y - 217, ventana)
        self.btn_experto = BotonMenu(
            "../img/BMenuEXPERTO.png", 202, 202, self.x - 217, self.y + 15, ventana)
        self.btn_equipo_r = BotonMenu(
            "../img/MenuRoja.png", 202, 202, self.x + 15, self.y - 217, ventana)
        self.btn_equipo_n = BotonMenu(
            "../img/MenuNegra.png", 202, 202, self.x + 15, self.y + 15, ventana)
        self.btn_play = BotonMenu(
            "../img/MenuPlay.png", 202, 202, self.x + 247, self.y - 217, ventana)
        self.btn_salir = BotonMenu(
            "../img/MenuSalir.png", 202, 202, self.x + 247, self.y + 15, ventana)

        self.botones_nivel = { 4: self.btn_inicial, 8: self.btn_interm, 12: self.btn_experto }

        self.fuente_error = Font("../font/Ubuntu-Title.ttf", 50)

    def dibujar_fondo(self):
        self.ventana.blit(self.fondo, (0, 0))

    def mostrar_error(self):
        if self.error == 1:
            e = self.fuente_error.render(
                "Debe elegir un nivel antes de iniciar...", True, (92, 92, 92, self.alpha))
            r = e.get_rect()
            r.x = self.x - r.width / 2
            r.y = self.y + 280

        if self.error == 2:
            e = self.fuente_error.render(
                "Debe elegir un equipo antes de iniciar...", True, (92, 92, 92, self.alpha))
            r = e.get_rect()
            r.x = self.x - r.width / 2
            r.y = self.y + 280

        if self.error != 0:
            self.ventana.blit(e, r)

    # Funcionalidad de los botones

    def boton_dos_jugadores(self):
        if self.btn_dos_jugadores.pulsado:
            self.btn_dos_jugadores.soltar()
        elif self.btn_inicial.pulsado or self.btn_interm.pulsado or self.btn_experto.pulsado:
            self.btn_interm.soltar()
            self.btn_inicial.soltar()
            self.btn_experto.soltar()
            self.btn_dos_jugadores.pulsar()
        else:
            self.btn_dos_jugadores.pulsar()

        self.btn_equipo_r.soltar()
        self.btn_equipo_n.soltar()

        self.gui.tablero.pvp = True

    def boton_intermedio(self):
        self.btn_dos_jugadores.soltar()
        if self.btn_interm.pulsado:
            self.btn_interm.soltar()
        elif self.btn_inicial.pulsado or self.btn_experto.pulsado or self.btn_dos_jugadores.pulsado:
            self.btn_inicial.soltar()
            self.btn_experto.soltar()
            self.btn_dos_jugadores.soltar()
            self.btn_interm.pulsar()
        else:
            self.btn_interm.pulsar()
        self.gui.tablero.nivel = 8
        self.gui.tablero.pvp = False

    def boton_inicial(self):
        self.btn_dos_jugadores.soltar()
        if self.btn_inicial.pulsado:
            self.btn_inicial.soltar()
        elif self.btn_interm.pulsado or self.btn_experto.pulsado or self.btn_dos_jugadores.pulsado:
            self.btn_interm.soltar()
            self.btn_experto.soltar()
            self.btn_dos_jugadores.soltar()
            self.btn_inicial.pulsar()
        else:
            self.btn_inicial.pulsar()
        self.gui.tablero.nivel = 4
        self.gui.tablero.pvp = False

    def boton_experto(self):
        self.btn_dos_jugadores.soltar()
        if self.btn_experto.pulsado:
            self.btn_experto.soltar()
        elif self.btn_inicial.pulsado or self.btn_interm.pulsado or self.btn_dos_jugadores.pulsado:
            self.btn_interm.soltar()
            self.btn_inicial.soltar()
            self.btn_dos_jugadores.soltar()
            self.btn_experto.pulsar()
        else:
            self.btn_experto.pulsar()
        self.gui.tablero.nivel = 12
        self.gui.tablero.pvp = False

    def boton_rojas(self):
        self.btn_dos_jugadores.soltar()
        if self.btn_equipo_r.pulsado:
            self.btn_equipo_r.soltar()
        elif self.btn_equipo_n.pulsado:
            self.btn_equipo_n.soltar()
            self.btn_equipo_r.pulsar()
        else:
            self.btn_equipo_r.pulsar()

    def boton_negras(self):
        self.btn_dos_jugadores.soltar()
        if self.btn_equipo_n.pulsado:
            self.btn_equipo_n.soltar()
        elif self.btn_equipo_r.pulsado:
            self.btn_equipo_r.soltar()
            self.btn_equipo_n.pulsar()
        else:
            self.btn_equipo_n.pulsar()

    def boton_play(self):
        self.btn_play.pulsar()
        self.gui.tablero.start_time = pygame.time.get_ticks()
        reiniciar_tablero()
        if self.btn_equipo_n.pulsado:
            self.gui.tablero.inicializar(False)
        elif self.btn_equipo_r.pulsado:
            self.gui.tablero.inicializar(True)
        else:
            self.gui.tablero.inicializar(None)

        if not self.btn_inicial.pulsado and not self.btn_interm.pulsado \
            and not self.btn_experto.pulsado and not self.btn_dos_jugadores.pulsado:
            self.error = 1
            self.btn_play.soltar()
        elif not self.btn_equipo_n.pulsado and not self.btn_equipo_r.pulsado and not self.btn_dos_jugadores.pulsado:
            self.error = 2
            self.btn_play.soltar()
        else:
            self.botones_nivel[self.gui.tablero.nivel].soltar()
            self.btn_equipo_n.soltar()
            self.btn_equipo_r.soltar()
            self.btn_play.soltar()
            self.gui.cambiar_escena(self.gui.tablero)

    def boton_salir(self):
        self.btn_salir.pulsar()
        self.gui.render_thread.running = False
        self.gui.escena.running = False
        self.running = False

    def on_render(self):
        self.ventana.blit(pygame.transform.smoothscale(
            self.fondo, (self.x * 2, self.y * 2)), (0, 0))
        self.btn_equipo_r.dibujar()
        self.btn_equipo_n.dibujar()
        self.btn_interm.dibujar()
        self.btn_experto.dibujar()
        self.btn_inicial.dibujar()
        self.btn_play.dibujar()
        self.btn_salir.dibujar()
        self.btn_dos_jugadores.dibujar()
        self.mostrar_error()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_dos_jugadores.btn_rect.collidepoint(event.pos):
                self.boton_dos_jugadores()

            elif self.btn_interm.btn_rect.collidepoint(event.pos):
                self.boton_intermedio()

            elif self.btn_inicial.btn_rect.collidepoint(event.pos):
                self.boton_inicial()

            elif self.btn_experto.btn_rect.collidepoint(event.pos):
                self.boton_experto()

            elif self.btn_equipo_r.btn_rect.collidepoint(event.pos):
                self.boton_rojas()

            elif self.btn_equipo_n.btn_rect.collidepoint(event.pos):
                self.boton_negras()

            elif self.btn_play.btn_rect.collidepoint(event.pos):
                self.boton_play()

            elif self.btn_salir.btn_rect.collidepoint(event.pos):
                self.boton_salir()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
