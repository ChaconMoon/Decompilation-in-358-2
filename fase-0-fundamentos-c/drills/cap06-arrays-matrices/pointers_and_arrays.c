#include <stdio.h>

int main(void)
{
        int a[5] = {11, 22, 33, 44, 55};

        int *p;

        p = &a[0]; // Puntero al primer elemento de la matriz

        p = a; // Esto es lo mismo de arriba pero mas bonito.

        printf("%d\n", *p); // Imprime "11"
}