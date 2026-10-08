#include <assert.h>
#include <stdio.h>
#include "../src/runlog.h"

void test_change_pointers(void)
{
        float a = 10.5f;
        float b = 25.5f;

        change_pointers(&a, &b);

        assert(a == 25.5f);
        assert(b == 10.5f);
        printf("--- ✓ test_change_pointers superado ---\n");
}

void test_swap_rows(void)
{
        float row_a[2] = {1.0, 2.0};
        float row_b_expected[2] = {1.0, 2.0};
        float row_b[2] = {3.0, 4.0};
        float row_a_expected[2] = {3.0, 4.0};

        swap_rows(row_a, row_b, 2);

        assert(row_a[0] == row_a_expected[0]);
        assert(row_a[1] == row_a_expected[1]);
        assert(row_b[0] == row_b_expected[0]);
        assert(row_b[1] == row_b_expected[1]);
        printf("--- ✓ test_swap_rows superado ---\n");
}
void test_reorder_matrix_bt_time(void)
{
        float matrix[2][INTENTOS] = {{1.0f, 15.0f, 0.0f, 0.0f, 0.0f}, {2.0f, 5.0f, 0.0f, 0.0f, 0.0f}};
        reorder_matrix_by_time(matrix, 2);
        assert(matrix[0][0] == 2.0f);
        assert(matrix[0][1] == 5.0f);
        assert(matrix[1][0] == 1.0f);
        assert(matrix[1][1] == 15.0f);
        printf("--- ✓ test_reorder_matrix_bt_time superado ---\n");
}
int main(void)
{
        printf("--- EJECUTANDO TESTS (runlog) ---\n");
        printf("--- TEST 1: CHANGE_POINTERS ---\n");
        test_change_pointers();
        printf("--- TEST 2: SWAP_ROWS ---\n");
        test_swap_rows();
        printf("--- TEST 2: REORDER_MATRIX_BY_TIME ---\n");
        test_reorder_matrix_bt_time();
        printf("--- FIN DE LA EJECUCIÓN DE TESTS ---\n");
}