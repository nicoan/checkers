#============================================================================
#        Modulo que contiene funciones auxiliares para el MiniMax
#============================================================================
import copy
import sys

sys.path.append("./engine")
from TableroMM import *

EQUIPOBLANCO = 0
EQUIPONEGRO = 1

#Clase que representa los nodos de los arboles
#
#Tablero es el estado del juego que representa ese nodo
#ListaMov es la lista de movimientos que se van a efectuar
#FichaSoplar es la ficha que (posiblemente) se sople


class NodoB:
    def __init__(self, Tablero, ListaMov):
        self.Tablero = Tablero
        self.ListaMov = ListaMov
        self.FichaSoplar = None

    def __str__(self):
        return str(self.ListaMov) + "\n" + str(self.Tablero) + "\n" + str(self.FichaSoplar)


def MovFicha(Ficha, Tab, MovList, Comio):

    #Creamos una lista de movimientos vacia
    Movimientos = []

    #Obtenemos la posicion de la ficha
    (x, y) = ArrayToPos(Ficha)

    #Si la ficha no esta coronada..
    if Tab.Tablero[Ficha] < ord('3'):
        #Dependiendo el color, vemos si se mueve hacia arriba o hacia abajo la ficha
        if Tab.Tablero[Ficha] == FICHABLANCA:
            p = 1
        else:
            p = -1

        i = 1
        while i <= 2:
            j = 0
            while j < 2:
                i = i * (-1)

                #Si es un movimiento valido...
                Vict = Tab.MovValido(Ficha, x + i, y + abs(i) * p)
                if Vict != -1:

                    #Esto es para prevenir que, si comio, haga un movimiento que no sea otra
                    #comida.
                    #La condicion es que no suceda que haya comido y sea un movimiento que
                    #no sea para comer (es decir, un -2)
                    if not (Comio and Vict == -2):

                        #Hacemos una copia del tablero y de la ficha, para que ejecute dicho
                        #movimiento.
                        TableroTmp = copy.deepcopy(Tab)

                        #Hacemos el movimiento en el tablero copiado, y agregamos el movimiento
                        #a la lista de movimientos.
                        #Push pone los elementos al principio de la lista, por eso primero agregamos
                        #el destino y luego el origen.
                        TableroTmp.EfectuarMovimiento(Ficha, x + i, y + abs(i) * p)

                        #Luego de efectuar el movimiento calculamos los posibles soplidos
                        TableroTmp.PosiblesSoplidos()

                        NewMovList = [Ficha, PosToArray(x + i, y + abs(i) * p)]

                        #Creamos un nuevo nodo con el tablero modificado
                        #Si venimos sin movimientos de antes solamente creamos el nodo
                        #con los nuevos movimientos generados...
                        if MovList == []:
                            NodoTmp = NodoB(TableroTmp, NewMovList)
                        #Sino, copiamos la MovList y le appendemos los nuevos movimietos
                        else:
                            DuplMovList = copy.deepcopy(MovList)
                            DuplMovList = DuplMovList + NewMovList
                            NodoTmp = NodoB(TableroTmp, DuplMovList)
                            #Le ponemos el mismo nombre a las dos listas para pasarla mas adelante
                            #en el caso de que haya comido, pues si se da un caso de este if habria
                            #que pasarle NewMovList y si se el else habria que pasarle DuplMovList
                            #con este "hack" lo arreglamos de manera facil
                            NewMovList = DuplMovList

                        Movimientos.append(NodoTmp)

                        #i fue un movimiento valido y ademas comimos (MovValido devuelve un numero
                        #entre 0 y 31 y no solo -2 para indicar que fue valido pero no comimos),
                        #vemos si puede comer de nuevo
                        if Vict != -2:
                            #Si comimos tenemos que limpiar nuestra lista de soplidos
                            if p == 1:
                                TableroTmp.ListaSoplosBlanca.LimpiarLista()
                            else:
                                TableroTmp.ListaSoplosNegra.LimpiarLista()

                            NuevosMovs = MovFicha(PosToArray(x + i, y + abs(i) * p), TableroTmp, NewMovList, True)
                            Movimientos += NuevosMovs
                j += 1
            i += 1
    else:
        i = 1
        j = 1

        while i < 8:
            z = 0
            while z < 4:
                i = i * (-1)

                if z < 2:
                    j = abs(j) * (-1)
                else:
                    j = abs(j)

                #Si es un movimiento valido...
                Vict = Tab.MovValido(Ficha, x + i, y + j)
                if Vict != -1:
                    if not (Comio and Vict == -2):

                        TableroTmp = copy.deepcopy(Tab)
                        TableroTmp.EfectuarMovimiento(Ficha, x + i, y + j)

                        #Luego de efectuar el movimiento calculamos los posibles soplidos
                        TableroTmp.PosiblesSoplidos()

                        NewMovList = [Ficha, PosToArray(x + i, y + j)]

                        if MovList == []:
                            NodoTmp = NodoB(TableroTmp, NewMovList)
                        else:
                            DuplMovList = copy.deepcopy(MovList)
                            DuplMovList = DuplMovList + NewMovList
                            NodoTmp = NodoB(TableroTmp, DuplMovList)
                            NewMovList = DuplMovList

                        Movimientos.append(NodoTmp)

                        if Vict != -2:
                            NuevosMovs = MovFicha(PosToArray(x + i, y + j), TableroTmp, NewMovList, True)
                            Movimientos += (NuevosMovs)
                z += 1
            i = abs(i) + 1
            j = abs(j) + 1

    return Movimientos


