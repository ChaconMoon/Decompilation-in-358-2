# Diario de Aprendizaje · Día 11
**Fecha**: 7 de Octubre de 2026  
**Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel  
**Módulo / Proyecto**: `fase-0-fundamentos-c/proyectos/p3-runlog`  
**Hito**: Graduación y Cierre del Bloque 0.1 (100% Completado ✅)

---

## 🎯 Objetivos de la Sesión
- [x] Blindar `calculate_averange` contra división por cero cuando `valid_attemps == 0` (evitando `NaN` en coma flotante IEEE 754).
- [x] Refactorizar `max_streak` como máquina de estados pura: saltar centinelas `-1` (`continue`), corregir sentido de comparación para speedrunning (`< last_attempt`) y ordenar ramas de salida.
- [x] Blindar `calculate_ranking` para excluir misiones sin intentos válidos y compactar la memoria contigua de `bests_times` con el puntero/índice destino `valid_missions`.
- [x] Arquitectura modular en C: creación de `src/runlog.h` con *Include Guards*, separación de `src/runlog.c` (cálculo) y `src/main.c` (interfaz interactiva).
- [x] Configuración del `Makefile` para compilación multi-archivo con `-Wall -Wextra -Werror` y regla automatizada `make test`.
- [x] Implementación de suite de tests unitarios con `<assert.h>` y sanitizers (`-fsanitize=address,undefined`) en `test/test_runlog.c`:
  - `test_change_pointers`
  - `test_swap_rows`
  - `test_reorder_matrix_bt_time`
- [x] Verificar en vivo el mecanismo de aserto fallido (abort y volcado con línea exacta) y aserto superado.

---

## 🧠 Conceptos Clave de C y Bajo Nivel

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

## 📝 Mis Notas y Reflexiones (Espacio para editar)
*(Escribe aquí tus conclusiones, dudas o ideas para la próxima sesión)*

- 

---

## 🚀 Próximos Pasos (Planificación para Mañana · Día 12)
- [ ] **Reestructurar el diario para hacerlo público**: Enfocar el formato del diario hacia una **newsletter personal** y documentar el código de este proyecto para que sea fácilmente comprensible a futuro.
- [ ] **Conversor/Wrapper para Substack**: Diseñar un script/wrapper que permita procesar las entradas del diario en Markdown y convertirlas automáticamente al formato de newsletter para su publicación en **Substack**.
- [ ] **Arranque del Bloque 0.2 (Cadenas y Memoria)**: Estudio de strings en C, punteros a `char` y el terminador nulo `\0` (`0.2.1`).

---

## 📦 Commit de GitHub
```text
Day-11: Modularización en C, include guards y suite de tests unitarios con sanitizers
```
