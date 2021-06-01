import pygame
from pygame import MOUSEBUTTONDOWN
import spritesheet

class EndMenu(object):
    def __init__(self, ventana, clock, gui):
        self.ventana = ventana
        self.clock = clock
        self.gui = gui

        self.ganador = -1

        self.running = True

        self.x = ventana.get_size()[0]
        self.y = ventana.get_size()[1]

        #Imagenes de fin de juego
        self.img_gana_roja = pygame.image.load("../img/GanaR1068.png")
        self.rect_r = self.img_gana_roja.get_rect()
        self.rect_r.x = (self.x - self.rect_r.width) / 2
        self.rect_r.y = 0

        self.img_gana_negra = pygame.image.load("../img/GanaN1068.png")
        self.rect_n = self.img_gana_negra.get_rect()
        self.rect_n.x = (self.x - self.rect_n.width) / 2
        self.rect_n.y = 0

        self.img_empate = pygame.image.load("../img/Empate1068.png")
        self.rect_e = self.img_empate.get_rect()
        self.rect_e.x = (self.x - self.rect_e.width) / 2
        self.rect_e.y = 0

        self.fondo_final = pygame.image.load("../img/Final1068.png").convert()

        self.btn_fin_juego_sheet = spritesheet.spritesheet("../img/SalirFinal.png")
        self.btn_fin_juego_images = self.btn_fin_juego_sheet.load_strip((0, 0, 202, 202), 2)
        self.btn_fin_juego = self.btn_fin_juego_images[0]
        self.rect_fin = self.btn_fin_juego.get_rect()
        self.rect_fin.x = self.x / 2 + 15
        self.rect_fin.y = self.y - 210

        self.btn_nuevo_juego_sheet = spritesheet.spritesheet("../img/PlayFinal.png")
        self.btn_nuevo_juego_images = self.btn_nuevo_juego_sheet.load_strip((0, 0, 202, 202), 2)
        self.btn_nuevo_juego = self.btn_nuevo_juego_images[0]
        self.rect_nuevo = self.btn_nuevo_juego.get_rect()
        self.rect_nuevo.x = self.x / 2 - 217
        self.rect_nuevo.y = self.y - 210

    def dibujar_fondo(self):
        pass

    def dibujar_ganador(self):
        self.ventana.blit(pygame.transform.smoothscale(self.fondo_final, (self.x, self.y)), (0, 0))

        if self.ganador == 2:
            self.ventana.blit(self.img_gana_negra, (self.rect_n.x, self.rect_n.y))
        elif self.ganador == 1:
            self.ventana.blit(self.img_gana_roja, (self.rect_r.x, self.rect_r.y))
        elif self.ganador == 3:
            self.ventana.blit(self.img_empate, (self.rect_e.x, self.rect_e.y))

        self.ventana.blit(self.btn_fin_juego, (self.rect_fin.x, self.rect_fin.y))
        self.ventana.blit(self.btn_nuevo_juego, (self.rect_nuevo.x, self.rect_nuevo.y))

    def set_ganador(self, ganador):
        if ganador == "Rojas":
            self.ganador = 1
        elif ganador == "Negras":
            self.ganador = 2
        else:
            self.ganador = 3

    def on_render(self):
        self.dibujar_ganador()
        pygame.display.flip()

    def on_event(self, event):
        #Si ya termino el juego habilito los botones de la pantalla de fin de juego
        if event.type == MOUSEBUTTONDOWN:
            if self.ganador != -1:
                if self.rect_fin.collidepoint(event.pos):
                    self.btn_fin_juego = self.btn_fin_juego_images[1]
                    self.btn_fin_juego = self.btn_fin_juego_images[0]
                    self.gui.render_thread.running = False
                    self.gui.escena.running = False
                    self.running = False
                elif self.rect_nuevo.collidepoint(event.pos):
                    self.btn_nuevo_juego = self.btn_nuevo_juego_images[1]
                    self.btn_nuevo_juego = self.btn_nuevo_juego_images[0]
                    self.gui.cambiar_escena(self.gui.main_menu)

    def on_execute(self):
        while self.running:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.on_event(event)
