import sys
import spritesheet
import copy

import pygame
from pygame.locals import *
from pygame.font import *

sys.path.append("./engine")
from TableroMM import *
sys.path.append("./engine/minimax")
import MiniMax


#FPS a los que corre el juego
FPS = 30

#Tablero correspondiente al motor de las damas
Tab = None

#Bandera que utilizamos para la animacion de movimiento de las fichas, si MoviendoFicha es True, entonces
#una ficha se esta trasladando en el tablero. Hasta que dicha ficha no se detenga, deshabilitamos todos
#los controles.
MoviendoFicha = False

#Lista de fichas que fueron comidas, las cuales tenemos que retirar del tablero luego de que la ficha
#que comio detenga su movimiento.
VictimaF = []

#Una lista con los movimientos que devuelve el algoritmo MiniMax, los cuales se efectuan en el tablero.
ColaMovimientos = []

#Variable que nos indica que ficha dibujar primero y que ficha dibujar despues, para que, cuando se comen
#entre si, la que come pase por encima de la otra
DibujaPrimero = False


def SetTab(Tablero):
    #Elegimos que heuristica queremos usar
    MiniMax.ElegirHeuristica(1)


def ReiniciarTablero():
    global Tab
    Tab = TableroB("11111111111100000000222222222222")


class FichaGrafica(pygame.sprite.Sprite):

    def __init__(self, Ficha, Ventana, (Tabx, Taby)):
        pygame.sprite.Sprite.__init__(self)
        if Tab.Tablero[Ficha] == FICHANEGRA:
            self.sheet = spritesheet.spritesheet("../img/fichas96N.png")
            self.Color = True
        else:
            self.sheet = spritesheet.spritesheet("../img/fichas96R.png")
            self.Color = False

        #self.images = self.sheet.load_strip((0, 0, 96, 96), 8)
        self.images = self.sheet.load_strip((0, 0, 60, 60), 8)
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.Seleccionada = False

        self.Ventana = Ventana

        self.x = Ventana.get_size()[0] / 2
        self.y = Ventana.get_size()[1] / 2

        self.Tabx = Tabx
        self.Taby = Taby

        self.Ficha = Ficha
        self.Corona = False
        self.Movi = False
        self.Comi = False

        #Control de movimiento
        self.Moviendo = False
        self.Destino = (0, 0)
        self.Sentido = (1, 1)

        self.fps = 45
        self._delay = 1000 / self.fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

        #Posicionamos la ficha en el tablero
        (x, y) = ArrayToPos(self.Ficha)
        #self.rect.x = 96 * x + Tabx + 56
        #self.rect.y = 96 * y + Taby + 56
        self.rect.x = 60 * x + Tabx + 235
        self.rect.y = 60 * y + Taby + 134

    def draw(self, Ventana):
        Ventana.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, t):
        #Updateamos cada 30 fps...
        if t - self._last_update > self._delay:

            #Vamos moviendo la ficha hasta que llegue a destino...
            if self.Moviendo:
                if (self.rect.x, self.rect.y) != self.Destino:
                    self.rect.x += 12 * self.Sentido[0]
                    self.rect.y += 12 * self.Sentido[1]
                else:
                    self.Moviendo = False

                    global MoviendoFicha
                    MoviendoFicha = False

                    z = (self.rect.y - self.Taby - 134) / 60

                    if z == 0 and self.Color:
                        self.image = self.images[7]
                        self.Corona = True
                    elif z == 7 and not self.Color:
                        self.image = self.images[7]
                        self.Corona = True

            self._last_update = t

    #Metodo que cambia la imagen de la ficha a seleccionada/no seleccionada
    def Seleccionar(self):
        if self.Seleccionada:
            self.Seleccionada = False
            if self.Corona:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
        else:
            self.Seleccionada = True

            if self.Corona:
                self.image = self.images[3]
            else:
                self.image = self.images[2]

    def ResaltarOn(self):
        if self.Corona:
            self.image = self.images[5]
        else:
            self.image = self.images[4]

    def ResaltarOff(self):
        if self.Corona:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def MarcarUltimaOn(self):
        if self.Corona:
            self.image = self.images[7]
        else:
            self.image = self.images[6]

    def MarcarUltimaOff(self):
        if self.Corona:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def Mover(self, x, y):
        #Cuanto avanzo en la diagonal
        (p, q) = ArrayToPos(self.Ficha)
        (j, k) = (x - p, y - q)
        if j != 0 and k != 0:
            #El sentido de X e Y (+1 o -1)
            self.Sentido = (j / abs(j), k / abs(k))
            posVictim = Tab.EfectuarMovimiento(self.Ficha, x, y)
            if posVictim >= 0 or posVictim == -2:
                #self.Destino = (96 * x + self.Tabx + 56, 96 * y + self.Taby + 56)
                self.Destino = (60 * x + self.Tabx + 235, 60 * y + self.Taby + 134)
                self.Ficha = PosToArray(x, y)
                self.Movi = True
                self.Moviendo = True
                global MoviendoFicha
                MoviendoFicha = True

                if posVictim >= 0:
                    self.Comi = False
                    global VictimaF
                    VictimaF.append(posVictim)

                    global Tab
                    ##Si teniamos varias fichas para comer y comemos con una, no nos pueden soplar la otra.
                    if self.Color:
                        Tab.ListaSoplosBlanca.LimpiarLista()
                    else:
                        Tab.ListaSoplosNegra.LimpiarLista()


