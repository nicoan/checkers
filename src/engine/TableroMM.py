FICHABLANCA = ord('1')
FICHABLANCAC = ord('3')
FICHANEGRA = ord('2')
FICHANEGRAC = ord('4')
ESPACIOVACIO = ord('0')

#=======================================================================
#                           Funciones auxiliares
#=======================================================================


def PosToArray(x, y):
    return (8 * y + x) / 2


def ArrayToPos(i):
    return ((i % 4) * 2 + (((i / 4) % 2) ^ 1), (i / 4))

# ======================================================================
#   Definicion y manejo de la estructura para manejar lista de soplidos
# ======================================================================


class ListaSoploB:

    def __init__(self):
        self.TurnoActual = []
        self.TurnoAnterior = []

    #Desplazamos las listas, cada lista contiene tuplas con (Ficha, Victima de ficha)
    #Las listas contiene solamente las fichas de un color
    def CargarNuevaLista(self, NuevaLista):
        self.TurnoAnterior = self.TurnoActual
        self.TurnoActual = NuevaLista

    def CandidatosSoplo(self, Tab):
        L = []
        for f in self.TurnoAnterior:
            (x, y) = ArrayToPos(f)
            if Tab.SeleccionarFicha(x, y) != ESPACIOVACIO:
                L.append(f)
        return L

    def RemoverSoplido(self, Ficha):
        for F in self.TurnoAnterior:
            if F == Ficha:
                self.TurnoAnterior.remove(F)
        for F in self.TurnoActual:
            if F == Ficha:
                self.TurnoActual.remove(F)

    def Debug(self, f1, f2):
        self.TurnoActual = [(f1, f2)]

    def LimpiarLista(self):
        self.TurnoAnterior = []
        self.TurnoActual = []

    def __str__(self):
        resStr = "Turno Anterior:\n"
        for F in self.TurnoAnterior:
            resStr += str(ArrayToPos(F)) + " "

        resStr += "\nTurno Actual:\n"
        for F in self.TurnoActual:
            resStr += str(ArrayToPos(F)) + " "

        return resStr


