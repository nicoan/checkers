import sys

sys.path.append("./engine")
from TableroMM import ArrayToPos

FICHABLANCA = ord('1')
FICHABLANCAC = ord('3')
FICHANEGRA = ord('2')
FICHANEGRAC = ord('4')
ESPACIOVACIO = ord('0')

#EQUIPOBLANCO = 0
#EQUIPONEGRO = 1

EQUIPOBLANCO = False
EQUIPONEGRO = True

# Clase abstracta para contener las diferentes Heuristicas

#Basado en el patron Strategy

#En strategy, esta seria la clase Contexto


class AppHeuristica:

    def __init__(self, n):
        if n == 2:
            self.Heuristica = Heuristica2()
        elif n == 3:
            self.Heuristica = Heuristica3()
        else:
            self.Heuristica = Heuristica1()

    def FuncionEvaluadora(self, Tab, Equipo):
        return self.Heuristica.FuncionEvaluadora(Tab, Equipo)


#En strategy, esta seria la clase Estrategia
class Heuristica:

    def __init__(self):
        pass

    def FuncionEvaluadora(self, Tab, Equipo):
        raise NotImplementedError("Metodo no implementado, clase abstracta.")


#Heuristica 1

# En esta heuristica solo consideramos la cantidad de fichas que quedan en el tablero, y, le damos
# mas importancia a las coronadas, ya que las mismas tienen mas valor por poder efectuar movimientos
# con mayor libertad.

class Heuristica1(Heuristica):

    def __init__(self):
        Heuristica.__init__(self)

    def FuncionEvaluadora(self, Tab, Equipo):
        PuntajeNegro = 0
        PuntajeBlanco = 0
        i = 0

        while i < 32:
            if Tab.Tablero[i] == FICHABLANCA:
                PuntajeBlanco += 3
            elif Tab.Tablero[i] == FICHANEGRA:
                PuntajeNegro += 3
            elif Tab.Tablero[i] == FICHABLANCAC:
                PuntajeBlanco += 10
            elif Tab.Tablero[i] == FICHANEGRAC:
                PuntajeNegro += 10
            i += 1

        if Equipo == EQUIPONEGRO:
            return  PuntajeNegro - PuntajeBlanco
        else:
            return PuntajeBlanco - PuntajeNegro


#Heuristica 2

# Esta heuristica sigue la idea de la heuristica 1 solo que agrega el hecho de que es mas conveniente
# ubicar las fichas de la mitad del tablero para adelante. Esto se ve reflejado en que a los casilleros
# superiores, le ponemos un mayor puntaje.

class Heuristica2(Heuristica):

    def __init__(self):
        Heuristica.__init__(self)

    def FuncionEvaluadora(self, Tab, Equipo):
        PuntajeNegro = 0
        PuntajeBlanco = 0
        i = 0

        while i < 32:
            if Tab.Tablero[i] == FICHABLANCA:
                PuntajeBlanco += 3 + self.PuntajeCasillero(ArrayToPos(i), EQUIPOBLANCO)
            elif Tab.Tablero[i] == FICHANEGRA:
                PuntajeNegro += 3 + self.PuntajeCasillero(ArrayToPos(i), EQUIPONEGRO)
            elif Tab.Tablero[i] == FICHABLANCAC:
                PuntajeBlanco += 20
            elif Tab.Tablero[i] == FICHANEGRAC:
                PuntajeNegro += 20
            i += 1

        if Equipo == EQUIPONEGRO:
            return  PuntajeNegro - PuntajeBlanco
        else:
            return PuntajeBlanco - PuntajeNegro

    def PuntajeCasillero(self, (x, y), Equipo):
        #Si somos negras..
        if Equipo == EQUIPONEGRO:
            if y < 4:
                return 7
            elif y == 7:
                return 10
            else:
                return 6
        else:
            if y > 4:
                return 7
            elif y == 0:
                return 10
            else:
                return 6

#Heuristica 3

# Esta heuristica sigue la idea de la heuristica 2 solo que en lugar de dividir el tablero a la mitad
# lo divide en distintas secciones, dandole mas importancias a las esquinas (que es, donde no me pueden
# comer).


class Heuristica3(Heuristica):

    def __init__(self):
        Heuristica.__init__(self)

    def FuncionEvaluadora(self, Tab, Equipo):
        PuntajeNegro = 0
        PuntajeBlanco = 0
        i = 0

        while i < 32:
            if Tab.Tablero[i] == FICHABLANCA:
                PuntajeBlanco += 3 + self.PuntajeCasillero(ArrayToPos(i))
            elif Tab.Tablero[i] == FICHANEGRA:
                PuntajeNegro += 3 + self.PuntajeCasillero(ArrayToPos(i))
            elif Tab.Tablero[i] == FICHABLANCAC:
                PuntajeBlanco += 20
            elif Tab.Tablero[i] == FICHANEGRAC:
                PuntajeNegro += 20
            i += 1

        if Equipo == EQUIPONEGRO:
            return  PuntajeNegro - PuntajeBlanco
        else:
            return PuntajeBlanco - PuntajeNegro

    def PuntajeCasillero(self, (x, y)):
            if y == 0 or y == 7:
                return 5
            elif x == 0 or x == 7:
                return 4
            elif (y == 1 or y == 6) and (x <= 6 or x >= 1):
                return 3
            elif (x == 1 or x == 6) and (y <= 6 or y >= 1):
                return 3
            elif (y == 2 or y == 5) and (x <= 5 or x >= 2):
                return 2
            elif (x == 2 or x == 5) and (y <= 5 or y >= 2):
                return 2
            else:
                return 1