class TableroGrafico(pygame.sprite.Sprite):

    def __init__(self, Ventana, Clock, Gui):
        #Ventana y reloj de pygame
        self.Ventana = Ventana
        self.Clock = Clock
        self.Gui = Gui

        #self.x = Ventana.get_size()[0] / 2
        #self.y = Ventana.get_size()[1] / 2
	self.x = 950
        self.y = 750

        self.running = True

        self.FondoEscalado = pygame.transform.smoothscale(pygame.image.load("../img/wall.jpg"), (self.x * 2, self.y * 2))
        self.YaDibujeFondo = False

        self.Tablero = pygame.image.load("../img/Tablero880.png").convert()
        self.RectTab = self.Tablero.get_rect()
        #self.Tabx = self.x - self.RectTab.width / 2
        #self.Taby = self.y - self.RectTab.height / 2

        self.Tabx = 0
        self.Taby = 0

        self.Pizarra = pygame.image.load("../img/comidas.png")
        self.RectPiz = self.Pizarra.get_rect()
        # 15 es la separacion entre el tablero y la pizarra
        #self.Pizx = self.Tabx + self.RectTab.width + 15
        #self.Pizy = self.Taby
        self.Pizx = 764
        self.Pizy = 100

        #self.SurfaceRend = self.FondoEscalado.subsurface(self.Pizx, self.Pizy + self.RectPiz.height + 19, 172, 300)
	self.SurfaceRend = self.Tablero.subsurface(self.Pizx, self.Pizy + self.RectPiz.height + 19, 10, 10)
        self.RectSurfR = self.SurfaceRend.get_rect()
	self.RectSurfR = self.RectTab 
        self.SurfRx = self.Pizx
        self.SurfRy = self.Pizy + self.RectPiz.height + 19

        self.Blancas = []
        self.Negras = []
        self.FichaSel = None
        #Las blancas son False y empiezan ellas
        self.Turno = False
        #Con quien juega la maquina
        self.TurnoMaquina = False
        self.Sople = False

        self.PvP = False

        #Nivel de juego que le pasamos al MiniMax...
        self.Nivel = 4

        #Grupos de sprites para fichas blancas y negras
        self.SpritesNegras = pygame.sprite.Group()
        self.SpritesBlancas = pygame.sprite.Group()

        #Nos dice si el jugador presiono el boton para soplar
        self.QuieroSoplar = False
        #Nos indica si el jugador ya soplo una vez
        self.YaSople = False

        #Los milisegundos que transcurrieron hasta empezar el juego
        self.StartTime = 0

        #Boton de menu
        self.BtnMenuSheet = spritesheet.spritesheet("../img/VolverMenu.png")
        self.BtnMenuImages = self.BtnMenuSheet.load_strip((0, 0, 130, 130), 2)
        self.BtnMenu = self.BtnMenuImages[0]
        self.BtnMenuRect = self.BtnMenu.get_rect()
        #self.BtnMenuRect.x = self.Pizx - 100 - self.RectTab.width - self.BtnMenuRect.width
        #self.BtnMenuRect.y = self.Taby + self.RectTab.height - self.BtnMenuRect.height
        self.BtnMenuRect.x = 36
        self.BtnMenuRect.y = 518

        #Boton de soplido
        self.BtnSoplarSheet = spritesheet.spritesheet("../img/botonS2.png")
        self.BtnSoplarImages = self.BtnSoplarSheet.load_strip((0, 0, 172, 30), 2)
        self.BtnSoplar = self.BtnSoplarImages[0]
        self.BtnSoplarRect = self.BtnSoplar.get_rect()
        self.BtnSoplarRect.x = self.Pizx
        self.BtnSoplarRect.y = self.Pizy + self.RectPiz.height + (self.SurfRy - (self.Pizy + self.RectPiz.height)) / 2

        #Texto...
        self.Fuente35 = Font("../font/MYRIADPRO-SEMIBOLD.OTF", 35)
        self.Fuente40 = Font("../font/Ubuntu-Title.ttf", 40)

        self.TextoTurno = self.Fuente35.render("Turno", True, (92, 64, 51))
        self.TextoTurnoRect = self.TextoTurno.get_rect()
        #self.TextoTurnoRect.x = 18
        #self.TextoTurnoRect.y = 92
        self.TextoTurnoRect.x = 809
        self.TextoTurnoRect.y = 560


        #Label tiempo
        self.TextoTiempo = self.Fuente40.render("Tiempo", True, (0, 0, 0, 0))
        self.TextoTiempoRect = self.TextoTiempo.get_rect()
        #self.TextoTiempoRect.x = self.SurfRx + self.RectSurfR.width / 2
        #self.TextoTiempoRect.y = self.SurfRy
        self.TextoTiempoRect.x = 0
        self.TextoTiempoRect.y = 0

        #Ultima resaltada
        self.UltimaResaltada = None

        #Variable que usamos para marcar la ultima pieza que movio la maquina
        self.UltimaMovidaMaquina = None
        self.UltimaMovidaComio = False

        #Hileras de fichas comidas
        self.FichasBlancasComidas = []
        self.FichasNegrasComidas = []
        for i in range(3):
            L = pygame.image.load("../img/HileraNegra.png").convert_alpha()
            Rect = L.get_rect()
            Rect.x = self.Pizx + 6
            Rect.y = i * 40 + self.Pizy + 7
            self.FichasNegrasComidas.append((L, Rect))

            L = pygame.image.load("../img/HileraRoja.png").convert_alpha()
            Rect = L.get_rect()
            Rect.x = self.Pizx + 6
            Rect.y = i * 40 + self.Pizy + 207
            self.FichasBlancasComidas.insert(0, (L, Rect))

        #Variable que utilizamos para calcular el tiempo desde la ultima vez que movio el usuario, para
        #pasar el turno
        self.TiempoDesdeMovida = 0
        self.PuedoPasarTurno = False

        #Bandera que nos indica si la maquina movio...
        self.MaquinaMovio = False

        #Bandera que nos indica que ya lanzo una jugada!
        self.YaLanceJugada = False

    def Inicializar(self, TurnoMaquina):
        #Grupos de sprites para fichas blancas y negras
        self.SpritesNegras.empty()
        self.SpritesBlancas.empty()

        self.Negras = []
        self.Blancas = []

        self.TurnoMaquina = TurnoMaquina
        self.Turno = False

        pos = 0
        for F in Tab.Tablero:
            if F == FICHANEGRA:
                FichaGN = FichaGrafica(pos, self.Ventana, (self.Tabx, self.Taby))
                self.Negras.append(FichaGN)
                self.SpritesNegras.add(FichaGN)

            elif F == FICHABLANCA:
                FichaGB = FichaGrafica(pos, self.Ventana, (self.Tabx, self.Taby))
                self.Blancas.append(FichaGB)
                self.SpritesBlancas.add(FichaGB)

            pos += 1

    def DibujarFondo(self):
        #self.Ventana.blit(self.FondoEscalado, (0, 0))
        self.Ventana.blit(self.Tablero, (0, 0))


    def SeleccionarFicha(self, posX, posY):

        for F in self.Blancas:
            if ArrayToPos(F.Ficha) == (posX, posY):
                return F

        for F in self.Negras:
            if ArrayToPos(F.Ficha) == (posX, posY):
                return F

        return None

    def BorrarFicha(self, FichaG):
        if FichaG.Color:
            self.Negras.remove(FichaG)
            self.SpritesNegras.remove(FichaG)
        else:
            self.Blancas.remove(FichaG)
            self.SpritesBlancas.remove(FichaG)

    #----------------------------------------------------------------
    #                      Metodos para dibujar
    #----------------------------------------------------------------

    def DibujarFichas(self):
        if DibujaPrimero:
            self.SpritesBlancas.draw(self.Ventana)
            self.SpritesNegras.draw(self.Ventana)
        else:
            self.SpritesNegras.draw(self.Ventana)
            self.SpritesBlancas.draw(self.Ventana)

    def DibujarTurno(self):
        if self.Turno:
            T = self.Fuente35.render("NEGRAS", True, (92, 64, 51))
        else:
            T = self.Fuente35.render("ROJAS", True, (92, 64, 51))

        R = T.get_rect()
        R.x = 849 - (R.width / 2)
        R.y = 590

        Cont = self.Fuente40.render(self.Contador(), True, (92, 64, 51))
        ContRect = Cont.get_rect()
        ContRect.x = 850 - (ContRect.width / 2)
        ContRect.y = 500

        self.Ventana.blit(T, R)
        self.Ventana.blit(Cont, ContRect)

        #if self.Turno:
        #    self.Ventana.blit(self.TurnoN, (self.RectTurno.x, self.RectTurno.y))
        #else:
        #    self.Ventana.blit(self.TurnoR, (self.RectTurno.x, self.RectTurno.y))

        #Cont = self.Fuente40.render(self.Contador(), True, (92, 64, 51))
        #ContRect = Cont.get_rect()
        #ContRect.x = self.SurfRx + (self.RectSurfR.width - ContRect.width) / 2
        #ContRect.y = self.SurfRy + 30

        #self.Ventana.blit(Cont, ContRect)

        #self.Ventana.blit(self.TextoTurno, (self.TextoTurnoRect.x, self.TextoTurnoRect.y))

    def DibujarHileras(self):
        #Fichas comidas
        FichasBlancasC = 12 - len(self.Blancas)
        FichasNegrasC = 12 - len(self.Negras)

        #Filas enteras que vamos a dibujar
        FilaBlanca = FichasBlancasC / 4
        FilaNegra = FichasNegrasC / 4

        #Filas completas que hay que dibujar
        for i in range(FichasBlancasC / 4):
            self.Ventana.blit((self.FichasBlancasComidas[i])[0].subsurface(0, 0, 160, 39), (self.FichasBlancasComidas[i])[1])
        if FilaBlanca != 3:
        #Dibujamos las fichas restantes de lafila que sigue
            self.Ventana.blit((self.FichasBlancasComidas[FilaBlanca])[0].subsurface(0, 0, (FichasBlancasC % 4) * 40, 39), (self.FichasBlancasComidas[FilaBlanca])[1])

        for i in range(FilaNegra):
            self.Ventana.blit((self.FichasNegrasComidas[i])[0].subsurface(0, 0, 160, 39), (self.FichasNegrasComidas[i])[1])

        if FilaNegra != 3:

            self.Ventana.blit((self.FichasNegrasComidas[FilaNegra])[0].subsurface(0, 0, (FichasNegrasC % 4) * 40, 39), (self.FichasNegrasComidas[FilaNegra])[1])

    #----------------------------------------------------------------
    #                      Metodos para updatear
    #----------------------------------------------------------------

    def on_render(self):
        if not self.YaDibujeFondo:
            self.DibujarFondo()
            self.YaDibujeFondo = True
        self.Ventana.blit(self.Pizarra, (self.Pizx, self.Pizy))
        self.Ventana.blit(self.Tablero, (self.Tabx, self.Taby))
        self.Ventana.blit(self.SurfaceRend, (self.SurfRx, self.SurfRy))
        self.DibujarTurno()
        self.DibujarHileras()
        self.DibujarFichas()
        self.Ventana.blit(self.BtnMenu, (self.BtnMenuRect.x, self.BtnMenuRect.y))
        self.Ventana.blit(self.BtnSoplar, (self.BtnSoplarRect.x, self.BtnSoplarRect.y))

        pygame.display.flip()

    def on_event(self, event):

        (x, y) = pygame.mouse.get_pos()
        #(col, fila) = ((x - self.Tabx - 56) / 96, (y - self.Taby - 56) / 96)
        (col, fila) = ((x - 235) / 60, (y - 134) / 60)

        if event.type == QUIT:
            self.Gui.RenderThread.running = False
            self.running = False

        elif event.type == MOUSEBUTTONDOWN:

            if self.BtnMenuRect.collidepoint(event.pos):
                self.Gui.CambiarEscena(self.Gui.mainMenu)

            if not MoviendoFicha:
                if self.BtnSoplarRect.collidepoint((x, y)):
                    if self.FichaSel is None and not self.Sople:
                        self.BtnSoplar = self.BtnSoplarImages[1]
                        self.QuieroSoplar = not self.QuieroSoplar

                else:
                    #Hacemos click sobre el tablero...
                    FichaOVacio = self.SeleccionarFicha(col, fila)

                    #Codigo para que soplemos nosotros...
                    if self.QuieroSoplar and FichaOVacio is not None and not self.YaSople:
                        if self.TurnoMaquina:
                            CandidatosListaSoplo = Tab.ListaSoplosBlanca.CandidatosSoplo(Tab)
                            ListaSoplo = Tab.ListaSoplosBlanca
                        else:
                            CandidatosListaSoplo = Tab.ListaSoplosNegra.CandidatosSoplo(Tab)
                            ListaSoplo = Tab.ListaSoplosNegra

                        for F in CandidatosListaSoplo:
                            if ArrayToPos(F) == (col, fila):
                                if not self.PvP:
                                    assert(FichaOVacio.Color == self.TurnoMaquina)
                                ListaSoplo.RemoverSoplido(FichaOVacio.Ficha)
                                Tab.Comer(FichaOVacio.Ficha)
                                self.BorrarFicha(FichaOVacio)
                                self.YaSople = True
                                break

                    if FichaOVacio is None:
                        if self.FichaSel is not None:
                            self.FichaSel.Mover(col, fila)
                            if self.FichaSel.Movi:
                                self.TiempoDesdeMovida = pygame.time.get_ticks()
                                self.PuedoPasarTurno = True
                    else:
                        #Nos aseguramos que este moviendo una ficha de su equipo
                        if FichaOVacio.Color == self.Turno:
                            if self.FichaSel is not None:
                                if not self.FichaSel.Movi:
                                    #Deselecciono la ultima ficha seleccionada
                                    self.FichaSel.Seleccionar()
                                    #Tomo la nueva ficha y la selecciono
                                    self.FichaSel = FichaOVacio
                                    if self.FichaSel is not None:
                                        self.FichaSel.Seleccionar()
                            else:
                                self.FichaSel = FichaOVacio
                                if self.FichaSel is not None:
                                    self.FichaSel.Seleccionar()
        elif event.type == MOUSEBUTTONUP:
            self.BtnSoplar = self.BtnSoplarImages[0]

        #Codigo para resaltar fichas en caso de querer soplar
        if self.QuieroSoplar:
            FichaAResaltar = self.SeleccionarFicha(col, fila)
            if FichaAResaltar != self.UltimaResaltada:
                #Nos fijamos que la ultima resaltada este y que ademas no sea la ficha
                #seleccionada para mover
                if self.UltimaResaltada is not None and not self.UltimaResaltada.Seleccionada:
                    self.UltimaResaltada.ResaltarOff()
                    if not self.PvP:
                        self.UltimaMovidaMaquina.MarcarUltimaOn()
                #Resaltamos la ficha que posiblemente soplemos (del equipo contario..)
                if FichaAResaltar is not None and FichaAResaltar.Color != self.Turno:
                    FichaAResaltar.ResaltarOn()
                self.UltimaResaltada = FichaAResaltar

    def PasarTurno(self):
        self.Sople = False
        #Deseleccionamos la ficha que movimos
        self.FichaSel.Seleccionar()
        self.FichaSel = None
        self.FinTurno(self.Turno)
        self.Turno = not self.Turno
        self.QuieroSoplar = False
        self.YaSople = False
        self.PuedoPasarTurno = False
        if self.PvP:
            global DibujaPrimero
            DibujaPrimero = not DibujaPrimero

    def ChequearFinJuego(self):
        if len(self.Blancas) == 0:
            self.Gui.endMenu.setGanador("Negras")
            self.Gui.CambiarEscena(self.Gui.endMenu)
        elif len(self.Negras) == 0:
            self.Gui.endMenu.setGanador("Rojas")
            self.Gui.CambiarEscena(self.Gui.endMenu)
        elif Tab.Tablas == 20:
            Tab.Tablas = 0
            self.Gui.endMenu.setGanador("Empate")
            self.Gui.CambiarEscena(self.Gui.endMenu)

    def on_loop(self):
        self.ChequearFinJuego()

        tick = pygame.time.get_ticks()

        if tick - self.TiempoDesdeMovida > 800 and self.PuedoPasarTurno:
            self.PasarTurno()

        if not MoviendoFicha:
            #Nos fijamos si hay alguien para borrar
            if VictimaF != []:
                global VictimaF
                for Vict in VictimaF:
                    (x, y) = ArrayToPos(Vict)
                    FichaABorrar = self.SeleccionarFicha(x, y)
                    self.BorrarFicha(FichaABorrar)
                    global VictimaF
                    VictimaF.remove(Vict)
                    self.TiempoDesdeMovida = pygame.time.get_ticks()
                    self.UltimaMovidaComio = True

            #Ejecutamos los movimientos que queremos hacer
            global ColaMovimientos
            if ColaMovimientos != []:

                (OrigX, OrigY) = ArrayToPos(ColaMovimientos[0])
                Ficha = self.SeleccionarFicha(OrigX, OrigY)

                #Marcamos la ultima que movemos para resaltarla...
                if self.UltimaMovidaMaquina is not None:
                    self.UltimaMovidaMaquina.MarcarUltimaOff()

                self.UltimaMovidaMaquina = Ficha
                self.UltimaMovidaMaquina.MarcarUltimaOn()

                (DestX, DestY) = ArrayToPos(ColaMovimientos[1])
                Ficha.Mover(DestX, DestY)
                ColaMovimientos.pop(0)
                ColaMovimientos.pop(0)
            #Si el turno es de la maquina y ya no se puede mover, paso el turno.
            if not MoviendoFicha and self.TurnoMaquina == self.Turno and ColaMovimientos == [] and self.MaquinaMovio:
                self.MaquinaMovio = False
                self.FinTurno(self.Turno)
                self.Turno = not self.Turno
                #Al pasar el turno digo que ya puedo lanzar una nueva jugada
                self.YaLanceJugada = False

                global DibujaPrimero
                DibujaPrimero = not self.TurnoMaquina

                #Vemos si le quedaron fichas por comer al finalizar el movimiento,
                #si le quedaron fichas por comer entonces debemos agregar la ficha
                #a la lista de soplidos
                SoplidosNuevos = Tab.FuturaVictima(self.UltimaMovidaMaquina.Ficha)
                if SoplidosNuevos != []:
                    if self.UltimaMovidaMaquina.Color and self.UltimaMovidaComio:
                        Tab.ListaSoplosBlanca.TurnoAnterior += SoplidosNuevos
                    else:
                        Tab.ListaSoplosNegra.TurnoAnterior += SoplidosNuevos
                self.UltimaMovidaComio = False

            #Si es mi turno y no muevo y no puedo pasar el turno (if de arriba), juego (soy la maquina)
            #Tambien prevengo de no ejecutar una jugada dos veces
            if self.TurnoMaquina == self.Turno and not self.YaLanceJugada and not self.PvP:
                self.Jugar(self.TurnoMaquina)

        self.SpritesBlancas.update(tick)
        self.SpritesNegras.update(tick)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while(self.running):
            self.Clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()

    def Jugar(self, Equipo):

        #Buscamos la mejor lista de movimientos
        MovTab = copy.deepcopy(Tab)
        Movida = MiniMax.MiniMaxAB(MovTab, Equipo, self.Nivel)

        #Chequeamos si no hay mas jugadas
        global Ganador
        if Movida == []:
            if Equipo:
                self.Gui.endMenu.setGanador("Rojas")
            else:
                self.Gui.endMenu.setGanador("Negras")
            self.Gui.CambiarEscena(self.Gui.endMenu)
        else:
            Movida = Movida.pop(len(Movida) - 1)[0]

            if Movida.FichaSoplar is not None:
                (x, y) = ArrayToPos(Movida.FichaSoplar)
                FichaASoplar = Tab.SeleccionarFicha(x, y)
                if self.TurnoMaquina:
                    Tab.ListaSoplosNegra.RemoverSoplido(FichaASoplar)
                else:
                    Tab.ListaSoplosBlanca.RemoverSoplido(FichaASoplar)
                Tab.Comer(PosToArray(x, y))
                self.BorrarFicha(self.SeleccionarFicha(x, y))

            global ColaMovimientos
            ColaMovimientos = Movida.ListaMov

            self.Sople = False

            self.MaquinaMovio = True

            global DibujaPrimero
            DibujaPrimero = self.TurnoMaquina

            self.YaLanceJugada = True

    def Contador(self):
        milisec = pygame.time.get_ticks() - self.StartTime
        hs = milisec / 3600000
        mins = (milisec - hs * 3600000) / 60000
        sec = (milisec - hs * 3600000 - mins * 60000) / 1000

        hs = str(hs)
        mins = str(mins)
        sec = str(sec)
        if len(hs) == 1:
            hs = "0" + hs
        if len(mins) == 1:
            mins = "0" + mins
        if len(sec) == 1:
            sec = "0" + sec
        return hs + ":" + mins + ":" + sec

    def FinTurno(self, Equipo):
        #Calculamos los posibles soplidos...

        Tab.PosiblesSoplidos()

        if Equipo:
            for F in self.Negras:
                F.Comi = False
                F.Movi = False
        else:
            for F in self.Blancas:
                F.Comi = False
                F.Movi = False