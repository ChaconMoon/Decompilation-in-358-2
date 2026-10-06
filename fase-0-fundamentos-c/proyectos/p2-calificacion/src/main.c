#include <stdio.h>

int main()
{
        int correct_answers[10] = {1, 3, 2, 4, 1, 3, 2, 1, 4, 1};
        int studient_answers[10] = {3, 4, 0, 4, 1, 3, 2, 1, 3, 1};
        float studient_score = 0;
        for (int i = 0; i < 10; i++)
        {
                const int actual_studient_answer = studient_answers[i];
                const int actual_correct_answer = correct_answers[i];

                switch (actual_studient_answer)
                {
                case 0:
                        printf("Pregunta %d: Omision\n", i + 1);
                        break;

                default:
                        studient_score += actual_correct_answer == actual_studient_answer ? 1 : -0.33;
                        printf("Nota actual del estudiante: %.2f\n", studient_score);
                        break;
                }
        }
        studient_score = studient_score < 0 ? 0 : studient_score;
        printf("Nota final del estudiante: %.2f\n", studient_score);
}
