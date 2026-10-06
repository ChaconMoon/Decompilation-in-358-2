#include <stdio.h>

int x = 5;
int y = 30;
int main(int argc, char const *argv[])
{
        if (x < 10 && y > 20) // Hace algo si se cumplen multiples condiciones.
        {
                printf("Haz algo\n");
        }
        if (x < 3 || y > 20) // Hace algo si se cumple una de las 2 condiciones.
        {
                printf("Haz algo, otra vez\n");
        }
        if (!(x > 5)) // Hace lo contrario que a condicion en los parentesis
        {
                printf("Haz algo una última vez\n");
        }
}