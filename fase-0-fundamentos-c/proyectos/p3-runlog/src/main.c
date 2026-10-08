#include "runlog.h"

int main(void)
{
        float tiempos[MISIONES][INTENTOS];
        float (*t)[INTENTOS] = tiempos;

        write_times(t);
        print_times(t);
        best_mision(t);
        valid_attemps(t);
        max_streak(t);
        calculate_averange(t);
        calculate_ranking(t);
        return 0;
}
