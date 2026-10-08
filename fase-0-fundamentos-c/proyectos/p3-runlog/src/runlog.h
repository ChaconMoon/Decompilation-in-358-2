#ifndef RUNLOG_H
#define RUNLOG_H
#define MISIONES 2
#define INTENTOS 5

void change_pointers(float *a, float *b);

void swap_rows(float *row_a, float *row_b, int cols);

void reorder_matrix_by_time(float (*matrix)[INTENTOS], int len);

void calculate_averange(float (*array)[INTENTOS]);

void calculate_ranking(float (*array)[INTENTOS]);

void max_streak(float (*array)[INTENTOS]);

void valid_attemps(float (*array)[INTENTOS]);

void best_mision(float (*array)[INTENTOS]);

void print_times(float (*array)[INTENTOS]);

void write_times(float (*array)[INTENTOS]);

#endif
