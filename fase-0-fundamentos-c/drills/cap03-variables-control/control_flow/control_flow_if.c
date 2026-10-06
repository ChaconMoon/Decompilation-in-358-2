#include <stdio.h>
int x = 10;
int main(void)
{
        if (x == 10) // Se puede hacer con o sin { } si solo es una linea
                printf("x es 10\n");
        printf("ESTO SE EJECUTA SIEMPRE\n"); // Apartir de la segunda linea esta fuera de la condición, por lo que esto se ejecuta siempre.

        if (x == 7)
        {
                printf("x es 7\n");
        }
        else if (x == 5)
        {
                printf("x no es 5\n");
        }
        else
        {
                printf("x no es ni 7 ni 5\n");
        }
}
