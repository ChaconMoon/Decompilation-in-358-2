# Diario de aprendiendo a decompilar en 358/2 dias - Dia 10: (Comienza la organización)

### Info:
- **Fecha**: 6 de Octubre de 2026
- **Objetivo general de la sesión**: Ordenamiento de matrices 2D en memoria física, intercambio de filas por punteros y blindaje del ranking en Runlog.
- **Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel

### Entrada del diario:

<img src="./diario-images/day-10.png" width="100%" alt="day-10 card">

## Aprendiendo Punteros, Matrices y punteros a matrices

He terminado el proyecto implementando las funciones necesarias. Se me quedó únicamente la función donde me tocaba crear un array auxiliar porque me pedía reordenar una matriz en base a unos criterios; en este caso, se me pedía extraer unos datos en concreto de un array e insertarlos en otro para posteriormente reordenar ese nuevo array. 

Como dije en entradas del blog anteriores, durante la ejecución de este software la finalidad era **no modificar el conjunto de datos original**, por lo que en la función `calculate_ranking` de [`fase-0-fundamentos-c/proyectos/p3-runlog/src/runlog.c`](../../fase-0-fundamentos-c/proyectos/p3-runlog/src/runlog.c) tuve que crear una matriz auxiliar:

```C
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
```

Fíjate en `reorder_matrix_by_time`: esa función lo que hace es ordenar la matriz que se le pasa por tiempo. La misión es el índice `0` y el tiempo es el índice `1`.

Esto se vería así en memoria:

```C
[1][3.4] // Mision 1 y tiempo
[2][2.5] // Mision 2 y tiempo
```

Para estar ordenadas por speedrun, la misión 2 (2.5s) debería estar por delante de la 1 (3.4s). Para eso se usa esta función:

```C
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
```

Esta función compara el tiempo de una fila con el de la siguiente (`matrix[j][1] > matrix[j + 1][1]`), es decir, mira la columna 1 (el tiempo). Si el tiempo actual es mayor que el siguiente, se intercambian las filas completas pasándolas a dos funciones auxiliares:

```C
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
```

Estas 2 funciones hacen un recorrido por cada una de las columnas de 2 filas y las intercambian, todo esto hecho mediante punteros (`*a`, `*b`). Así interactuamos directamente sobre la memoria RAM donde viven los datos.

Sé que tal vez es muy poco para una entrada del diario, pero creedme: incluso con la IA para preguntar cosas me ha costado entenderlo, aunque tengo que reconocer que me parece muy chulo cómo funciona, jeje.

Con esto he terminado el proyecto, listo para testearlo al día siguiente.

Seguiré contando, jeje. ¡Nos vemos en la siguiente entrada del blog!

### Checklist:
- [x] Implementar la función de intercambio mediante punteros: `change_pointers(float *a, float *b)`.
- [x] Extender el intercambio a filas completas de una matriz 2D: `swap_rows(float *row_a, float *row_b, int cols)`.
- [x] Crear el algoritmo de ordenamiento `reorder_matrix_by_time` sobre la columna de tiempos.
- [x] Implementar `calculate_ranking` acoplando ID de misión con su mejor tiempo.

### Tags:
#DecompilandoEn358Dias #C #Matrices #Punteros #RowMajor #Runlog

