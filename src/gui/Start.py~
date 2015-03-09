from pygame import *
from pygame.locals import *
from pygame.font import *
import spritesheet


from Gui import *
from Juego import ReiniciarTablero


n = 0
e1 = 0
e2 = 0


class BotonMenu:

    def __init__(self, Imagen, Width, Height, x, y, Ventana):
        self.BtnSheet = spritesheet.spritesheet(Imagen)
        self.BtnImages = self.BtnSheet.load_strip((0, 0, Width, Height), 2)
        self.Btn = self.BtnImages[0]
        self.BtnRect = self.Btn.get_rect()
        self.BtnRect.x = x
        self.BtnRect.y = y
        self.Pulsado = False
        self.Ventana = Ventana

    def Pulsar(self):
        self.Btn = self.BtnImages[1]
        self.Pulsado = True

    def Soltar(self):
        self.Btn = self.BtnImages[0]
        self.Pulsado = False

    def Dibujar(self):
        #self.Ventana.blit(self.Btn + des_x, self.BtnRect+ des_y)
        (x, y) = (self.BtnRect.x, self.BtnRect.y)
        self.Ventana.blit(self.Btn, (x, y))


class MainMenu:

    def __init__(self, Ventana, Clock, Gui):
        self.Clock = Clock
        self.Ventana = Ventana
        self.Gui = Gui
        self.Equipo = None
        self.Dificultad = None

        self.running = True
        self.Error = 0
        self.Alpha = 255


        self.x = Ventana.get_size()[0] / 2
        self.y = Ventana.get_size()[1] / 2
