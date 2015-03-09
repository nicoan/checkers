import random
#import time
#import sys

from AuxMM import *
from Heuristicas import AppHeuristica

Heuristica = AppHeuristica(1)

NodoRecorridos = 0
Jugada = 0

# =================================================================================
#                                       Minimax
# =================================================================================


def EstadoTerminal(Nodo):
    ContBlanco = 0
    ContNegro = 0

    i = 0

    while i < 32:
        if Nodo.Tablero.Tablero[i] == FICHABLANCA or Nodo.Tablero.Tablero[i] == FICHABLANCAC:
            ContBlanco += 1
        elif Nodo.Tablero.Tablero[i] == FICHANEGRA or Nodo.Tablero.Tablero[i] == FICHANEGRAC:
            ContNegro += 1
        i += 1
    if Nodo.Tablero.Tablas == 20:
        return True
    if ContBlanco == 0 or ContNegro == 0:
        return True
    else:
        return False


#Funcion que nos calcula la jugada con la poda Alfa-Beta de MiniMax
#Nodo           -> El estado del juego en ese momento
#Nivel          -> El nivel de profundidad del arbol en ese momento
#Alfa           -> Valor Alfa
#Beta           -> Valor Beta
#Equipo         -> Para quien calculamos las jugadas en ese nivel
#JugadorMaquina -> Para que color devolvemos el puntaje de la heuristica
#NivelMax       -> Nivel de profundidad maximo

def AlfaBeta(Nodo, Nivel, Alfa, Beta, Equipo, JugadorMaquina, Lista):
    global NodoRecorridos
    NodoRecorridos += 1
    if EstadoTerminal(Nodo) or Nivel == 1:
        return Heuristica.FuncionEvaluadora(Nodo.Tablero, JugadorMaquina)
    else:
        #Generamos todos los movimientos posibles
        ListaMovimientos = GenerarMovimientos(Nodo.Tablero, Equipo)

        #Si no tenemos hijos para la siguiente jugada, entonces devolvemos el puntaje
        #del tablero en donde estamos.
        if ListaMovimientos == []:
            return Heuristica.FuncionEvaluadora(Nodo.Tablero, JugadorMaquina)
        #El que maximiza
        if Equipo == JugadorMaquina:
            for NodoHijo in ListaMovimientos:
                Alfa = max(Alfa, AlfaBeta(NodoHijo, Nivel - 1, Alfa, Beta, not Equipo, JugadorMaquina, Lista + [Nodo]))
                if Beta <= Alfa:
                    break
            return Alfa
        #El que minimiza
        else:
            for NodoHijo in ListaMovimientos:
                Beta = min(Beta, AlfaBeta(NodoHijo, Nivel - 1, Alfa, Beta, not Equipo, JugadorMaquina, Lista + [Nodo]))
                if Beta <= Alfa:
                    break
            return Beta


#Ejecucion de la poda AlfaBeta, Nos retorna las jugadas con sus puntajes
def MiniMaxAB(Tablero, Equipo, NivelMax):
    #Calculamos cual movimiento es mejor con AlfaBeta
    Movs = [(Mov, AlfaBeta(Mov, NivelMax, -8000, 8000, not Equipo, Equipo, list())) for Mov in GenerarMovimientos(Tablero, Equipo)]

    #Ordenamos de forma aleatoria los elementos (para que se elija de forma random las jugadas
    #con mejor puntaje)
    random.shuffle(Movs)

    #Ordenamos de manera que las mejores jugadas esten a lo ultimo
    Movs.sort(key=lambda (move, winner): winner)

    global Jugada
    Jugada += 1
    global NodoRecorridos

    NodoRecorridos = 0

    return Movs


def ElegirHeuristica(n):
    global Heuristica
    assert(n < 4 and n > 0)
    Heuristica = AppHeuristica(n)
