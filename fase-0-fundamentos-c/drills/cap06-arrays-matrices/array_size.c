#include <stdio.h>
int main(void)
{

        int x[12];

        printf("Número de bytes en el array: %zu\n", sizeof x);     // 48. 4 bytes por elemento por 12 elementos.
        printf("Número de bytes por elemento: %zu\n", sizeof(int)); // 4, el tamaño de un int.

        printf("Número de elementos: %zu\n", sizeof x / sizeof(int)); // 48/4. El array tiene 12 elementos

        printf("Número de bytes necesarios para almacenar un array de 48 doulbles: %zu\n", sizeof(double[48]));
}
