#include <stdio.h>
int a = 999;

int main(void)
{
        // Tamaño de variables.
        printf("%zu\n", sizeof a);      // Imprime 4, el espacio que ocupa un entero en memoria: 4 bytes.
        printf("%zu\n", sizeof(2 + 7)); // Imprime 4, el espacio que ocupa un entero en memoria: 4 bytes.
        printf("%zu\n", sizeof(3.14));  // Imprime 8, el espacio de un float en memoria: 8 bytes.

        // Tamaño de tipos.
        printf("%zu\n", sizeof(int));  // Imprime 4, el espacio que ocupa un entero en memoria: 4 bytes.
        printf("%zu\n", sizeof(char)); // Imprime 1, el espacio que ocupa un caracter en memoria: 1 byte.
}
