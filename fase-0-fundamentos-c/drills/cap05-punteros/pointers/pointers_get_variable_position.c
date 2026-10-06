#include <stdio.h>

int main(void)
{
        int i = 10;

        printf("El valor de i es: %d\n", i);
        printf("Y su dirección de memoria es %p\n", (void *)&i);
}