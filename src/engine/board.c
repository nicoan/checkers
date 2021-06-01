#include "list.c"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char PIECE_WHITE = '1';
const char PIECE_WHITE_CROWNED = '3';
const char PIECE_BLACK = '2';
const char PIECE_BLACK_CROWNED = '4';
const char WHITE_SPACE = '0';

const char TEAM_WHITE = 0;
const char TEAM_BLACK = 1;

// Estructura que representa un tablero
typedef struct board_ {
  char *representation;
  // Nos dice si hay al menos un movimiento de fichas blancas que puede comer
  char can_jump_white_team;
  // Nos dice si hay al menos un movimiento de fichas negras que puede comer
  char can_jump_black_team;
} Board;

void set_teams_can_jump(Board *board);

/* Funciones de arreglo */
int position_to_array(int x, int y) 
{
  return (8 * y + x) / 2;
}

// Devolvemos en la decena la posicion x y en la unidad la posicion y.
int array_to_position(int i) 
{
  return ((i % 4) * 2 + (((i / 4) % 2) ^ 1)) * 10 + (i / 4);
}

char get_x_from_position(int position) 
{
  return (position / 10);
}

char get_y_from_position(int position) 
{
  return (position % 10);
}

/*
 * Nos devuelve un tablero donde en cada lugar hay uno de los siguientes:
 * 0 -> Espacio vacio
 * 1 -> Blanca
 * 2 -> Negra
 * 3 -> Blanca Coronada
 * 4 -> Negra Coronada
 */
Board *board_from_representation(char *board_representation) 
{
  Board *new_board = (Board*) malloc(sizeof(Board));
  new_board->representation = (char*) malloc(sizeof(char) * 33);

  memcpy(new_board->representation, board_representation, sizeof(char) * 33);
  new_board->representation[32] = '\0';

  // Calculamos si algun equipo puede comer
  set_teams_can_jump(new_board);

  return new_board;
}

void free_board(Board *board) 
{
  free(board->representation);
  free(board);
}

Board *duplicate_board(Board *board) 
{
  Board *new_board = (Board*) malloc(sizeof(Board));
  new_board->representation = (char*) malloc(sizeof(char) * 33);

  // Copiamos las fichas
  memcpy(new_board->representation, board->representation, sizeof(char) * 33);
  new_board->representation[32] = '\0';

  // Copiamos si puede comer
  new_board->can_jump_white_team = board->can_jump_white_team;
  new_board->can_jump_black_team = board->can_jump_black_team;

  return new_board;
}

/*
 * Funcion que, dada una posicion (x, y) del tablero, nos devuelve
 * la ficha que se encuentra en dicho lugar.
 */
char select_piece(Board *board, int x, int y) 
{
  return board->representation[position_to_array(x, y)];
}

/* Elimina una ficha del tablero */
void remove_piece(Board *board, int piece) 
{
  board->representation[piece] = WHITE_SPACE;
}

void print_board(Board *board) 
{
  int i, j;
  char FLAG = 0;
  printf("Representacion: %s\n", board->representation);
  printf("     0   1   2   3   4   5   6   7\n");
  printf("   ┌───┬───┬───┬───┬───┬───┬───┬───┐\n");
  for (i = 0; i < 8; i++) {
    printf("%d  │", i);
    for (j = 0; j < 8; j++) {
      if (FLAG) {
        char ficha = select_piece(board, j, i);
        if (ficha == PIECE_WHITE)
            printf(" b │");
        else if (ficha == PIECE_BLACK)
            printf(" n │");
        else if (ficha == PIECE_WHITE_CROWNED)
            printf(" B │");
        else if (ficha == PIECE_BLACK_CROWNED)
            printf(" N │");
        else
            printf("   │");
      } else {
        printf("   │");
      }
      FLAG = FLAG ^ 1;
    }
    FLAG = FLAG ^ 1;
    if (i < 7)
      printf("\n   ├───┼───┼───┼───┼───┼───┼───┼───┤\n");
  }
  printf("\n   └───┴───┴───┴───┴───┴───┴───┴───┘\n");
  printf("Pueden comer las blancas: %d\n", board->can_jump_white_team);
  printf("Pueden comer las negras: %d\n", board->can_jump_black_team);
}

char is_my_team(char piece_color, int team)
{
  return team == TEAM_WHITE
    ? piece_color == PIECE_WHITE || piece_color == PIECE_WHITE_CROWNED
    : piece_color == PIECE_BLACK || piece_color == PIECE_BLACK_CROWNED;
}

int get_team(char piece_color) 
{
  if (piece_color == WHITE_SPACE) {
    return -1;
  }

  return piece_color == PIECE_WHITE || piece_color == PIECE_WHITE_CROWNED
    ? TEAM_WHITE
    : TEAM_BLACK;
}

