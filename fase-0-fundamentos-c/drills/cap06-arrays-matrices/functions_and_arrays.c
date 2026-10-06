#include <stdio.h>

// Psar como puntero al primer elemento
void times2(int *a, int len)
{
        for (int i = 0; i < len; i++)
        {
                printf("2: %d\n", a[i] * 2);
        }
}
// Pasarlo como un array sin longitud.
void times3(int a[], int len)
{
        for (int i = 0; i < len; i++)
        {
                printf("3: %d\n", a[i] * 3);
        }
}
// Pasarlo como un array de logitud fija, hace lo mismo que arriba, el numero da igual, lo interpretara de la misma forma, mientras sea mayor de 0
void times4(int a[5], int len)
{
        for (int i = 0; i < len; i++)
        {
                printf("4: %d\n", a[i] * 4);
        }
}

// Estas 3 formas de pasar un array funcionan, pero la mas correcta es la primera, pasando el puntero.
int main(void)
{
        int x[5] = {11, 22, 33, 44, 55};

        times2(x, 5);
        times3(x, 7);
        times4(x, 5);
}
