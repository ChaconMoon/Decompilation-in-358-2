#include <stdio.h>

void print_2D_array(int matrix[2][3])
{
        int row, col;
        for (row = 0; row < 2; row++)
        {
                for (col = 0; col < 3; col++)
                {
                        printf("(ROW: %d COL: %d): %d\n", row, col, matrix[row][col]);
                }
        }
}
int main(void)
{
        int x[2][3] = {
            {1, 2, 3}, {4, 5, 6}};

        print_2D_array(x);
}