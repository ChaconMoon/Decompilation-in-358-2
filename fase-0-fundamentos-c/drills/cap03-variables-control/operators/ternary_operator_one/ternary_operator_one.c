#include <stdio.h>
int main(void)
{
        int y;
        int x = 10;
        y = x > 10 ? 17 : 37;
        printf("%d\n", y);

        // Es el equivalente a este código.

        if (x > 10)
        {
                y = 17;
        }
        else
        {
                y = 37;
        }
        printf("%d\n", y);
}