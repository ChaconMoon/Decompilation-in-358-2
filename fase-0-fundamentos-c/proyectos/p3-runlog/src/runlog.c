#include <stdio.h>
#include "runlog.h"

void change_pointers(float *a, float *b)
{
        float temp = *a;
        *a = *b;
        *b = temp;
}
void swap_rows(float *row_a, float *row_b, int cols)
{
        for (int c = 0; c < cols; c++)
        {
                change_pointers(&row_a[c], &row_b[c]);
        }
}
void reorder_matrix_by_time(float (*matrix)[INTENTOS], int len)
{
        for (int i = 0; i < len; i++)
        {
                for (int j = 0; j < len - 1 - i; j++)
                {
                        if (matrix[j][1] > matrix[j + 1][1])
                        {
                                swap_rows(matrix[j], matrix[j + 1], MISIONES);
                        }
                }
        }
}
void calculate_averange(float (*array)[INTENTOS])
{
        int valid_attemps;
        float total_sum;
        for (int i = 0; i < MISIONES; i++)
        {
                valid_attemps = 0;
                total_sum = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] > 0)
                        {
                                valid_attemps++;
                                total_sum += array[i][j];
                        }
                }
                if (valid_attemps > 0)
                {
                        printf("El promedio es: %.2f\n", total_sum / valid_attemps);
                }
                else
                {
                        printf("No hay intentos validos\n");
                }
        }
}
void calculate_ranking(float (*array)[INTENTOS])
{
        float bests_times[MISIONES][INTENTOS];
        float best_time_actual_mision;
        int valid_missions = 0;
        for (int i = 0; i < MISIONES; i++)
        {
                best_time_actual_mision = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] > 0 && (best_time_actual_mision == 0 || array[i][j] < best_time_actual_mision))
                        {
                                best_time_actual_mision = array[i][j];
                        }
                }
                if (best_time_actual_mision > 0)
                {
                        // Guardamos explícitamente ambos datos:
                        bests_times[valid_missions][0] = i + 1;
                        bests_times[valid_missions][1] = best_time_actual_mision;
                        valid_missions++;
                }
        }
        reorder_matrix_by_time(bests_times, valid_missions);

        for (int i = 0; i < valid_missions; i++)
        {
                printf("Mision %.0f. Mejor tiempo %.2f\n", bests_times[i][0], bests_times[i][1]);
        }
}
void max_streak(float (*array)[INTENTOS])
{
        for (int i = 0; i < MISIONES; i++)
        {
                int streak;
                int max_streak = 0;
                float last_attempt;
                int has_valid = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] <= 0)
                        {
                                continue;
                        }
                        if (!has_valid)
                        {
                                has_valid = 1;
                                streak = 1;
                                last_attempt = array[i][j];
                        }

                        else if (array[i][j] < last_attempt)
                        {
                                streak++;
                                if (streak > max_streak)
                                {
                                        max_streak = streak;
                                }
                                last_attempt = array[i][j];
                        }
                        else
                        {
                                streak = 1;
                                last_attempt = array[i][j];
                        }
                }
                if (!has_valid)
                {
                        printf("Mision %d. No hay intentos validos\n", i + 1);
                }
                else
                {

                        printf("Mision %d. Numero maximo de recha de mejores tiempos %d\n", i + 1, max_streak);
                }
        }
}
void valid_attemps(float (*array)[INTENTOS])
{
        int valid_attemps;
        for (int i = 0; i < MISIONES; i++)
        {
                valid_attemps = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] > 0)
                        {
                                valid_attemps++;
                        }
                }
                printf("Mision %d. Numero de intentos validos: %d\n", i + 1, valid_attemps);
        }
}
void best_mision(float (*array)[INTENTOS])
{
        float best_time;
        for (int i = 0; i < MISIONES; i++)
        {
                best_time = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] > 0 && (best_time == 0 || array[i][j] < best_time))
                        {
                                best_time = array[i][j];
                        }
                }
                if (best_time > 0)
                {
                        printf("Mision %d. Mejor tiempo %.2f\n", i + 1, best_time);
                }
                else
                {
                        printf("Mision %d. No hay intentos validos\n", i + 1);
                }
        }
}
void print_times(float (*array)[INTENTOS])
{
        for (int i = 0; i < MISIONES; i++)
        {
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] != -1)
                        {
                                printf("Mision %d intento %d: tiempo: %.2f\n", i + 1, j + 1, array[i][j]);
                        }
                        else
                        {
                                printf("Mision %d intento %d: Invalido\n", i + 1, j + 1);
                        }
                }
        }
}
void write_times(float (*array)[INTENTOS])
{

        for (int i = 0; i < MISIONES; i++)
        {
                for (int j = 0; j < INTENTOS; j++)
                {

                        printf("Mision %d intento %d: Indique el tiempo: ", i + 1, j + 1);
                        scanf("%f", &array[i][j]);
                }
        }
}