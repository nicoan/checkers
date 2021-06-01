// gcc -shared -fPIC -g auxnc.c -o mm.so
// gcc -shared -fPIC -O3 aux.c -o mm.so
// gcc -shared -fPIC -DH1 -g aux.c -o mm.so && gdb --args python-dbg ctest.py
#include <stdint.h>
#include <limits.h>
#include <sys/param.h>
#include "heuristics.h"

#define UP -1
#define DOWN 1

#ifdef H1
  const int HEURISTIC = 1;
#else
  const int HEURISTIC = 2;
#endif

int visited_nodes;
// MiniMax Node
typedef struct mmnodo_ {
  List* movements;
  Board *board;
  int score;
} MMNodo;

typedef struct boardposition_ {
  char position;
} BoardPosition;

MMNodo *create_mm_node(Board *Tab, List *LMov)
{
  MMNodo *new_node;

  new_node = (MMNodo*) malloc(sizeof(MMNodo));

  new_node->board = Tab;
  new_node->movements = LMov;

  // Puntaje que nunca llegara el minimax
  new_node->score = INT_MIN;

  return new_node;
}

void free_mm_node(MMNodo *n)
{
  free_board(n->board);
  free_list_f(n->movements, free);
  free(n);
}

void print_position(BoardPosition *p)
{
#ifdef DEBUG
  int pos = array_to_position(p->position);
  printf("(%d,%d)", get_x_from_position(pos), get_y_from_position(pos));
#endif
}

void print_mm_node(MMNodo *n)
{
#ifdef DEBUG
  printf("Movimientos: ");
  print(n->movements, (void *)print_position);
  printf("\nPuntaje: %d\n", n->score);
  print_board(n->board);
#endif
}

List *move_common_piece(int piece, Board *board, List *movement_list, char jumped)
{
  //Creamos una lista de movimientos vacia
  List* movements = create_list();

  //Obtenemos la posicion de la ficha
  char x = get_x_from_position(array_to_position(piece));
  char y = get_y_from_position(array_to_position(piece));

  //Si la ficha no esta coronada..
  if (board->representation[piece] < PIECE_WHITE_CROWNED) {
    //Dependiendo el color, vemos si se mueve hacia arriba o hacia abajo la ficha
    char p = (board->representation[piece] == PIECE_WHITE) ? DOWN : UP;

    int i = 1;
    while (i <= 2) {
      int j = 0;
      while (j < 2) {
        i = i * (-1);
        char possible_victim = is_valid_movement(board, piece, x + i, y + abs(i) * p);
        // Si es un movimiento valido y ademas...
        // Esto es para prevenir que, si comio, haga un movimiento que no sea otra comida.
        // La condicion es que no suceda que haya comido y sea un movimiento que no sea para comer (es decir, un -2)
        if (possible_victim != -1 && (!jumped || possible_victim != -2)) {
          // Hacemos una copia del tablero y de la ficha, para que ejecute dicho
          // movimiento.
          Board *tmp_board = duplicate_board(board);

          // Hacemos el movimiento en el tablero copiado, y agregamos el movimiento
          // a la lista de movimientos.
          // Push pone los elementos al principio de la lista, por eso primero agregamos
          // el destino y luego el origen.
          execute_piece_movement(tmp_board, piece, x + i, y + abs(i) * p);

          BoardPosition *new_position = (BoardPosition*) malloc(sizeof(BoardPosition));
          new_position->position = (char) position_to_array(x + i, y + abs(i) * p);
          BoardPosition *old_position = (BoardPosition*) malloc(sizeof(BoardPosition));
          old_position->position = (char) piece;
          List *new_movement_list = singleton(new_position);
          push(new_movement_list, old_position);

          // Creamos un nuevo nodo con el tablero modificado
          // Si venimos sin movimientos de antes solamente creamos el nodo
          // con los nuevos movimientos generados...
          MMNodo *current_movement_node;
          if (movement_list == NULL) {
            current_movement_node = create_mm_node(tmp_board, new_movement_list);
          // Sino, copiamos la movement_list y le appendemos los nuevos movimietos
          } else {
            List *full_movement_list = duplicate(movement_list, sizeof(BoardPosition));
            concatenate(full_movement_list, new_movement_list);
            current_movement_node = create_mm_node(tmp_board, full_movement_list);
          }

          // NOTE: Si se corona no puede volver a comer...
          // NOTE: Esto ya esta contemplado.. por accidente, porque esta funcion
          // no contempla moverse para la direccion contraria.

          // Si fue un movimiento valido y ademas comimos (MovValido devuelve un numero
          // entre 0 y 31 y no solo -2 para indicar que fue valido pero no comimos),
          // vemos si puede comer de nuevo
          if (possible_victim != -2) {
            List *new_movements = move_common_piece(position_to_array(x + i, y + abs(i) * p), tmp_board, current_movement_node->movements, 1);

            // Si los nuevos movimientos no son vacios, quiere decir que comimos de nuevo, en cuyo caso
            // en lugar de pushear el movimiento actual (que tiene una comida parcial porque Vict != -2)
            // concatenamos los nuevos movimientos que tienen las secuencias de comidas completas
            if (!is_empty(new_movements)) {
              concatenate(movements, new_movements);
              free_mm_node(current_movement_node);
            // Si son vacios no comimos de nuevo, por lo tanto el ultimo movimiento de comida es el actual
            // lo agregamos al Nodo
            } else {
              push(movements, current_movement_node);
              free_list(new_movements);
            }
          // Si no comimos es un movimiento comun y corriente lo agregamos a la lista de movimientos.
          } else {
            push(movements, current_movement_node);
          }
        }
        j++;
      }
      i++;
    }
  }
  return movements;
}

