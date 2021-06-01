import copy
import pygame
from pygame.font import Font
import spritesheet

from engine.board import Tablero, array_to_pos, pos_to_array, FICHANEGRA, FICHABLANCA, FICHANEGRAC, FICHABLANCAC
from engine.bindings import minimax

# FPS a los que corre el juego
FPS = 30

# Tablero correspondiente al motor de las damas
TABLERO = None

# Bandera que utilizamos para la animacion de movimiento de las fichas, si MoviendoFicha es True,
# entonces # una ficha se esta trasladando en el tablero. Hasta que dicha ficha no se detenga,
# deshabilitamos todos los controles.
MOVIENDO_FICHA = False

# Lista de fichas que fueron comidas, las cuales tenemos que retirar del tablero luego de que la
# ficha que comio detenga su movimiento.
VICTIMA_F = []

# Una lista con los movimientos que devuelve el algoritmo MiniMax, los cuales se efectuan en el
# tablero.
COLA_MOVIMIENTOS = []

# Variable que nos indica que ficha dibujar primero y que ficha dibujar despues, para que, cuando
# se comen entre si, la que come pase por encima de la otra
DIBUJAR_PRIMERO = False


def reiniciar_tablero():
    global TABLERO
    TABLERO = Tablero("11111111111100000000222222222222")
    # TABLERO = Tablero("00000100000010021000004102002302")
    # TABLERO = Tablero("00000100000010021000004102022300")

class FichaGrafica(pygame.sprite.Sprite):
    def __init__(self, ficha, ventana, (tab_x, tab_y)):
        pygame.sprite.Sprite.__init__(self)
        tablero = TABLERO.obtener_representacion()
        if tablero[ficha] == FICHANEGRA or tablero[ficha] == FICHANEGRAC:
            self.sheet = spritesheet.spritesheet("../img/fichas96N.png")
            self.color = True
            self.corona = tablero[ficha] == FICHANEGRAC
        else:
            self.sheet = spritesheet.spritesheet("../img/fichas96R.png")
            self.color = False
            self.corona = tablero[ficha] == FICHABLANCAC

        self.images = self.sheet.load_strip((0, 0, 60, 60), 8)
        self.image = self.images[1] if self.corona else self.images[0]

        self.rect = self.image.get_rect()
        self.seleccionada = False

        self.ventana = ventana

        self.x = ventana.get_size()[0] / 2
        self.y = ventana.get_size()[1] / 2

        self.tab_x = tab_x
        self.tab_y = tab_y

        self.ficha = ficha
        self.movi = False
        self.comi = False

        # Control de movimiento
        self.moviendo = False
        self.destino = (0, 0)
        self.sentido = (1, 1)

        self.fps = 45
        self._delay = 1000 / self.fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

        # Posicionamos la ficha en el tablero
        (x, y) = array_to_pos(self.ficha)
        self.rect.x = 60 * x + tab_x + 235
        self.rect.y = 60 * y + tab_y + 134

    def draw(self, ventana):
        ventana.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, t):
        """Updateamos cada 30 fps..."""
        if t - self._last_update > self._delay:

            # Vamos moviendo la ficha hasta que llegue a destino...
            if self.moviendo:
                if (self.rect.x, self.rect.y) != self.destino:
                    self.rect.x += 12 * self.sentido[0]
                    self.rect.y += 12 * self.sentido[1]
                else:
                    self.moviendo = False

                    global MOVIENDO_FICHA
                    MOVIENDO_FICHA = False

                    z = (self.rect.y - self.tab_y - 134) / 60

                    if z == 0 and self.color:
                        self.image = self.images[7]
                        self.corona = True
                    elif z == 7 and not self.color:
                        self.image = self.images[7]
                        self.corona = True

            self._last_update = t

    # Metodo que cambia la imagen de la ficha a seleccionada/no seleccionada
    def seleccionar(self):
        if self.seleccionada:
            self.seleccionada = False
            if self.corona:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
        else:
            self.seleccionada = True

            if self.corona:
                self.image = self.images[3]
            else:
                self.image = self.images[2]

    def resaltar_on(self):
        if self.corona:
            self.image = self.images[5]
        else:
            self.image = self.images[4]

    def resaltar_off(self):
        if self.corona:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def marcar_ultima_on(self):
        if self.corona:
            self.image = self.images[7]
        else:
            self.image = self.images[6]

    def marcar_ultima_off(self):
        if self.corona:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def mover(self, x, y):
        # Cuanto avanzo en la diagonal
        (p, q) = array_to_pos(self.ficha)
        (j, k) = (x - p, y - q)
        if j != 0 and k != 0:
            # El sentido de X e Y (+1 o -1)
            self.sentido = (j / abs(j), k / abs(k))
            pos_victim = TABLERO.efectuar_movimiento(self.ficha, x, y)
            if pos_victim >= 0 or pos_victim == -2:
                self.destino = (60 * x + self.tab_x + 235,
                                60 * y + self.tab_y + 134)
                self.ficha = pos_to_array(x, y)
                self.movi = True
                self.moviendo = True
                global MOVIENDO_FICHA
                MOVIENDO_FICHA = True

                if pos_victim >= 0:
                    self.comi = False
                    global VICTIMA_F
                    VICTIMA_F.append(pos_victim)

