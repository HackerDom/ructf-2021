#include <stdio.h>

#include "vector.h"


const size_t VECTOR_INITIAL_SIZE = 8;

void vector_init(vector_t *vector, vector_item_clear_t item_clear) {
    if (vector->is_initialized) {
        return;
    }

    vector->size = 0;
    vector->max_size = VECTOR_INITIAL_SIZE;

    vector->items = calloc(vector->max_size, sizeof(vector_item_t));

    if (vector->items == NULL) {
        perror("calloc error");
        exit(1);
    }

    vector->item_clear = item_clear;

    vector->is_initialized = true;
}

void vector_clear(vector_t *vector) {
    if (!vector->is_initialized) {
        return;
    }

    for (size_t i = 0; i < vector->size; i++) {
        if (vector->items[i] == NULL) {
            continue;
        }

        if (vector->item_clear != NULL) {
            vector->item_clear(vector->items[i]);
        }

        free(vector->items[i]);
        vector->items[i] = NULL;
    }

    free(vector->items);
    vector->items = NULL;

    vector->is_initialized = false;
}

vector_item_t vector_get(vector_t *vector, size_t index) {
    if (!vector->is_initialized || index >= vector->size) {
        return NULL;
    }

    return vector->items[index];
}

void vector_resize(vector_t *vector, size_t size) {
    vector->items = realloc(vector->items, sizeof(vector_item_t) * size);

    if (vector->items == NULL) {
        perror("realloc error");
        exit(1);
    }

    vector->max_size = size;
}

void vector_append(vector_t *vector, vector_item_t item) {
    if (!vector->is_initialized) {
        return;
    }

    if (vector->size == vector->max_size) {
        vector_resize(vector, vector->max_size * 2);
    }

    vector->items[vector->size] = item;
    vector->size += 1;
}