List *move_crowned_piece(int piece, Board *board, List *movement_list, char jumped)
{
  List* movements = create_list();
  char x = get_x_from_position(array_to_position(piece));
  char y = get_y_from_position(array_to_position(piece));

  int i = 1;
  int j = 1;
  while (i < 8) {
    int z = 0;
    while (z < 4) {
      i = i * (-1);
      j = z < 2 ? abs(j) * (-1) : abs(j);

      char possible_victim = is_valid_movement(board, piece, x + i, y + j);
      //Si es un movimiento valido...
      if (possible_victim != -1 && (!jumped || possible_victim != -2)) {
        Board *tmp_board = duplicate_board(board);
        execute_piece_movement(tmp_board, piece, x + i, y + j);

        BoardPosition *new_position = (BoardPosition*) malloc(sizeof(BoardPosition));
        new_position->position = (char) position_to_array(x + i, y + j);
        BoardPosition *old_position = (BoardPosition*) malloc(sizeof(BoardPosition));
        old_position->position = (char) piece;
        List *new_movement_list = singleton(new_position);
        push(new_movement_list, old_position);

        MMNodo *current_movement_node;
        if (movement_list == NULL) {
          current_movement_node = create_mm_node(tmp_board, new_movement_list);
        } else {
          List *full_movement_list = duplicate(movement_list, sizeof(BoardPosition));
          concatenate(full_movement_list, new_movement_list);
          current_movement_node = create_mm_node(tmp_board, full_movement_list);
        }

        if (possible_victim != -2) {
          List *new_movements = move_crowned_piece(position_to_array(x + i, y + j), tmp_board, current_movement_node->movements, 1);
          if (!is_empty(new_movements)) {
            concatenate(movements, new_movements);
            free_mm_node(current_movement_node);
          } else {
            push(movements, current_movement_node);
            free_list(new_movements);
          }
        } else {
          push(movements, current_movement_node);
        }
      }
      z++;
    }
    i = abs(i) + 1;
    j = abs(j) + 1;
  }
  return movements;
}

List *generate_movement(Board *board, char team)
{
  //Creamos una lista de movimientos vacia
  List* movements = create_list();

  for (int i = 0; i < 32; i++) {
    char Ficha = board->representation[i];
    if (is_my_team(Ficha, team)) {
      List* MovsParticulares = is_crowned(Ficha)
        ? move_crowned_piece(i, board, NULL, 0)
        : move_common_piece(i, board, NULL, 0);
      concatenate(movements, MovsParticulares);
    }
  }

  return movements;
}

/* =================================================================================
 *                                       Minimax
 * =================================================================================
 */

char is_terminal_state(MMNodo *node)
{
  char amount_whites = 0;
  char amount_blacks = 0;

  for (int i = 0; i < 32; i++) {
    if (get_team(node->board->representation[i]) == TEAM_WHITE)
      amount_whites += 1;
    else if (get_team(node->board->representation[i]) == TEAM_BLACK)
      amount_blacks += 1;
  }

  if (amount_whites == 0 || amount_blacks == 0) return 1;
  else return 0;
}

int alpha_beta(MMNodo *node, char level, int alpha, int beta, char team, char machine_player)
{
  visited_nodes++;

  if (is_terminal_state(node) || level == 0) {
    return eval(HEURISTIC, node->board, machine_player);
  } else {
    //Generamos todos los movimientos posibles
    List *movements = generate_movement(node->board, team);

    //Si no tenemos hijos para la siguiente jugada, entonces devolvemos el puntaje
    //del tablero en donde estamos.
    if (is_empty(movements)) {
      free_list_f(movements, (void*) free_mm_node);
      return eval(HEURISTIC, node->board, machine_player);
    }

    ListNode *aux;
    // El que maximiza...
    if (team == machine_player) {
      for (aux = movements->first; aux != NULL; aux = aux->next) {
        int tmp = alpha_beta((MMNodo*)aux->data, level - 1, alpha, beta, get_enemy_team(team), machine_player);
        alpha = MAX(alpha, tmp);
        if (beta <= alpha) {
          break;
        }
      }
      free_list_f(movements, (void*) free_mm_node);
      return alpha;
    }
    // El que minimiza...
    else {
      for (aux = movements->first; aux != NULL; aux = aux->next) {
        int tmp = alpha_beta((MMNodo*)aux->data, level - 1, alpha, beta, get_enemy_team(team), machine_player);
        beta = MIN(beta, tmp);
        if (beta <= alpha) {
          break;
        }
      }
      free_list_f(movements, (void*) free_mm_node);
      return beta;
    }
  }
  return 0;
}

List* minimax(Board *board, char team, char max_level)
{
  // Generamos los movimientos mios a partir del tablero actual
  List *movements = generate_movement(board, team);

#ifdef DEBUG
  print_board(board);
#endif
  for (ListNode *aux = movements->first; aux != NULL; aux = aux->next) {
    MMNodo *node = (MMNodo*)aux->data;
    // Calculamos el puntaje empezando con el movimiento del adversario
    node->score = alpha_beta(node, max_level, INT_MIN, INT_MAX, get_enemy_team(team), team);
  }

#ifdef DEBUG
  printf("\nMovimientos generados:\n");
  print(movements, (void *)print_mm_node);
#endif
  return movements;
}
