#include <stdio.h>

int x;
int y;
int i;
int j;
int main()
{

        x = 10, y = 20; // Permite ejecutar todo esto como una sola expresión.

        for (i = 0, j = 10; i < 100; i++, j++) // Se usa en los bucles for para poder incluir varias operaciones dentro de cada expresion dentro del for
        {
                printf("%d, %d\n", i, j);
        }
}
