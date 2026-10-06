#include <stdio.h>
int main(void)
{
        int i;
        int *p;

        p = &i;

        i = 10;
        *p = 20;

        printf("i es %d\n", i);  // Imprime 20
        printf("i es %d\n", *p); // Imprime de-referencia de p es lo mismo que i.
}