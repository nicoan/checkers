#include "list.c"

// A list node
typedef struct nodo_ nodo;

/* The structure of the list.
 *
 * It contains:
 * nodo *first : A pointer to the first element
 * nodo *last  : A pointer to the last element
 */
typedef struct list_ list;

/* Function: createList()
 *
 * Returns an empty list.
 */
list *create_list();


/* Function: append()
 *
 * Adds data at the end of the list.
 *
 * Arguments:
 * list *l     : The list where we add the data.
 * void *datos : The data we want to add.
 *
 * Returns the list l with "datos" at the end of it.
 */
void append (list *l, void *data);

/* Function: pop()
 *
 * Adds data at the begining of the list.
 *
 * Arguments:
 * list *l     : The list where we add the data.
 * void *datos : The data we want to add.
 *
 * Returns the list l with "datos" in the begining.
 */

void push (list *l, void *data);

/* Function: search()
 *
 * Search specific data on the list. We have an argument that is a compare function,
 * that takes two arguments (the two we want to compare) and returns 1 if they're
 * equal or false otherwise.
 *
 * Arguments:
 * list *l                      : The list where we look for the data.
 * void *datos                  : The data we look for.
 * (* cmp_func)(void *, void *) : The compare function.
 *
 * Returns 1 if data was found or 0 otherwise
 */

int search(list *l, void *data, int (* cmp_func)(void *, void *));


/* Function: print()
 *
 * Pretty print all the list. We have an argument that is a print function. This
 * function must take data and prettyprint it.
 *
 * Arguments:
 * list *l                      : The list we want to print.
 * (* func_pr)(void *, void *)  : The print function.
 *
 */

void print (list *l, void (* func_pr)(void *));

/* Function: isEmpty()
 *
 * Arguments:
 * list *l : The list we want to see if it's empty.
 *
 * Returns 1 if the list is empty or 0 therwise.
 */

int is_empty(list *l);

/* Function: concatenate()
 *
 * Concatenate te two lists of the arguments. We concat the second list into the fisrt.
 * The second list is liberated and the fist one has the elements of the two lists.
 *
 * Arguments:
 * list *l1 : The fist list we want to concatenate.
 * list *l1 : The second list we want to concatenate.
 *
 */

void concatenate(list *l1, list *l2);

/* Function: delete()
 *
 * Delete specific data on the list. We have an argument that is a compare function,
 * that takes two arguments (the two we want to compare) and it's used to find the
 * data we want to delete.
 *
 * Arguments:
 * list *l                      : The list where we want to delete the data.
 * void *datos                  : The data we want to delete.
 * (* cmp_func)(void *, void *) : The compare function.
 *
 */
void delete_element(list *l, void *data, int (* cmp_func)(void *, void *));

/* Function: singleton()
 *
 * Creates a new list with an element inside.
 *
 * Arguments:
 * void *datos : The data we want to add to the list.
 *
 * Returns a list with a single element.
 */
list *singleton(void *data);


/* Function: duplicate()
 *
 * Creates a copy of a list
 *
 * Arguments:
 * list *: List to be copied
 *
 * Returns a copy of the list *l
 */
list *duplicate(list *l);
