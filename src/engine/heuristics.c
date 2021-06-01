#include "board.h"

int heuristic1(Board *board, int team);
int heuristic2(Board *board, int team);

int eval(int strategy, Board *board, int team)
{
  switch (strategy) {
    case 1:
      return heuristic1(board, team);
    case 2:
      return heuristic2(board, team);
    default:
      return heuristic1(board, team);
  }
}

// Heuristic 1

/**
 * We just evaluate the pieces left in the board
 * Kings are more valuable of course
 */
int heuristic1(Board *board, int team)
{
  int points_black = 0;
  int points_white = 0;
  int i = 0;

  while (i < 32) {
    if (board->representation[i] == PIECE_WHITE) points_white += 1;
    else if (board->representation[i] == PIECE_BLACK) points_black += 1;
    else if (board->representation[i] == PIECE_WHITE_CROWNED) points_white += 2;
    else if (board->representation[i] == PIECE_BLACK_CROWNED) points_black += 2;
    i++;
  }

  return team == TEAM_BLACK
    ? points_black - points_white
    : points_white - points_black;
}

// Heuristic 2

/**
 * Besides the amount of pieces left, we also weight the position,
 * if we are in the 'enemy' half of the board we weight higher and
 * we add one point per enemy 'eaten'
 */
int position_points(int position, char ficha)
{
  int y = get_y_from_position(array_to_position(position));
  if (y <= 4)
    return ficha == PIECE_BLACK || ficha == PIECE_BLACK_CROWNED ? 5 : 7;
  else
    return ficha == PIECE_BLACK || ficha == PIECE_BLACK_CROWNED ? 7 : 5;
}

int heuristic2(Board *board, int team)
{
  int quantity_black = 0;
  int points_black = 0;
  int quantity_white = 0;
  int points_white = 0;
  int i = 0;

  while (i < 32) {
    char ficha = board->representation[i];
    if (ficha == PIECE_WHITE) {
      points_white += 3 + position_points(i, ficha);
      quantity_white++;
    } else if (ficha == PIECE_BLACK) {
      points_black += 3 + position_points(i, ficha);
      quantity_black++;
    } else if (ficha == PIECE_WHITE_CROWNED) {
      points_white += 10 + position_points(i, ficha);
      quantity_white++;
    } else if (ficha == PIECE_BLACK_CROWNED) {
      points_black += 10 + position_points(i, ficha);
      quantity_black++;
    }
    i++;
  }

  return team == TEAM_BLACK
    ? points_black + (12 - quantity_white) - points_white
    : points_white + (12 - quantity_black) - points_black;
}

