#include <stdio.h>

void increment(int *p); // Crea un prototipo de la función incremento.

int main(void)
{
        int i = 10;  // Establece 10 como el valor de i
        int *j = &i; // Asigna a j el valor de la dirección en memoria de i.

        printf("i es %d\n", i);          // i es 10
        printf("i es tambien %d\n", *j); // el valor del puntero j que hace referencia a i es 10

        increment(j); // Manda a incrementar el valor al que haga referencia el puntero j

        printf("i es %d\n", i); // Ahora i vale 11
}

void increment(int *p)
{
        *p += 1; // Aumenta d1 el valor de la variable en la dirección de memeoria a la que hace referencia p
}