int get_enemy_team(int team) 
{
  return team == TEAM_WHITE ? TEAM_BLACK : TEAM_WHITE;
}

int is_crowned(char piece_color) 
{
  return piece_color == PIECE_WHITE_CROWNED || piece_color == PIECE_BLACK_CROWNED;
}

char piece_can_jump_from(char *board, int team, int x, int y) 
{
  int y_direction = team == TEAM_WHITE ? 1 : -1;
  int x_direction = 1;

  for (int i = 0; i < 2; i++, x_direction = x_direction * -1) {
    // Primero nos fijamos que podemos comer dependiendo la coordenada vertical
    if (((team == TEAM_WHITE && y <= 5) || (team == TEAM_BLACK && y >= 2)) &&
        ((x_direction == 1 && x <= 5) || (x_direction == -1 && x >= 2))) {
      // Nos fijamos que:
      // - La ficha que esta una posicion mas arriba (o abajo) a la izquierda (o derecha) no sea de mi equipo
      // - La posicion dos lugares mas arriba (o abajo) y dos lugares mas a la izquierda (o derecha) este vacia
      char possible_victim = board[position_to_array(x + 1 * x_direction, y + 1 * y_direction )];
      char can_jump = possible_victim != WHITE_SPACE
        && !is_my_team(possible_victim, team)
        && board[position_to_array(x + 2 * x_direction, y + 2 * y_direction )] == WHITE_SPACE;

      if (can_jump) {
        return 1;
      }
    }
  }
  return 0;
}

char piece_crowned_can_jump_from(char *board, int team, int x, int y) 
{
  int x_direction = 1;
  int y_direction = 1;

  // Hacemos 4 iteraciones para las cuatro diagonales posibles
  int i = 0;
  while (i < 4) {
    int x_offset = 0;
    int y_offset = 0;
    // Chequeamos que estamos en posiciones validas para poder comer
    // En el caso de x:
    //   - Si estoy yendo hacia la derecha (xDirection = 1) y tengo al menos dos casilleros mas para poder comer
    //   - Si estoy yendo hacia la izquierda (xDirection = -1) y tengo al menos dos casilleros mas para poder comer.
    // En el caso de y:
    //   - Si estoy yendo hacia la abajo (yDirection = 1) y tengo al menos dos casilleros mas para poder comer
    //   - Si estoy yendo hacia la arriba (yDirection = -1) y tengo al menos dos casilleros mas para poder comer.
    while (((x_direction == 1 && x + x_offset <= 5) || (x_direction == -1 && x - x_offset >= 2))
        && ((y_direction == 1 && y + y_offset <= 5) || (y_direction == -1 && y - y_offset >= 2))) {
      // printf("Posible Victima: (%d, %d)\n", x + (1 + x_offset) * xDirection, y + (1 + y_offset) * yDirection);
      // printf("Espacio Vacio  : (%d, %d)\n", x + (2 + x_offset) * xDirection, y + (2 + y_offset) * yDirection);

      char possible_victim = board[position_to_array(x + (1 + x_offset) * x_direction, y + (1 + y_offset) * y_direction)];
      char where_do_i_fall = board[position_to_array(x + (2 + x_offset) * x_direction, y + (2 + y_offset) * y_direction)];

      // Este es el casillero en diagonal anterior a la victima que apuntamos. Tiene que ser un espacio vacio
      // si no lo es, tenemos dos fichas juntas pegadas y no podemos comer (siempre y cuando los offset sean
      // mayor a 0, porque si es 0 este casillero somos nosotros mismos)
      // Tambien puede pasar de tener en una misma diagonal dos fichas pegadas, un espacio y otra ficha, en
      // este caso TAMPOCO puede comer porque no se pueden saltar dos fichas juntas.
      char pre_victim = board[position_to_array(x + x_offset * x_direction, y + y_offset * y_direction)];

      // La conclusion es, si lo primero que encuentro cuando recorro la diagonal son dos fichas juntas pegadas,
      // rompo el loop porque en esa diagnonal no puedo hacer nada
      if (pre_victim != WHITE_SPACE && possible_victim != WHITE_SPACE && x_offset > 0 && y_offset > 0) {
        break;
      }

      char can_jump = possible_victim != WHITE_SPACE
        && !is_my_team(possible_victim, team)
        && ((x_offset > 0 && y_offset > 0 && pre_victim == WHITE_SPACE) || (x_offset == 0 && y_offset == 0))
        && where_do_i_fall == WHITE_SPACE;

      // Si podemos comer ya retornamos que si
      if (can_jump) {
        return 1;
      }

      x_offset++;
      y_offset++;
    }
    // printf("\n");
    x_direction = x_direction * -1;
    // Si ya pasaron dos iteraciones cambiamos la direccion de y (ya se hicieron izquierda y derecha de la
    // primer direccion)
    if (i == 1) {
      y_direction = y_direction * -1;
    }

    i++;
  }

  return 0;
}

