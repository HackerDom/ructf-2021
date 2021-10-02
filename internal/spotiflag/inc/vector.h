#ifndef _VECTOR_H
#define _VECTOR_H

#include <stdlib.h>
#include <stdbool.h>


typedef void (*vector_item_t);

typedef void (*vector_item_clear_t)(vector_item_t);

typedef struct vector_s {
    bool is_initialized;
    size_t size;
    size_t max_size;
    vector_item_t *items;
    vector_item_clear_t item_clear;
} vector_t;

void vector_init(vector_t *vector, vector_item_clear_t item_clear);

void vector_clear(vector_t *vector);

vector_item_t vector_get(vector_t *vector, size_t index);

void vector_append(vector_t *vector, vector_item_t item);


#endif