def GenerarMovimientos(Tab, Equipo):

    if Equipo == EQUIPOBLANCO:
        Eq = FICHABLANCA
        EqC = FICHABLANCAC
        ListaSoplos = Tab.ListaSoplosBlanca.CandidatosSoplo(Tab)
    else:
        Eq = FICHANEGRA
        EqC = FICHANEGRAC
        ListaSoplos = Tab.ListaSoplosNegra.CandidatosSoplo(Tab)

    #Creamos una lista de movimientos vacia
    Movimientos = []

    if ListaSoplos != []:

        # Nos fijamos que la ficha que vaya a soplar exista, o no sea de su mismo equipo.
        # El hecho de que sea de su mismo equipo se puede dar porque una ficha contraria puede estar
        # marcada para que pueda ser soplada en proximos turnos, pero puede suceder dicha ficha, dos
        # turnos mas adelante (es decir cuando la pueden soplar) ya no este ahi, y, en cambio, haya
        # una ficha del mismo equipo de quien puede soplar.
        for aux in ListaSoplos:
            if Tab.Tablero[aux] == ESPACIOVACIO or Tab.Tablero[aux] == Eq or Tab.Tablero[aux] == EqC:
                ListaSoplos.remove(aux)

        i = 0
        while i < 32:
            if Tab.Tablero[i] == Eq or Tab.Tablero[i] == EqC:

                for aux in ListaSoplos:
                    #Ponemos la victima de la lista de soplidos
                    Vict = aux

                    #Por cada posible soplido, geneamos un tablero nuevo, en el cual se
                    #soplara la ficha vict, y luego se evaluaran los movimientos posibles.

                    TableroSoplo = copy.deepcopy(Tab)

                    #Quitamos la ficha que tenemos que soplar del tablero...
                    TableroSoplo.Comer(Vict)

                    #Sacamos de la lista la ficha que ya soplamos...
                    if Equipo == EQUIPOBLANCO:
                        TableroSoplo.ListaSoplosBlanca.RemoverSoplido(Vict)
                    else:
                        TableroSoplo.ListaSoplosNegra.RemoverSoplido(Vict)

                    #Genero nuevos movimientos sin la ficha que soplamos
                    MovsParticulares = MovFicha(i, TableroSoplo, [], False)

                    #Ponemos la ficha a soplar en cada nodo (el contenido de
                    #MovsParticulares son nodos de MiniMax)
                    for NodoTab in MovsParticulares:
                        NodoTab.FichaSoplar = Vict

                    #Concatenamos los nueovs movimientos..
                    Movimientos += MovsParticulares
            i += 1
    else:
        i = 0
        while i < 32:
            if Tab.Tablero[i] == Eq or Tab.Tablero[i] == EqC:
                MovsParticulares = MovFicha(i, Tab, [], False)
                Movimientos += MovsParticulares
            i += 1

    return Movimientos
