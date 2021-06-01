import os
import ctypes
import random

# ==============================================================
# Representacion de las estructuras utilizadas en C, en Python
# ==============================================================

PATH = os.path.dirname(os.path.realpath(__file__))
ENGINE = ctypes.CDLL("%s/mm.so" % PATH)

# Estructura de listas genericas representadas en python
class CListNode(ctypes.Structure):
    pass

CListNode._fields_ = [
    ("data", ctypes.POINTER(ctypes.c_void_p)),
    ("next", ctypes.POINTER(CListNode)),
    ("prev", ctypes.POINTER(CListNode))
]

class CList(ctypes.Structure):
    _fields_ = [
        ("first", ctypes.POINTER(CListNode)),
        ("last", ctypes.POINTER(CListNode))
    ]

# Tablero
class CBoardPosition(ctypes.Structure):
    _fields_ = [
        ("position", ctypes.c_char)
    ]

class CTablero(ctypes.Structure):
    _fields_ = [
        ("representation", ctypes.c_char_p),
        ("can_jump_white_team", ctypes.c_char),
        ("can_jump_black_team", ctypes.c_char)
    ]


class CMMNodo(ctypes.Structure):
    _fields_ = [
        ("movements", ctypes.POINTER(CList)),
        ("board", ctypes.POINTER(CTablero)),
        ("score", ctypes.c_int)
    ]


# Le damos el tipo de los argumentos y el tipo de retorno de las funciones que
# vamos a utilizar de la libreria de C
ENGINE.board_from_representation.argtype = [ctypes.c_char_p]
ENGINE.board_from_representation.restype = ctypes.POINTER(CTablero)

ENGINE.minimax.argtype = [ctypes.POINTER(CTablero), ctypes.c_int, ctypes.c_int]
ENGINE.minimax.restype = ctypes.POINTER(CList)

ENGINE.select_piece.argtype = [ctypes.POINTER(CTablero), ctypes.c_int, ctypes.c_int]
ENGINE.select_piece.restype = ctypes.c_char

ENGINE.is_valid_movement.argtype = [ctypes.POINTER(CTablero), ctypes.c_int, ctypes.c_int, ctypes.c_int]
ENGINE.is_valid_movement.restype = ctypes.c_int

ENGINE.remove_piece.argtype = [ctypes.POINTER(CTablero), ctypes.c_int]

ENGINE.execute_piece_movement.argtype = [ctypes.POINTER(CTablero), ctypes.c_int, ctypes.c_int, ctypes.c_int]
ENGINE.execute_piece_movement.restype = ctypes.c_int

ENGINE.print_mm_node.argtype = [ctypes.POINTER(CMMNodo)]

def recorrer_movs(c_lista_mov):
    movs = []
    val = c_lista_mov.contents.first
    while bool(val):
        movs_int = ctypes.cast(
            val.contents.data, ctypes.POINTER(CBoardPosition))
        movs.append(ord(movs_int.contents.position))
        val = val.contents.next
    return movs

def minimax(tablero, equipo, nivel):
    result = []
    minimax_result = ENGINE.minimax(tablero.c_board, equipo, nivel)
    val = minimax_result.contents.first
    while bool(val):
        mmnod = ctypes.cast(val.contents.data, ctypes.POINTER(CMMNodo))
        movimientos = recorrer_movs(mmnod.contents.movements)
        result += [(movimientos, mmnod.contents.score)]
        val = val.contents.next

    ENGINE.free_list_f(minimax_result, ENGINE.free_mm_node)

    # Ordenamos la lista para que la mejor jugada este a lo ultimo
    result.sort(key=lambda (move, winner): winner)
    # Nos quedamos solo con los puntajes mas altos
    filtered_result = filter(lambda (move, winner): winner == result[-1][1], result)
    # Hacemos shuffle de los resultados para que elija cualquier movimiento con puntaje mas alto
    return filtered_result[random.randrange(0, len(filtered_result))]