void set_teams_can_jump(Board *board) 
{
  // Reseteamos que pueda comer antes de calcularlo
  board->can_jump_white_team = 0;
  board->can_jump_black_team = 0;

  for (int i = 0; i < 32; i++) {
    char piece_color = board->representation[i];
    int team = get_team(piece_color);

    // Si hay un espacio en blanco no evaluamos nada...
    if (team == -1) {
      continue;
    }

    // Nos fijamos si el equipo blanco o el negro ya esta marcado como que puede comer, para no hacer los calculos
    // de nuevo
    if ((team == TEAM_WHITE && !board->can_jump_white_team) || (team == TEAM_BLACK && !board->can_jump_black_team)) {
      // Obtenemos la coordenadas de la ficha
      char x = get_x_from_position(array_to_position(i));
      char y = get_y_from_position(array_to_position(i));

      // Nos fijamos si puede comer...
      char can_jump = is_crowned(piece_color)
        ? piece_crowned_can_jump_from(board->representation, team, x, y)
        : piece_can_jump_from(board->representation, team, x, y);

      // Si puede lo anotamos en el tablero
      if (can_jump) {
        if (team == TEAM_WHITE) {
          board->can_jump_white_team = 1;
        } else {
          board->can_jump_black_team = 1;
        }
      }
    }
  }
}

char is_valid_common_movement(Board *board, int piece, int pos_x, int pos_y) 
{
  // Chequeamos que NO nos vayamos del tablero.
  if (pos_x < 0 || pos_x > 7 || pos_y < 0 || pos_y > 7) {
    return -1;
  }

  // Chequeamos que a donde queremos ir no haya una ficha
  if (board->representation[position_to_array(pos_x, pos_y)] != WHITE_SPACE) {
    return -1;
  }

  // Dependiendo el color, vemos si se mueve hacia arriba o hacia abajo la ficha
  char p = board->representation[piece] == PIECE_WHITE ? 1 : -1;

  // Obtenemos la posicion de la ficha que queremos mover
  char x = get_x_from_position(array_to_position(piece));
  char y = get_y_from_position(array_to_position(piece));

  // Chequeamos que no nos queremos mover donde estamos
  if (x == pos_x || y == pos_y) {
    return -1;
  }

  // Obtenemos el sentido de X (Si se mueve a izquierda o a derecha)
  char pos_x_sent = pos_x - x;
  pos_x_sent = pos_x_sent / (char)abs(pos_x_sent);

  // Muevo sin comer
  if (pos_x == x + pos_x_sent && pos_y == y + p) {
    return -2;
  // Muevo y como (o sea, me salto un casillero)
  } else if (pos_x == x + 2 * pos_x_sent && pos_y == y + 2 * p) {
    // Si hay una victima y esta tiene distinto color...
    // El Tablero[Ficha] + 2 representa la reina del equipo que esta moviendo es
    // decir, si somos blancas (1) nuestra reina es 3, esto es para fijarnos que
    // nuestra reina no sea una victima, o en otras palabras, que no podamos
    // comer nuestra reina.
    char victim = select_piece(board, pos_x - pos_x_sent, pos_y - p);
    if (victim != WHITE_SPACE && victim != board->representation[piece] && victim != board->representation[piece] + 2)
      return position_to_array(pos_x - pos_x_sent, pos_y - p);
  } else {
    return -1;
  }

  return -1;
}

