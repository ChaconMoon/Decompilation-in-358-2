# Cierre del Bloque 0.1: Dominando Punteros y Tests Unitarios en C
*Crónicas de un profesor de FP aprendiendo C a bajo nivel, memoria y decompilación*

> 📅 **Período**: Días 10 al 11 | 🏷️ **Reto**: `#DecompilandoEn358Dias` | 🎯 **Hito**: Bloque 0.1

---

## 🎣 1. El Gancho: La trinchera del aula y la pantalla negra
Cuando enseñas programación a diario, es fácil acostumbrarse a las comodidades de los lenguajes modernos. Pero cuando decides quitar las ruedas de entrenamiento y mirar qué ocurre físicamente dentro de la memoria y el procesador de una consola retro, el mundo cambia por completo.

En esta entrega recapitulamos los avances recientes de nuestro viaje de 358,5 días para dominar C y decompilar videojuegos legendarios desde sus entrañas.

## 🧠 2. Bajo el Capó: Lo que la CPU y la RAM nos enseñaron
### 📍 Conceptos Clave (Día 10)
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

### 📍 Conceptos Clave (Día 11)
### 1. La Arquitectura Modular en C: `.h` vs `.c`
- **Declaración vs Definición**: Una función solo se define UNA vez (en el `.c`, generando código máquina en el `.o`), pero se declara tantas veces como sea necesario (en el `.h` con su prototipo terminado en `;`).
- **El Preprocesador es solo un corta-pega**: `#include "runlog.h"` copia literalmente el texto. Si se incluye más de una vez en la misma unidad de traducción sin protección, genera colisiones de símbolos duplicados.
- **Include Guards (`#ifndef RUNLOG_H`, `#define RUNLOG_H`, `#endif`)**: Actúan como centinela en tiempo de preprocesado; la primera inclusión registra el identificador y cualquier inclusión posterior salta el archivo en bloque.

### 2. Compactación de Memoria (Índice Origen vs Índice Destino)
- Al filtrar datos en un array o matriz (ej. misiones válidas para el ranking), no se puede indexar el array destino con el iterador de lectura `i`:
  - Si la Misión 1 falla y la Misión 2 es válida, usar `bests_times[i]` dejaría la fila 0 llena de ceros o basura.
  - La solución a bajo nivel es desacoplar el índice: `bests_times[valid_missions]` apila siempre de forma contigua en memoria empezando desde `0`.

### 3. Testing Unitario con `<assert.h>` y Detección de Memoria
- En C estándar, `assert(condicion)` es la herramienta nativa más rápida y sin dependencias: aborta de inmediato (`SIGABRT`) imprimiendo fichero, función y línea del fallo.
- **AddressSanitizer (ASan) + UBSan**: Con `-fsanitize=address,undefined`, el compilador inserta sondas que interceptan cualquier corrupción silenciosa de RAM, desbordamiento o comportamiento indefinido antes de que el test dé falsos positivos.

### 4. Reflexión Arquitectónica: Separación de Cómputo e I/O
- Funciones que calculan y a la vez ejecutan `printf` no se pueden testear limpiamente con `assert` sin capturar `stdout`.
- Para testear lógica de presentación compleja se necesita separar el cómputo (que devuelva datos) y la representación formateada. Para estructurar esas salidas sin perder ergonomía se requieren **cadenas de caracteres (`char *`)** y **estructuras (`struct`)**, que constituyen el núcleo del Bloque 0.2.

---

## 🛠️ 3. En la Trinchera: El código y los bugs que casi nos vuelven locos
### 🔍 Auditoría y depuración (Día 10)
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

Uno de los mayores aprendizajes al trabajar a bajo nivel es que el compilador no siempre te salvará: la disciplina de compilar con `-Wall -Wextra -Werror` y apoyar los tests con `-fsanitize=address,undefined` convierte horas de depuración a ciegas en fallos inmediatos y reproducibles.

## 🎮 4. Conexión Gamer: De Nintendo DS a Nintendo 3DS
- **Nintendo DS (Kingdom Hearts 358/2 Days)**: Nuestro laboratorio de referencia con el procesador ARM946E-S. Observamos cómo la convención de llamadas AAPCS y la disposición contigua de memoria organizan las misiones y estados de Roxas.
- **Nintendo 3DS (Yo-kai Watch 2: Mentespectros)**: Nuestro gran proyecto independiente de ingeniería inversa. La CPU ARM11 MPCore comparte las mismas convenciones y arquitectura base de registros, preparando el terreno para cuando extraigamos y analicemos el ejecutable `code.bin`.

## 🎓 5. La Píldora del Profe: Hábitos Atómicos y Aprendizaje Continuo
Aprender decompilación no es cuestión de sentarse 8 horas un fin de semana a leer documentación árida; es el resultado acumulativo de micro-retos de 30 minutos al día. Si un concepto parece inabordable, se trocea hasta que quepa en la palma de la mano.

---

### 📊 Estado del Reto y Código Fuente
- 💻 **Repositorio en GitHub**: [Decompilation in 358-2](https://github.com/) *(Actualizado diariamente)*
- 🏷️ **Hashtag de seguimiento en redes**: `#DecompilandoEn358Dias`

*¡Nos vemos en la siguiente entrega bajo el capó!*