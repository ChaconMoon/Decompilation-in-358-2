#include <stdio.h>

int main(void)
{
        int row, col;
        int matrix[2][5] = {{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}};

        for (row = 0; row < (int)(sizeof matrix / sizeof matrix[0]); row++)
        {
                for (col = 0; col < (int)(sizeof matrix[0] / sizeof matrix[0][0]); col++)
                {
                        printf("(ROW: %d COL:%d): %d\n", row, col, matrix[row][col]);
                }
        }
}