char is_valid_crowned_movement(Board *board, int piece, int pos_x, int pos_y) 
{
  // Chequeamos que NO nos vayamos del tablero.
  if (pos_x < 0 || pos_x > 7 || pos_y < 0 || pos_y > 7) {
    return -1;
  }

  // Chequeamos que a donde queremos ir no haya una ficha
  if (board->representation[position_to_array(pos_x, pos_y)] != WHITE_SPACE) {
    return -1;
  }

  // Chequeamos que lo que se quiera mover sea una reina
  if (board->representation[piece] == PIECE_WHITE || board->representation[piece] == PIECE_BLACK) {
    return -1;
  }

  // Obtenemos la posicion de la ficha que queremos mover
  char x = get_x_from_position(array_to_position(piece));
  char y = get_y_from_position(array_to_position(piece));

  if (x == pos_x || y == pos_y) {
    return -1;
  }

  // Obtenemos el sentido de X (Si se mueve a izquierda o a derecha)
  char pos_x_sent = pos_x - x;
  pos_x_sent = pos_x_sent / abs(pos_x_sent);

  // Obtenemos el sentido de Y (Si se mueve a izquierda o a derecha)
  char pos_y_sent = pos_y - y;
  pos_y_sent = pos_y_sent / abs(pos_y_sent);

  // Si nos movemos los mismos casilleros tanto en x como en y, entonces nos
  // movimos por una diagonal valida (creo que este checkeo se puede sacar)
  if (abs(pos_x - x) == abs(pos_y - y)) {
    // Para mover hasta la posicion deseada, debemos mirar si no hay alguna
    // ficha en el medio que nos impida el paso. Empezamos el indice en 1 para no
    // chequear nuestra posicion.
    for (int i = 1; i < abs(pos_x - x); i++) {
      char victim = select_piece(board, x + (i * pos_x_sent), y + (i * pos_y_sent));
      // Si el casillero esta ocupado y no es el penultimo al que tenemos que ir
      // entonces hay una ficha en el camino
      if (victim != WHITE_SPACE && i != abs(pos_x - x) - 1)
        return -1;
      // Si el casillero esta ocupado y es el penultimo al que tenemos que ir
      // entonces hay una ficha para comer en el camino
      else if (victim != WHITE_SPACE && i == abs(pos_x - x) - 1) {
        // Nos fijamos que se pueda comer, como en MovComunValido
        if (victim != board->representation[piece] && victim != board->representation[piece] - 2)
          return position_to_array(x + (i * pos_x_sent), y + (i * pos_y_sent));
        else
          return -1;
      }
    }
    // Si pasamos el for es porque no habia ninguna ficha adelante, por lo tanto
    // es un movimiento valido
    return -2;
  }

  return -1;
}

char is_valid_movement(Board *board, int piece, int pos_x, int pos_y) 
{
  // Chequeamos que nos hayan pasado una ficha y no un espacio vacio
  if (board->representation[piece] == WHITE_SPACE)
    return -1;

  // Nos fijamos si la ficha es coronada (3 o 4)
  int result = is_crowned(board->representation[piece])
    ? is_valid_crowned_movement(board, piece, pos_x, pos_y)
    : is_valid_common_movement(board, piece, pos_x, pos_y);

  // Nos fijamos que si puede comer el equipo de la ficha que esta moviendo
  // entonces el movimiento que trato de hacer sea una comida (ya que es
  // obligatoria). Si es una comida, retornamos el movimiento como valido.

  // Si movemos sin comer...
  if (result == -2) {
    int team = get_team(board->representation[piece]);
    // Si soy el equipo blanco y existe algun movimiento en donde puedo comer
    // entonces no comer es invalido...
    if (team == TEAM_WHITE && board->can_jump_white_team) {
      return -1;
    }

    // Lo mismo para el equipo negro...
    if (team == TEAM_BLACK && board->can_jump_black_team) {
      return -1;
    }
  }

  return result;
}

void move_piece(Board *board, int piece, int pos_x, int pos_y) 
{
  if (0 <= position_to_array(pos_x, pos_y) && position_to_array(pos_x, pos_y) <= 3 && board->representation[piece] == PIECE_BLACK)
    board->representation[position_to_array(pos_x, pos_y)] = PIECE_BLACK_CROWNED;
  else if (28 <= position_to_array(pos_x, pos_y) && position_to_array(pos_x, pos_y) <= 31 && board->representation[piece] == PIECE_WHITE)
    board->representation[position_to_array(pos_x, pos_y)] = PIECE_WHITE_CROWNED;
  else
    board->representation[position_to_array(pos_x, pos_y)] = board->representation[piece];

  board->representation[piece] = WHITE_SPACE;
}

int execute_piece_movement(Board *board, int piece, int pos_x, int pos_y) 
{
  char victim = is_valid_movement(board, piece, pos_x, pos_y);
  // Si el movimiento retorna un numero mayor a 0, es porque comimos una ficha.
  // Dicha ficha esta guardada en la variable Victima, y es una posicion en el
  // arreglo de fichas Tablero.

  if (victim >= 0) {
    // Comemos la ficha
    remove_piece(board, victim);

    // Movemos la ficha hacia su posicion de destino
    move_piece(board, piece, pos_x, pos_y);
  }
  // Si es -2 fue un movimiento valido sin comer
  else if (victim == -2) {
    move_piece(board, piece, pos_x, pos_y);
  }

  //Recalculamos quien puede comer en el tablero entero
  set_teams_can_jump(board);

  // Retornamos el resultado de efectuar el movimiento
  return victim;
}