#Clase tablero
class TableroB:

    def __init__(self, Tab):
        #Lista de soplidos que puede hacer las blancas
        self.ListaSoplosBlanca = ListaSoploB()
        #Lista de soplidos que puede hacer las negras
        self.ListaSoplosNegra = ListaSoploB()
        self.Tablero = bytearray(Tab)
        self.Tablas = 0

    def __str__(self):
        FLAG = False
        ret = "     0   1   2   3   4   5   6   7\n"
        ret += "   ---------------------------------\n"
        for i in range(8):
            ret += str(i) + "  |"
            for j in range(8):
                if FLAG:
                    if self.SeleccionarFicha(j, i) == FICHABLANCA:
                        ret += " b |"
                    elif self.SeleccionarFicha(j, i) == FICHANEGRA:
                        ret += " n |"
                    elif self.SeleccionarFicha(j, i) == FICHABLANCAC:
                        ret += " B |"
                    elif self.SeleccionarFicha(j, i) == FICHANEGRAC:
                        ret += " N |"
                    else:
                        ret += "   |"
                else:
                    ret += "   |"
                FLAG = not FLAG
            FLAG = not FLAG
            ret += "\n   ---------------------------------\n"
        ret += str(self.Tablero) + "\n"
        ret += "Soplos Blancos\n" + str(self.ListaSoplosBlanca)
        ret += "\nSoplos Negra\n" + str(self.ListaSoplosNegra)

        return ret

     # Funcion que, dada una posicion (x, y) del tablero, nos devuelve
     # la ficha que se encuentra en dicho lugar.

    def SeleccionarFicha(self, x, y):
        return self.Tablero[PosToArray(x, y)]

    # ------------------------------------------------------
    #       Funciones para controlar los movimientos
    # ------------------------------------------------------

    # Esta funcion nos dice si un movimiento no coronado es valido o no
    # Solo es usada en MovValido()
    #
    # Argumentos:
    # Tablero -> El tablero de juego
    # Ficha   -> Posicion de la ficha en el arreglo de fichas que queremos mover (indice del arreglo)
    # PosX    -> Coordenada X hacia donde vamos
    # PosY    -> Coordenada Y hacia donde vamos
    # Retornos:
    # -1  -> Si el movimiento NO es valido.
    # -2 -> Si el movimiento ES valido, pero no se comio ninguna ficha en el transcurso.
    # n  -> Si el movimiento ES valido, y ademas se comio una ficha en la posicion n
    #        donde 0 <= n <= 31

    def MovComunValido(self, Ficha, PosX, PosY):

        #Chequeamos que NO nos vayamos del tablero.
        if PosX < 0 or PosX > 7 or PosY < 0 or PosY > 7:
            return -1

        #Chequeamos que a donde queremos ir no haya una ficha
        if (self.Tablero[PosToArray(PosX, PosY)] != ESPACIOVACIO):
            return -1

        #Dependiendo el color, vemos si se mueve hacia arriba o hacia abajo la ficha
        if (self.Tablero[Ficha] == FICHABLANCA):
            p = 1
        else:
            p = -1

        #Obtenemos la posicion de la ficha que queremos mover
        (x, y) = ArrayToPos(Ficha)

        if x == PosX or y == PosY:
            return -1

        #Obtenemos el sentido de X (Si se mueve a izquierda o a derecha)
        PosXSent = PosX - x
        PosXSent = PosXSent / abs(PosXSent)

        #Muevo sin comer
        if PosX == x + PosXSent and PosY == y + p:
            return -2
        #Muevo y como (o sea, me salto un casillero)
        elif PosX == x + 2 * PosXSent and PosY == y + 2 * p:
            #Si hay una victima y esta tiene distinto color...
            # El Tablero[Ficha] + 2 representa la reina del equipo que esta moviendo es decir,
            # si somos blancas (1) nuestra reina es 3, esto es para fijarnos que nuestra reina
            # no sea una victima, o en otras palabras, que no podamos comer nuestra reina.
            Victima = self.SeleccionarFicha(PosX - PosXSent, PosY - p)
            if Victima != ESPACIOVACIO and Victima != self.Tablero[Ficha] and Victima != self.Tablero[Ficha] + 2:
                return PosToArray(PosX - PosXSent, PosY - p)
        else:
            return -1
        return -1

    # Esta funcion nos dice si un movimiento coronado es valido o no
    # Solo es usada en MovValido()
    #
    # Argumentos:
    # Tablero -> El tablero de juego
    # Ficha   -> Posicion de la ficha en el arreglo de fichas que queremos mover (indice del arreglo)
    # PosX    -> Coordenada X hacia donde vamos
    # PosY    -> Coordenada Y hacia donde vamos
    # Retornos:
    # -1  -> Si el movimiento NO es valido.
    # -2 -> Si el movimiento ES valido, pero no se comio ninguna ficha en el transcurso.
    # n  -> Si el movimiento ES valido, y ademas se comio una ficha en la posicion n
    #        donde 0 <= n <= 31

    def MovCoronadoValido(self, Ficha, PosX, PosY):

        #Chequeamos que NO nos vayamos del tablero.
        if PosX < 0 or PosX > 7 or PosY < 0 or PosY > 7:
            return -1

        #Chequeamos que a donde queremos ir no haya una ficha
        if self.Tablero[PosToArray(PosX, PosY)] != ESPACIOVACIO:
            return -1

        #Chequeamos que lo que se quiera mover sea una reina
        if self.Tablero[Ficha] == FICHABLANCA or self.Tablero[Ficha] == FICHANEGRA:
            return -1

        #Obtenemos la posicion de la ficha que queremos mover
        (x, y) = ArrayToPos(Ficha)

        if x == PosX or y == PosY:
            return -1

        #Obtenemos el sentido de X (Si se mueve a izquierda o a derecha)
        PosXSent = PosX - x
        PosXSent = PosXSent / abs(PosXSent)

        #Obtenemos el sentido de Y (Si se mueve a izquierda o a derecha)
        PosYSent = PosY - y
        PosYSent = PosYSent / abs(PosYSent)

        #Si nos movemos los mismos casilleros tanto en x como en y, entonces nos movimos
        #por una diagonal valida (creo que este checkeo se puede sacar)
        if abs(PosX - x) == abs(PosY - y):
            #Para mover hasta la posicion deseada, debemos mirar si no hay alguna ficha
            #en el medio que nos impida el paso.
            #Empezamos el indice en 1 para no chequear nuestra posicion.

            for i in range(1, abs(PosX - x)):
                Victima = self.SeleccionarFicha(x + (i * PosXSent), y + (i * PosYSent))
                #Si el casillero esta ocupado y no es el penultimo al que tenemos que ir
                #entonces hay una ficha en el camino
                if Victima != ESPACIOVACIO and i != abs(PosX - x) - 1:
                    return -1
                #Si el casillero esta ocupado y es el penultimo al que tenemos que ir
                #entonces hay una ficha para comer en el camino
                elif Victima != ESPACIOVACIO and i == abs(PosX - x) - 1:
                    #Nos fijamos que se pueda comer, como en MovComunValido
                    if Victima != self.Tablero[Ficha] and Victima != self.Tablero[Ficha] - 2:
                        return PosToArray(x + (i * PosXSent), y + (i * PosYSent))
                    else:
                        return -1
            #Si pasamos el for es porque no habia ninguna ficha adelante, por lo tanto
            #es un movimiento valido
            return -2
        return -1

    # Esta funcion nos dice si un movimiento es valido o no
    #
    # Argumentos:
    # Tablero -> El tablero de juego
    # Ficha   -> Posicion de la ficha en el arreglo de fichas que queremos mover (indice del arreglo)
    # PosX    -> Coordenada X hacia donde vamos
    # PosY    -> Coordenada Y hacia donde vamos
    # Retornos:
    # -1  -> Si el movimiento NO es valido.
    # -2 -> Si el movimiento ES valido, pero no se comio ninguna ficha en el transcurso.
    # n  -> Si el movimiento ES valido, y ademas se comio una ficha en la posicion n
    #        donde 0 <= n <= 31

    def MovValido(self, Ficha, PosX, PosY):
        #Chequeamos que nos hayan pasado una ficha y no un espacio vacio
        if self.Tablero[Ficha] == ESPACIOVACIO:
            return -1

        #Nos fijamos si la ficha es coronada (3 o 4)
        if self.Tablero[Ficha] > ord('2'):
            return self.MovCoronadoValido(Ficha, PosX, PosY)
        else:
            return self.MovComunValido(Ficha, PosX, PosY)

    # Elimina una ficha del tablero
    def Comer(self, Ficha):
        self.Tablas = 0
        self.Tablero[Ficha] = ESPACIOVACIO

    # Movemos una ficha en el tablero
    # Argumentos:
    # Tablero -> El tablero de juego
    # Ficha   -> Posicion de la ficha en el arreglo de fichas que queremos mover (indice del arreglo)
    # PosX    -> Coordenada X hacia donde vamos
    # PosY    -> Coordenada Y hacia donde vamos

    def MoverFicha(self, Ficha, PosX, PosY):
        self.Tablas += 1
        if 0 <= PosToArray(PosX, PosY) and PosToArray(PosX, PosY) <= 3 and self.Tablero[Ficha] == FICHANEGRA:
            self.Tablero[PosToArray(PosX, PosY)] = FICHANEGRAC
        elif 28 <= PosToArray(PosX, PosY) and PosToArray(PosX, PosY) <= 31 and self.Tablero[Ficha] == FICHABLANCA:
            self.Tablero[PosToArray(PosX, PosY)] = FICHABLANCAC
        else:
            self.Tablero[PosToArray(PosX, PosY)] = self.Tablero[Ficha]
        self.Tablero[Ficha] = ESPACIOVACIO

    # Efectuamos los movimientos validos
    # Argumentos:
    # Tablero -> El tablero de juego
    # Ficha   -> Posicion de la ficha en el arreglo de fichas que queremos mover (indice del arreglo)
    # PosX    -> Coordenada X hacia donde vamos
    # PosY    -> Coordenada Y hacia donde vamos
    # Retornos:
    # -1  -> Si el movimiento NO es valido.
    # -2 -> Si el movimiento ES valido, pero no se comio ninguna ficha en el transcurso.
    # n  -> Si el movimiento ES valido, y ademas se comio una ficha en la posicion n
    #        donde 0 <= n <= 31
    #

    def EfectuarMovimiento(self, Ficha, PosX, PosY):
    #Si el movimiento retorna un numero mayor a 0, es porque comimos una ficha.
    #Dicha ficha esta guardada en la variable Victima, y es una posicion en el
    #arreglo de fichas Tablero.

        Victima = self.MovValido(Ficha, PosX, PosY)
        if Victima >= 0:
            #Comemos la ficha
            self.Comer(Victima)

            #Movemos la ficha hacia su posicion de destino
            self.MoverFicha(Ficha, PosX, PosY)

            #Retornamos a quien comimos
            return Victima

        #Si es -2 fue un movimiento valido sin comer
        elif Victima == -2:
            self.MoverFicha(Ficha, PosX, PosY)
            return Victima
        else:
            return Victima

    def FuturaVictima(self, Ficha):

        ListaVictimas = []

        #Obtenemos la posicion de la ficha
        (x, y) = ArrayToPos(Ficha)

        if self.Tablero[Ficha] < ord('3'):

            #Dependiendo el color, vemos si se mueve hacia arriba o hacia abajo la ficha
            if self.Tablero[Ficha] == FICHABLANCA:
                p = 1
            else:
                p = -1

            i = 2
            j = 0

            while j < 2:
                i = i * (-1)
                Vict = self.MovValido(Ficha, x + i, y + 2 * p)
                if Vict > -1:
                    ListaVictimas.append(Ficha)
                j += 1
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
                    Vict = self.MovValido(Ficha, x + i, y + j)
                    if Vict > -1:
                        ListaVictimas.append(Ficha)
                    z += 1
                i = abs(i) + 1
                j = abs(j) + 1

        return ListaVictimas

    def PosiblesSoplidos(self):
        i = 0

        NuevasVictimasBlancas = []
        NuevasVictimasNegras = []

        while i < 32:
            if self.Tablero[i] == FICHABLANCA or self.Tablero[i] == FICHABLANCAC:
                aux = self.FuturaVictima(i)
                NuevasVictimasBlancas += aux
            elif self.Tablero[i] == FICHANEGRA or self.Tablero[i] == FICHANEGRAC:
                aux = self.FuturaVictima(i)
                NuevasVictimasNegras += aux
            i += 1

        #self.ListaSoplosBlanca.CargarNuevaLista(NuevasVictimasBlancas)
        #self.ListaSoplosNegra.CargarNuevaLista(NuevasVictimasNegras)
        self.ListaSoplosBlanca.CargarNuevaLista(NuevasVictimasNegras)
        self.ListaSoplosNegra.CargarNuevaLista(NuevasVictimasBlancas)
