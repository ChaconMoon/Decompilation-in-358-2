#include <stdio.h>
void multiply_array(int *a, int len)
{
        for (int i = 0; i < len; i++)
        {
                a[i] *= 2;
        }
}

int main(void)
{
        int array[5] = {1, 2, 3, 4, 5};
        int *p = array;

        for (int i = 0; i < 5; i++)
        {
                printf("Array Original: %d\n", array[i]);
        }
        multiply_array(p, 5);

        for (int i = 0; i < 5; i++)
        {
                printf("Array Duplicado: %d\n", array[i]);
        }
}