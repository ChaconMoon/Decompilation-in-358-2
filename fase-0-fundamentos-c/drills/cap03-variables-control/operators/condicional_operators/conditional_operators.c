#include <stdio.h>

int A = 5;
int B = 7;

int main(void)
{
        A == B; // Verdadero si A es equivalente a B
        A != B; // Verdadero si A no es equivalente a B
        A < B;  // Verdadero si A es menor que A
        A > B;  // Verdadero si A es mayor que B
        A <= B; // Verdadero si A es menor o igual que A
        A >= B; // Verdadero si A es mayor o igual que B

        // Estas expresiones se suelen usar en los condicionales if

        if (A <= 10)
        {
                printf("Exito!\n");
        }
}
