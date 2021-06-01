from bindings import ENGINE 

FICHABLANCA = '1'
FICHABLANCAC = '3'
FICHANEGRA = '2'
FICHANEGRAC = '4'
ESPACIOVACIO = '0'

# =======================================================================
#                           Funciones auxiliares
# =======================================================================
def pos_to_array(x, y):
    return (8 * y + x) / 2


def array_to_pos(i):
    return (i % 4) * 2 + (((i / 4) % 2) ^ 1), (i / 4)


class Tablero(object):
    def __init__(self, representacion):
        self.c_board = ENGINE.board_from_representation(representacion)
        self.tablas = 0

    def obtener_representacion(self):
        return self.c_board.contents.representation

    def seleccionar_ficha(self, x, y):
        return ENGINE.select_piece(self.c_board, x, y)

    def mov_valido(self, ficha, x, y):
        return ENGINE.is_valid_movement(self.c_board, ficha, x, y)

    def comer(self, ficha):
        ENGINE.remove_piece(self.c_board, ficha)

    def efectuar_movimiento(self, ficha, x, y):
        return ENGINE.execute_piece_movement(self.c_board, ficha, x, y)