class TableroGrafico(pygame.sprite.Sprite):
    def __init__(self, ventana, clock, gui):
        # Ventana y reloj de pygame
        self.ventana = ventana
        self.clock = clock
        self.gui = gui

        self.x = 950
        self.y = 750

        self.running = True
        self.ya_dibuje_fondo = False

        self.tablero = pygame.image.load("../img/Tablero880.png").convert()
        self.rect_tab = self.tablero.get_rect()

        self.tab_x = 0
        self.tab_y = 0

        self.pizarra = pygame.image.load("../img/comidas.png")
        self.rect_piz = self.pizarra.get_rect()
        # 15 es la separacion entre el tablero y la pizarra
        self.piz_x = 764
        self.piz_y = 100

        self.surface_rend = self.tablero.subsurface(
            self.piz_x, self.piz_y + self.rect_piz.height + 19, 10, 10)
        self.rect_surf_r = self.surface_rend.get_rect()
        self.rect_surf_r = self.rect_tab
        self.surf_rx = self.piz_x
        self.surf_ry = self.piz_y + self.rect_piz.height + 19

        self.blancas = []
        self.negras = []
        self.ficha_sel = None
        # Las blancas son False y empiezan ellas
        self.turno = False 
        # Con quien juega la maquina
        self.turno_maquina = False

        self.pvp = False

        # Nivel de juego que le pasamos al MiniMax...
        self.nivel = 4

        # Grupos de sprites para fichas blancas y negras
        self.sprites_negras = pygame.sprite.Group()
        self.sprites_blancas = pygame.sprite.Group()

        # Los milisegundos que transcurrieron hasta empezar el juego
        self.start_time = 0

        # Boton de menu
        self.btn_menu_sheet = spritesheet.spritesheet("../img/VolverMenu.png")
        self.btn_menu_images = self.btn_menu_sheet.load_strip((0, 0, 130, 130), 2)
        self.btn_menu = self.btn_menu_images[0]
        self.btn_menu_rect = self.btn_menu.get_rect()
        self.btn_menu_rect.x = 36
        self.btn_menu_rect.y = 518

        # Texto...
        self.fuente35 = Font("../font/MYRIADPRO-SEMIBOLD.OTF", 35)
        self.fuente40 = Font("../font/Ubuntu-Title.ttf", 40)

        self.texto_turno = self.fuente35.render("Turno", True, (92, 64, 51))
        self.texto_turno_rect = self.texto_turno.get_rect()
        self.texto_turno_rect.x = 809
        self.texto_turno_rect.y = 560

        # Label tiempo
        self.texto_tiempo = self.fuente40.render("Tiempo", True, (0, 0, 0, 0))
        self.texto_tiempo_rect = self.texto_tiempo.get_rect()
        self.texto_tiempo_rect.x = 0
        self.texto_tiempo_rect.y = 0

        # Ultima resaltada
        self.ultima_resaltada = None

        # Variable que usamos para marcar la ultima pieza que movio la maquina
        self.ultima_movida_maquina = None
        self.ultima_movida_comio = False

        # Hileras de fichas comidas
        self.fichas_blancas_comidas = []
        self.fichas_negras_comidas = []
        for i in range(3):
            l = pygame.image.load("../img/HileraNegra.png").convert_alpha()
            rect = l.get_rect()
            rect.x = self.piz_x + 6
            rect.y = i * 40 + self.piz_y + 7
            self.fichas_negras_comidas.append((l, rect))

            l = pygame.image.load("../img/HileraRoja.png").convert_alpha()
            rect = l.get_rect()
            rect.x = self.piz_x + 6
            rect.y = i * 40 + self.piz_y + 207
            self.fichas_blancas_comidas.insert(0, (l, rect))

        # Variable que utilizamos para calcular el tiempo desde la ultima vez que movio el usuario,
        # para pasar el turno
        self.tiempo_desde_movida = 0
        self.puedo_pasar_turno = False

        # Bandera que nos indica si la maquina movio...
        self.maquina_movio = False

        # Bandera que nos indica que ya lanzo una jugada!
        self.ya_lance_jugada = False

    def inicializar(self, turno_maquina):
        # Grupos de sprites para fichas blancas y negras
        self.sprites_negras.empty()
        self.sprites_blancas.empty()

        self.negras = []
        self.blancas = []

        self.turno_maquina = turno_maquina
        self.turno = False 

        pos = 0
        for f in TABLERO.obtener_representacion():
            if f == FICHANEGRA or f == FICHANEGRAC:
                ficha_gn = FichaGrafica(pos, self.ventana, (self.tab_x, self.tab_y))
                self.negras.append(ficha_gn)
                self.sprites_negras.add(ficha_gn)

            elif f == FICHABLANCA or f == FICHABLANCAC:
                ficha_gb = FichaGrafica(pos, self.ventana, (self.tab_x, self.tab_y))
                self.blancas.append(ficha_gb)
                self.sprites_blancas.add(ficha_gb)

            pos += 1

    def dibujar_fondo(self):
        self.ventana.blit(self.tablero, (0, 0))

    def seleccionar_ficha(self, pos_x, pos_y):
        for f in self.blancas:
            if array_to_pos(f.ficha) == (pos_x, pos_y):
                return f

        for f in self.negras:
            if array_to_pos(f.ficha) == (pos_x, pos_y):
                return f

        return None

    def borrar_ficha(self, ficha_g):
        if ficha_g.color:
            self.negras.remove(ficha_g)
            self.sprites_negras.remove(ficha_g)
        else:
            self.blancas.remove(ficha_g)
            self.sprites_blancas.remove(ficha_g)

    # ----------------------------------------------------------------
    #                      Metodos para dibujar
    # ----------------------------------------------------------------

    def dibujar_fichas(self):
        if DIBUJAR_PRIMERO:
            self.sprites_blancas.draw(self.ventana)
            self.sprites_negras.draw(self.ventana)
        else:
            self.sprites_negras.draw(self.ventana)
            self.sprites_blancas.draw(self.ventana)

    def dibujar_turno(self):
        if self.turno:
            t = self.fuente35.render("NEGRAS", True, (92, 64, 51))
        else:
            t = self.fuente35.render("ROJAS", True, (92, 64, 51))

        r = t.get_rect()
        r.x = 849 - (r.width / 2)
        r.y = 590

        cont = self.fuente40.render(self.contador(), True, (92, 64, 51))
        cont_rect = cont.get_rect()
        cont_rect.x = 850 - (cont_rect.width / 2)
        cont_rect.y = 500

        self.ventana.blit(t, r)
        self.ventana.blit(cont, cont_rect)

    def dibujar_hileras(self):
        # Fichas comidas
        fichas_blancas_c = 12 - len(self.blancas)
        fichas_negras_c = 12 - len(self.negras)

        # Filas enteras que vamos a dibujar
        fila_blanca = fichas_blancas_c / 4
        fila_negra = fichas_negras_c / 4

        # Filas completas que hay que dibujar
        for i in range(fichas_blancas_c / 4):
            self.ventana.blit((self.fichas_blancas_comidas[i])[0].subsurface(
                0, 0, 160, 39), (self.fichas_blancas_comidas[i])[1])
        if fila_blanca != 3:
            # Dibujamos las fichas restantes de lafila que sigue
            self.ventana.blit((self.fichas_blancas_comidas[fila_blanca])[0].subsurface(
                0, 0, (fichas_blancas_c % 4) * 40, 39), (self.fichas_blancas_comidas[fila_blanca])[1])

        for i in range(fila_negra):
            self.ventana.blit((self.fichas_negras_comidas[i])[0].subsurface(
                0, 0, 160, 39), (self.fichas_negras_comidas[i])[1])

        if fila_negra != 3:
            self.ventana.blit((self.fichas_negras_comidas[fila_negra])[0].subsurface(
                0, 0, (fichas_negras_c % 4) * 40, 39), (self.fichas_negras_comidas[fila_negra])[1])

    # ----------------------------------------------------------------
    #                      Metodos para updatear
    # ----------------------------------------------------------------

    def on_render(self):
        if not self.ya_dibuje_fondo:
            self.dibujar_fondo()
            self.ya_dibuje_fondo = True
        self.ventana.blit(self.pizarra, (self.piz_x, self.piz_y))
        self.ventana.blit(self.tablero, (self.tab_x, self.tab_y))
        self.ventana.blit(self.surface_rend, (self.surf_rx, self.surf_ry))
        self.dibujar_turno()
        self.dibujar_hileras()
        self.dibujar_fichas()
        self.ventana.blit(
            self.btn_menu, (self.btn_menu_rect.x, self.btn_menu_rect.y))

        pygame.display.flip()

    def on_event(self, event):

        (x, y) = pygame.mouse.get_pos()
        (col, fila) = ((x - 235) / 60, (y - 134) / 60)

        if event.type == pygame.QUIT:
            self.gui.render_thread.running = False
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_menu_rect.collidepoint(event.pos):
                self.gui.cambiar_escena(self.gui.main_menu)

            if not MOVIENDO_FICHA:
                # Hacemos click sobre el tablero...
                ficha_o_vacio = self.seleccionar_ficha(col, fila)

                if ficha_o_vacio is None:
                    if self.ficha_sel is not None:
                        self.ficha_sel.mover(col, fila)
                        if self.ficha_sel.movi:
                            self.tiempo_desde_movida = pygame.time.get_ticks()
                            self.puedo_pasar_turno = True
                else:
                    # Nos aseguramos que este moviendo una ficha de su equipo
                    if ficha_o_vacio.color == self.turno:
                        if self.ficha_sel is not None:
                            if not self.ficha_sel.movi:
                                # Deselecciono la ultima ficha seleccionada
                                self.ficha_sel.seleccionar()
                                # Tomo la nueva ficha y la selecciono
                                self.ficha_sel = ficha_o_vacio
                                if self.ficha_sel is not None:
                                    self.ficha_sel.seleccionar()
                        else:
                            self.ficha_sel = ficha_o_vacio
                            if self.ficha_sel is not None:
                                self.ficha_sel.seleccionar()

    def pasar_turno(self):
        # Deseleccionamos la ficha que movimos
        self.ficha_sel.seleccionar()
        self.ficha_sel = None
        self.fin_turno(self.turno)
        self.turno = not self.turno
        self.puedo_pasar_turno = False
        if self.pvp:
            global DIBUJAR_PRIMERO
            DIBUJAR_PRIMERO = not DIBUJAR_PRIMERO

    def chequear_fin_juego(self):
        if not self.blancas:
            self.gui.end_menu.set_ganador("Negras")
            self.gui.cambiar_escena(self.gui.end_menu)
        elif not self.negras:
            self.gui.end_menu.set_ganador("Rojas")
            self.gui.cambiar_escena(self.gui.end_menu)
        elif TABLERO.tablas == 20:
            TABLERO.tablas = 0
            self.gui.end_menu.set_ganador("Empate")
            self.gui.cambiar_escena(self.gui.end_menu)

    def on_loop(self):
        self.chequear_fin_juego()

        tick = pygame.time.get_ticks()

        if tick - self.tiempo_desde_movida > 800 and self.puedo_pasar_turno:
            self.pasar_turno()

        if not MOVIENDO_FICHA:
            # Nos fijamos si hay alguien para borrar
            if VICTIMA_F != []:
                global VICTIMA_F
                for vict in VICTIMA_F:
                    (x, y) = array_to_pos(vict)
                    ficha_a_borrar = self.seleccionar_ficha(x, y)
                    self.borrar_ficha(ficha_a_borrar)
                    global VICTIMA_F
                    VICTIMA_F.remove(vict)
                    self.tiempo_desde_movida = pygame.time.get_ticks()
                    self.ultima_movida_comio = True

            # Ejecutamos los movimientos que queremos hacer
            global COLA_MOVIMIENTOS
            if COLA_MOVIMIENTOS != []:
                # import pdb; pdb.set_trace()
                (orig_x, orig_y) = array_to_pos(COLA_MOVIMIENTOS[0])
                ficha = self.seleccionar_ficha(orig_x, orig_y)

                # Marcamos la ultima que movemos para resaltarla...
                if self.ultima_movida_maquina is not None:
                    self.ultima_movida_maquina.marcar_ultima_off()

                self.ultima_movida_maquina = ficha
                self.ultima_movida_maquina.marcar_ultima_on()

                (dest_x, dest_y) = array_to_pos(COLA_MOVIMIENTOS[1])
                ficha.mover(dest_x, dest_y)
                COLA_MOVIMIENTOS.pop(0)
                COLA_MOVIMIENTOS.pop(0)

            # Si el turno es de la maquina y ya no se puede mover, paso el turno.
            if not MOVIENDO_FICHA and self.turno_maquina == self.turno and \
                    COLA_MOVIMIENTOS == [] and self.maquina_movio:
                self.maquina_movio = False
                self.fin_turno(self.turno)
                self.turno = not self.turno
                # Al pasar el turno digo que ya puedo lanzar una nueva jugada
                self.ya_lance_jugada = False

                global DIBUJAR_PRIMERO
                DIBUJAR_PRIMERO = not self.turno_maquina
                self.ultima_movida_comio = False

            # Si es mi turno y no muevo y no puedo pasar el turno (if de arriba), juego
            # (soy la maquina). Tambien prevengo de no ejecutar una jugada dos veces
            if self.turno_maquina == self.turno and not self.ya_lance_jugada and not self.pvp:
                self.jugar(self.turno_maquina)

        self.sprites_blancas.update(tick)
        self.sprites_negras.update(tick)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()

    def jugar(self, equipo):
        # Buscamos la mejor lista de movimientos
        # mov_tab = copy.deepcopy(TABLERO)
        movida = minimax(TABLERO, equipo, self.nivel)

        # Chequeamos si no hay mas jugadas
        if not movida:
            if equipo:
                self.gui.end_menu.set_ganador("Rojas")
            else:
                self.gui.end_menu.set_ganador("Negras")
            self.gui.cambiar_escena(self.gui.end_menu)
        else:
            global COLA_MOVIMIENTOS
            COLA_MOVIMIENTOS = movida[0]

            self.maquina_movio = True

            global DIBUJAR_PRIMERO
            DIBUJAR_PRIMERO = self.turno_maquina

            self.ya_lance_jugada = True

    def contador(self):
        milisec = pygame.time.get_ticks() - self.start_time
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

    def fin_turno(self, equipo):
        if equipo:
            for f in self.negras:
                f.comi = False
                f.movi = False
        else:
            for f in self.blancas:
                f.comi = False
                f.movi = False
