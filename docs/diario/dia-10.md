# Diario de Aprendizaje · Día 10

**Fecha**: 6 de Octubre de 2026  

**Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel  

**Módulo / Proyecto**: `fase-0-fundamentos-c/proyectos/p3-runlog`

---

## 🎯 Objetivos de la Sesión
- [x] Implementar la función de intercambio mediante punteros: `change_pointers(float *a, float *b)`.
- [x] Extender el intercambio a filas completas de una matriz 2D: `swap_rows(float *row_a, float *row_b, int cols)`.
- [x] Crear el algoritmo de ordenamiento `reorder_matrix_by_time` para ordenar intentos/misiones.
- [x] Implementar `calculate_ranking` acoplando el número de misión con su mejor tiempo.
- [x] Descomentar e inspeccionar todas las funciones del proyecto: `best_mision`, `valid_attemps`, `max_streak`, `calculate_averange`, `calculate_ranking`.

---

## 🧠 Conceptos Clave de C y Bajo Nivel

### 1. Punteros y Matrices en Memoria Física (Row-Major Order)
- Una matriz bidimensional en C (`matrix[FILAS][COLS]`) no existe como tal en la memoria física; es una secuencia continua y plana de bytes en la memoria RAM.
- Al escribir `matrix[j]`, la expresión **decae a la dirección de memoria** donde comienza la fila `j` (`&matrix[j][0]`).
- **Error descubierto y resuelto**: Comparar `matrix[j] > matrix[j + 1]` compara las **direcciones de memoria**, nunca los valores. Como la fila `j` se sitúa antes en RAM que la fila `j + 1`, la condición siempre resultaba falsa.
- **Solución correcta**: Acceder a la columna donde vive el dato real: `matrix[j][1] > matrix[j + 1][1]`.

### 2. Acoplar Datos en Filas (Identificador + Métrica)
- Para que el número de misión no se pierda al ordenar los tiempos, se crea una matriz auxiliar de 2 columnas:
  - **Columna 0**: ID de la misión (`1.0`, `2.0`, ...).
  - **Columna 1**: Mejor tiempo obtenido (`best_time`).
- Al invocar `swap_rows`, toda la fila se intercambia en bloque, garantizando que el tiempo viaje siempre junto a su misión correspondiente.

---

## 🔍 Revisión de Código y Casos Borde Encontrados

Tras descomentar todas las funciones en `src/main.c`, hemos identificado los siguientes puntos clave:

### 1. `calculate_ranking` y `reorder_matrix_by_time` ✅ (Resuelto)
- **Estado**: Funciona al 100% y compila sin advertencias con `-Wall -Wextra -Werror`.
- **Comprobación**:
  - Si Misión 2 tiene mejor tiempo que Misión 1 (ej. 2.00s vs 5.00s), el algoritmo intercambia las filas completas y ubica la Misión 2 en primer puesto.
  - Blindado con la condición `array[i][j] > 0 && (best_time_actual_mision == 0 || array[i][j] < best_time_actual_mision)` para descartar intentos no válidos (`-1`).

### 2. `best_mision` y el caso de intentos inválidos (`-1`) ✅ (Resuelto)
- **Corrección aplicada**:
  ```c
  if (array[i][j] > 0 && (best_time == 0 || array[i][j] < best_time))
  ```
  Ahora los intentos `-1` se descartan de inmediato y encuentra con precisión el menor tiempo positivo incluso si el primer intento no es válido. Comprobado con éxito en consola (`4.00s` y `2.00s`). Saltos de línea y numeración humana corregidos (`i + 1`).

### 3. `max_streak` (Racha de reducción de tiempo) ⚠️
- **Problema detectado**:
  - En la cláusula `else`, la asignación `max_streak = streak;` sobrescribe el récord alcanzado sin comprobar si `streak > max_streak`.
  - Si el primer intento es `-1`, la condición `last_attempt == 0` lo cuenta erróneamente como parte de la racha.
- **Corrección recomendada**:
  - Ignorar los `-1` en el cálculo de rachas y actualizar el máximo únicamente con `if (streak > max_streak) max_streak = streak;`.

### 4. `calculate_averange` (Promedio) ⚠️
- **Problema detectado**:
  - Si todos los intentos de una misión son inválidos (`valid_attemps == 0`), se produce una **división por cero** (`total_sum / 0`), generando `nan`.
- **Corrección recomendada**:
  - Envolver el cálculo en un `if (valid_attemps > 0)`.

---

## 📝 Mis Notas y Reflexiones (Espacio para editar)
*(Escribe aquí tus conclusiones, dudas o ideas para la próxima sesión)*

- 

---

## 🚀 Próximos Pasos (Planificación para Mañana · Día 11)
- [ ] **Diseñar y crear suite de tests para `runlog`**: Crear pruebas automatizadas con scripts/entradas controladas para validar los casos límite (intentos `-1` aislados y consecutivos, rankings con tiempos idénticos, misiones sin intentos válidos).
- [ ] **Blindar división por cero en `calculate_averange`** cuando `valid_attemps == 0`.
- [ ] **Refinar `max_streak`** para ignorar `-1` y preservar el récord global sin sobrescribirlo.

---

## 📦 Commit de GitHub
```text
Day-10: Ordenamiento de matrices 2D, punteros y blindaje de ranking en Runlog
```
