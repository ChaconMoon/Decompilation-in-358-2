#include <stdio.h>

int main(void)
{
        int x = 40;
        printf("El número %d es %s\n", x, x % 2 == 0 ? "Par :)" : "Impar :(");
}
