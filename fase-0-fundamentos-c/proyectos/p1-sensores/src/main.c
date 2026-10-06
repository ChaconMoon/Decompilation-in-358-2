#include <stdio.h>

float temperatures[4];

int main(void)
{
        float temperatures[4];

        temperatures[0] = 19.3;
        temperatures[1] = 23.7;
        temperatures[2] = 30.5;
        temperatures[3] = 40.7;

        for (int i = 0; i < (int)sizeof(temperatures) / (int)sizeof(temperatures[0]); i++)
        {
                float temp_actual = temperatures[i];
                printf("La temperatura %d es: %.1f, cuyo valor ocupa %zu bytes en la memoria RAM\n",
                       i + 1,
                       temp_actual,
                       sizeof(temp_actual));
                if (temp_actual > 36.5)
                {
                        printf("La temperatura %d supera el umbral de riesgo\n", i + 1);
                }
        }
}