#	self.x = 950
#       self.y = 750

        #Escalamos directamente el fondo
        self.Fondo = pygame.transform.smoothscale(pygame.image.load("../img/FondoPresentacion.png").convert(), (self.x * 2, self.y * 2))

        #Botones
        self.BtnDosJugadores = BotonMenu("../img/BMenu2JUGADORES.png", 202, 202, self.x - 449, self.y - 217, Ventana)
        self.BtnInterm = BotonMenu("../img/BMenuINTERMEDIO.png", 202, 202, self.x - 449, self.y + 15, Ventana)
        self.BtnInicial = BotonMenu("../img/BMenuINICIAL.png", 202, 202, self.x - 217, self.y - 217, Ventana)
        self.BtnExperto = BotonMenu("../img/BMenuEXPERTO.png", 202, 202, self.x - 217, self.y + 15, Ventana)
        self.BtnEquipoR = BotonMenu("../img/MenuRoja.png", 202, 202, self.x + 15, self.y - 217, Ventana)
        self.BtnEquipoN = BotonMenu("../img/MenuNegra.png", 202, 202, self.x + 15, self.y + 15, Ventana)
        self.BtnPlay = BotonMenu("../img/MenuPlay.png", 202, 202, self.x + 247, self.y - 217, Ventana)
        self.BtnSalir = BotonMenu("../img/MenuSalir.png", 202, 202, self.x + 247, self.y + 15, Ventana)

        self.BotonesNivel = {1: self.BtnInicial, 2: self.BtnInterm, 4: self.BtnExperto}

        #self.Fuente1 = Font("../font/Amazon Palafita.ttf", 200)

        #self.Titulo = self.Fuente1.render("CHECKERS", True, (190, 20, 50))
        #self.R = self.Titulo.get_rect()
        #self.R.x = self.x - self.R.width / 2
        #self.R.y = 55

        self.FuenteError = Font("../font/Ubuntu-Title.ttf", 50)

    def DibujarFondo(self):
        self.Ventana.blit(self.Fondo, (0, 0))

    def MostrarError(self):
        if self.Error == 1:
            E = self.FuenteError.render("Debe elegir un nivel antes de iniciar...", True, (92, 92, 92, self.Alpha))
            R = E.get_rect()
            R.x = self.x - R.width / 2
            R.y = self.y + 280

        if self.Error == 2:
            E = self.FuenteError.render("Debe elegir un equipo antes de iniciar...", True, (92, 92, 92, self.Alpha))
            R = E.get_rect()
            R.x = self.x - R.width / 2
            R.y = self.y + 280

        if self.Error != 0:
            self.Ventana.blit(E, R)

    #Funcionalidad de los botones

    def BotonDosJugadores(self):
        if self.BtnDosJugadores.Pulsado:
            self.BtnDosJugadores.Soltar()
        elif self.BtnInicial.Pulsado or self.BtnInterm.Pulsado or self.BtnExperto.Pulsado:
            self.BtnInterm.Soltar()
            self.BtnInicial.Soltar()
            self.BtnExperto.Soltar()
            self.BtnDosJugadores.Pulsar()
        else:
            self.BtnDosJugadores.Pulsar()

        self.BtnEquipoR.Soltar()
        self.BtnEquipoN.Soltar()

        self.Gui.tablero.PvP = True

    def BotonIntermedio(self):
        self.BtnDosJugadores.Soltar()
        if self.BtnInterm.Pulsado:
            self.BtnInterm.Soltar()
        elif self.BtnInicial.Pulsado or self.BtnExperto.Pulsado or self.BtnDosJugadores.Pulsado:
            self.BtnInicial.Soltar()
            self.BtnExperto.Soltar()
            self.BtnDosJugadores.Soltar()
            self.BtnInterm.Pulsar()
        else:
            self.BtnInterm.Pulsar()
        self.Gui.tablero.Nivel = 2
        self.Gui.tablero.PvP = False

    def BotonInicial(self):
        self.BtnDosJugadores.Soltar()
        if self.BtnInicial.Pulsado:
            self.BtnInicial.Soltar()
        elif self.BtnInterm.Pulsado or self.BtnExperto.Pulsado or self.BtnDosJugadores.Pulsado:
            self.BtnInterm.Soltar()
            self.BtnExperto.Soltar()
            self.BtnDosJugadores.Soltar()
            self.BtnInicial.Pulsar()
        else:
            self.BtnInicial.Pulsar()
        self.Gui.tablero.Nivel = 1
        self.Gui.tablero.PvP = False

    def BotonExperto(self):
        self.BtnDosJugadores.Soltar()
        if self.BtnExperto.Pulsado:
            self.BtnExperto.Soltar()
        elif self.BtnInicial.Pulsado or self.BtnInterm.Pulsado or self.BtnDosJugadores.Pulsado:
            self.BtnInterm.Soltar()
            self.BtnInicial.Soltar()
            self.BtnDosJugadores.Soltar()
            self.BtnExperto.Pulsar()
        else:
            self.BtnExperto.Pulsar()
        self.Gui.tablero.Nivel = 4
        self.Gui.tablero.PvP = False

    def BotonRojas(self):
        self.BtnDosJugadores.Soltar()
        if self.BtnEquipoR.Pulsado:
            self.BtnEquipoR.Soltar()
        elif self.BtnEquipoN.Pulsado:
            self.BtnEquipoN.Soltar()
            self.BtnEquipoR.Pulsar()
        else:
            self.BtnEquipoR.Pulsar()

    def BotonNegras(self):
        self.BtnDosJugadores.Soltar()
        if self.BtnEquipoN.Pulsado:
            self.BtnEquipoN.Soltar()
        elif self.BtnEquipoR.Pulsado:
            self.BtnEquipoR.Soltar()
            self.BtnEquipoN.Pulsar()
        else:
            self.BtnEquipoN.Pulsar()

    def BotonPlay(self):
        self.BtnPlay.Pulsar()
        self.Gui.tablero.StartTime = pygame.time.get_ticks()
        ReiniciarTablero()
        if self.BtnEquipoN.Pulsado:
            self.Gui.tablero.Inicializar(False)
        elif self.BtnEquipoR.Pulsado:
            self.Gui.tablero.Inicializar(True)
        else:
            self.Gui.tablero.Inicializar(None)

        if not self.BtnInicial.Pulsado and not self.BtnInterm.Pulsado and not self.BtnExperto.Pulsado and not self.BtnDosJugadores.Pulsado:
            self.Error = 1
            self.BtnPlay.Soltar()
        elif not self.BtnEquipoN.Pulsado and not self.BtnEquipoR.Pulsado and not self.BtnDosJugadores.Pulsado:
            self.Error = 2
            self.BtnPlay.Soltar()
        else:
            self.BotonesNivel[self.Gui.tablero.Nivel].Soltar()
            self.BtnEquipoN.Soltar()
            self.BtnEquipoR.Soltar()
            self.BtnPlay.Soltar()
            self.Gui.CambiarEscena(self.Gui.tablero)

    def BotonSalir(self):
        self.BtnSalir.Pulsar()
        self.Gui.RenderThread.running = False
        self.Gui.Escena.running = False
        self.running = False

    def on_render(self):
        self.Ventana.blit(pygame.transform.smoothscale(self.Fondo, (self.x * 2, self.y * 2)), (0, 0))
        #self.Ventana.blit(self.Titulo, (self.R.x, self.R.y))
        self.BtnEquipoR.Dibujar()
        self.BtnEquipoN.Dibujar()
        self.BtnInterm.Dibujar()
        self.BtnExperto.Dibujar()
        self.BtnInicial.Dibujar()
        self.BtnPlay.Dibujar()
        self.BtnSalir.Dibujar()
        self.BtnDosJugadores.Dibujar()
        self.MostrarError()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.BtnDosJugadores.BtnRect.collidepoint(event.pos):
                self.BotonDosJugadores()

            elif self.BtnInterm.BtnRect.collidepoint(event.pos):
                self.BotonIntermedio()

            elif self.BtnInicial.BtnRect.collidepoint(event.pos):
                self.BotonInicial()

            elif self.BtnExperto.BtnRect.collidepoint(event.pos):
                    self.BotonExperto()

            elif self.BtnEquipoR.BtnRect.collidepoint(event.pos):
                self.BotonRojas()

            elif self.BtnEquipoN.BtnRect.collidepoint(event.pos):
                self.BotonNegras()

            elif self.BtnPlay.BtnRect.collidepoint(event.pos):
                self.BotonPlay()

            elif self.BtnSalir.BtnRect.collidepoint(event.pos):
                self.BotonSalir()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while(self.running):
            self.Clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
