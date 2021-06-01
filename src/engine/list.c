#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct listnode_ {
  void *data;
  struct listnode_ *next;
  struct listnode_ *prev;
} ListNode;

typedef struct list_ {
  ListNode *first;
  ListNode *last;
} List;

ListNode *create_node(void *datos)
{
  ListNode *nuevoNodo;

  nuevoNodo = (ListNode*) malloc(sizeof(ListNode));

  nuevoNodo->data = datos;
  nuevoNodo->next = NULL;
  nuevoNodo->prev = NULL;

  return nuevoNodo;
}

List *create_list()
{
  List *newList;

  newList = (List*) malloc(sizeof(List));

  newList->first = NULL;
  newList->last = NULL;

  return newList;
}

void free_list(List *l)
{
  ListNode *tmp, *head;
  head = l->first;

  while (head != NULL) {
    tmp = head;
    head = head->next;
    free(tmp);
  }

  free(l);
}

void free_list_f(List *l, void (* freefnc)(void*))
{
  ListNode *tmp, *head;
  head = l->first;

  while (head != NULL) {
    tmp = head;
    head = head->next;
    freefnc(tmp->data);
    free(tmp);
  }

  free(l);
}


/* Function: isEmpty()
 *
 * Arguments:
 * list *l : The list we want to see if it's empty.
 *
 * Returns 1 if the list is empty or 0 therwise.
 */

int is_empty(List *l)
{
  return (l == NULL || (l->first == NULL && l->last == NULL));
}

/* Function: singleton()
 *
 * Creates a new list with an element inside.
 *
 * Arguments:
 * void *datos : The data we want to add to the list.
 *
 * Returns a list with a single element.
 */
List *singleton(void *data)
{
  List *new_list;
  ListNode *new_item;

  new_list = (List*) malloc(sizeof(List));
  new_item = (ListNode*) malloc(sizeof(ListNode));

  new_item->data = data;
  new_item->prev = NULL;
  new_item->next = NULL;

  new_list->first = new_item;
  new_list->last = new_item;

  return new_list;
}

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
void append(List *l, void *data)
{
  ListNode *new_item;

  new_item = (ListNode*) malloc(sizeof(ListNode));

  new_item->data = data;
  new_item->next = NULL;

  //If the last item is NULL then the list MUST be empty (first item is also NULL)
  if (l->last == NULL) {
    l->first = new_item;
    l->last = new_item;
  } else {
    new_item->prev = l->last;
    (l->last)->next = new_item;
    l->last = new_item;
  }
}

/* Function: pop()
 *
 * Adds data at the begining of the list.
 *
 * Arguments:
 * list *l     : The list where we add the data.
 * void *datos : The data we want to add.
 *
 * Returns the list l with "data" in the begining.
 */
void push(List *l, void *data)
{
  ListNode *new_item;

  new_item = (ListNode*) malloc(sizeof(ListNode));

  new_item->data = data;
  new_item->prev = NULL;

  if (is_empty(l)) {
    new_item->next = NULL;
    l->first = new_item;
    l->last = new_item;
  } else {
    new_item->next = l->first;
    (l->first)->prev = new_item;
    l->first = new_item;
  }
}

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

int search(List *l, void *data, int (* cmp_func)(void *, void *))
{
  ListNode *aux;

  for (aux = l->first; aux != NULL; aux = aux->next) {
    if ((*cmp_func)(data, aux->data)) {
      return 1;
    }
  }

  return 0;
}

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
void print(List *l, void (* func_pr)(void *))
{
  ListNode *aux;

  if (l == NULL || is_empty(l))
    printf("[]");
  else {
    printf("[");
    for (aux = l->first; aux != NULL; aux = aux->next) {
      (*func_pr)(aux->data);
      if (aux->next != NULL) printf(",");
    }
    printf("]");
  }
}

/* Function: concatenate()
 *
 * Concatenate the two lists passed in the arguments. We concat the second list into the fisrt.
 * The second list is freed and the first one contains the elements of both lists.
 *
 * Arguments:
 * list *l1 : The fist list we want to concatenate.
 * list *l1 : The second list we want to concatenate.
 *
 */
void concatenate(List *l1, List *l2)
{
  if (is_empty(l1)) {
    if (l1 == NULL) {
      l1 = create_list();
    }

    l1->first = l2->first;
    l1->last = l2->last;
  }
  else if (!is_empty(l2)) {
    //El elemento anterior del primer elemento de la lista dos
    //es el ultimo elemento de la lista 1.
    (l2->first)->prev = l1->last;
    //El elemento siguiente del ultimo elemento de la lista uno
    //es el primero de la lista dos.
    (l1->last)->next = l2->first;

    l1->last = l2->last;
  }
  free(l2);
}

/* Function: delete()
 *
 * Delete specific data on the list. We have an argument that is a compare function,
 * that takes two arguments (the two we want to compare), used to find the data we 
 * want to delete.
 *
 * Arguments:
 * list *l                      : The list where we want to delete the data.
 * void *datos                  : The data we want to delete.
 * (* cmp_func)(void *, void *) : The compare function.
 *
 */
void delete_element(List *l, void *data, int (* cmp_func)(void *, void *))
{
  ListNode *aux;
  if (!is_empty(l)) {
    for (aux = l->first; aux != NULL; aux = aux->next) {
      if ((*cmp_func)(data, aux->data)) {

        //Si el dato anterior es null, entonces estamos al principio de
        //la lista
        if (aux->prev == NULL) {
          l->first = aux->next;
          //Esto es porque habia un segundo elemento
          if (l->first != NULL) {
            (l->first)->prev = NULL;
          } else {
            //Si no habia un segundo elemento..
            l->last = NULL;
          }
          free(aux);
          break;
        }
        //Si el dato siguiente es null, entonces estamos al final de
        //la lista
        else if (aux->next == NULL) {
          l->last = aux->prev;
          (l->last)->next = NULL;
          free(aux);
          break;
        } else {
          (aux->prev)->next = aux->next;
          (aux->next)->prev = aux->prev;
          free(aux);
          break;
        }
      }
    }
  }
}

/* Function: duplicate()
 *
 * Creates a copy of a list
 *
 * Arguments:
 * list *: List to be copied
 *
 * Returns a copy of the list *l
 */
List *duplicate(List *l, size_t data_size)
{
  List *duplicated_list = create_list();

  if (is_empty(l)) return duplicated_list;

  //Ponemos el primer elemento
  ListNode *new_item;
  ListNode *last_new_item;
  for (ListNode *aux = l->first; aux != NULL; aux = aux->next) {
    new_item = (ListNode*) malloc(sizeof(ListNode));

    new_item->data = malloc(data_size);
    memcpy(new_item->data, aux->data, data_size);
    new_item->next = NULL;

    if (is_empty(duplicated_list)) {
      new_item->prev = NULL;
      duplicated_list->first = new_item;
    } else {
      last_new_item->next = new_item;
      new_item->prev = last_new_item;
    }
    last_new_item = new_item;
  }

  //Ponemos como ultimo item, el ultimo creado.
  duplicated_list->last = new_item;
  return duplicated_list;
}
