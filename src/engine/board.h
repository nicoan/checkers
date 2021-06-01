#include "board.c"

extern const char PIECE_WHITE;
extern const char PIECE_WHITE_CROWNED;
extern const char PIECE_BLACK;
extern const char PIECE_BLACK_CROWNED;
extern const char WHITE_SPACE;

extern const char TEAM_WHITE;
extern const char TEAM_BLACK;

int position_to_array(int x, int y);
int array_to_position(int i);
char get_x_from_position(int position);
char get_y_from_position(int position);

void print_board(Board *board);

char is_valid_movement(Board *board, int piece, int pos_x, int pos_y);
int execute_piece_movement(Board *board, int piece, int pos_x, int pos_y);
char select_piece(Board *board, int x, int y);

int get_enemy_team(int team);
