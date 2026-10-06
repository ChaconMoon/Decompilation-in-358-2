#include <stdio.h>
#define LENGHT 10

int main(void)
{
        int i;
        int a[5] = {22, 37, 3490, 18, 95};

        for (i = 0; i < 5; i++)
        {
                printf("A es:%d\n", a[i]);
        }
        int b[3] = {0, [2] = 7};

        for (i = 0; i < 3; i++)
        {
                printf("B es:%d\n", b[i]);
        }
        int c[LENGHT] = {[LENGHT - 3] = 3, 2, 1};

        for (i = 0; i < LENGHT; i++)
        {
                printf("C es:%d\n", c[i]);
        }
}