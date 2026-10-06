#include <stdio.h>

int i;
int j;

int main()
{
        i = 10;
        j = 5 + i++;

        printf("%d,%d\n", i, j); // Imprime 10, 15. i se incrementa despues de hacer la operación.

        i = 10;
        j = 5 + ++i;

        printf("%d,%d\n", i, j); // Imprime 10, 16, i se incrementa antes de hacer la operación.

        for (i = 0; i < 10; i++) // Esto se suele usar en bucles for para aumentar el indice
        {
                printf("i es %d\n", i);
        }
}
