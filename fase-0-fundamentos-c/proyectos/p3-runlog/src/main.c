#include <stdio.h>

#define MISIONES 2
#define INTENTOS 5

void calculate_averange(float (*array)[INTENTOS])
{
}
void calculate_ranking(float (*array)[INTENTOS])
{
}
void max_streak(float (*array)[INTENTOS])
{
        int streak;
        int max_streak = 0;
        float last_attempt;
        for (int i = 0; i < MISIONES; i++)
        {
                streak = 0;
                last_attempt = 0;
                max_streak = 0;
                for (int j = 0; j < INTENTOS; j++)
                {
                        if (array[i][j] > 0 && last_attempt > array[i][j] || last_attempt == 0)
                        {
                                streak++;
                                last_attempt = array[i][j];
                        }
                        else
                        {
                                printf("Racha de reducir tiempo: %d\n ", streak);
                                max_streak = streak;
                                streak = 1;
                                last_attempt = array[i][j];
                        }
                }
                printf("Racha de reducir tiempo: %d\n ", streak);
                if (streak > max_streak)
                {
                        max_streak = streak;
                }
                printf("Mision %d. Numero maximo de recha de mejores tiempos %d\n", i + 1, max_streak);
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
                        if (array[i][j] < best_time && array[i][j] > 0 || best_time == 0)
                        {
                                best_time = array[i][j];
                        }
                }
                printf("Mision %d. Mejor tiempo %.2f\n", i, best_time);
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
                                printf("Mision %d intento %d: Invalido\n", i + 1, j + 1, array[i][j]);
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
int main(void)
{
        float tiempos[MISIONES][INTENTOS];
        float (*t)[INTENTOS] = tiempos;

        write_times(t);
        print_times(t);
        best_mision(t);
        valid_attemps(t);
        max_streak(t);
        return 0;
}
