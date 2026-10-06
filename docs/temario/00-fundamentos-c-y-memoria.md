# Temario Detallado · Fase 0: Cimientos de C y Memoria de Bajo Nivel

Bienvenido a la **Fase 0**. Esta fase sienta las bases indispensables de programación antes de tocar un desensamblador. En decompilación y desarrollo de videojuegos para consolas retro, C no es un lenguaje de programación de alto nivel abstracto: **es una forma humana de estructurar bytes y punteros sobre la memoria RAM física**.

---

## Bloque 0.1: Repaso y Cierre de Fundamentos

### Conceptos Clave
- **El Modelo de Memoria en C**: Stack (pila de llamadas locales), Heap (memoria dinámica), Data/BSS (variables globales y estáticas), Text (código binario ejecutable).
- **Tipos y Representación**: Por qué un `char` es 1 byte, un `short` es 2 bytes, y un `int`/`long` dependen de la arquitectura (32 bits en consolas retro como GBA, NDS, PS1 y N64).
- **Aritmética de Punteros**: Qué significa realmente `*(ptr + i)` frente a `arr[i]`.

### Proyectos y Ejercicios
1. **Analizador de Sensores (`proyectos/p1-sensores`)** [Completado]:
   - Aprendizaje: Iteración sobre arrays de floats, cálculo de `sizeof` con `%zu`, condicionales para umbrales de alerta.
2. **Módulo de Calificación (`proyectos/p2-calificacion`)** [Completado]:
   - Aprendizaje: Comparación de respuestas de candidatos con plantilla usando `switch`, penalizaciones y omisiones.
3. **Runlog (`proyectos/p3-runlog`)** [En curso - Hito final]:
   - **Misión 0.1.13**: Completar `calculate_averange` descartando los intentos marcados con `-1`.
   - **Misión 0.1.14**: Completar `calculate_ranking` usando un array auxiliar de índices sin alterar los datos originales.
   - **Misión 0.1.15**: Implementar `intercambiar(float *a, float *b)` y el ordenamiento de burbuja.
   - **Misión 0.1.16**: Compilación limpia con `-Wall -Wextra -Werror`.

---

## Bloque 0.2: Cadenas, Structs, Enums y Alineación de Memoria

### Conceptos Clave
- **Cadenas en C**: A diferencia de lenguajes modernos, las cadenas no tienen longitud guardada en un objeto; terminan cuando aparece un byte con valor `0` (`'\0'`).
- **Estructuras (`struct`)**: La base para modelar entidades de juego (personajes, objetos de inventario, entidades enemigas).
- **Alineación de Memoria (Data Alignment & Padding)**:
  - Las CPUs de 32 bits (como el procesador ARM de Nintendo DS) prefieren leer enteros de 4 bytes en direcciones de memoria múltiplos de 4.
  - El compilador añade bytes invisibles (*padding*) entre miembros de un struct para mantener la alineación natural.
  - La directiva `__attribute__((packed))` elimina el padding, lo cual es vital cuando leemos un struct directamente desde un archivo binario o una ROM.

### Ejercicios Prácticos
- **Drill 0.2.1**: Demostración del byte nulo `\0` imprimiendo una cadena cortada a mitad de array.
- **Drill 0.2.2**: Escribir `mi_strlen` recorriendo la memoria con un puntero `while (*s++)`.
- **Drill 0.2.6 & 0.2.7**: Comparar `sizeof(struct SinEmpaquetar)` vs `sizeof(struct Empaquetado)` en consola e imprimir los offsets de cada miembro con la macro `offsetof()`.
- **Proyecto Gamer (Paneles de KH Days)**:
  ```c
  typedef struct {
      u8 id;
      u8 tipo;       /* 1 = magia, 2 = habilidad, 3 = objeto */
      u8 nivel;
      u8 ranuras;    /* 1x1, 1x2, etc. */
  } Panel;
  ```

---

## Bloque 0.3: Gestión Dinámica de Memoria y Punteros Avanzados

### Conceptos Clave
- **Gestión Dinámica**: `malloc` solicita bytes contiguos en el Heap del sistema operativo. Si falla, devuelve `NULL`. Es mandatorio comprobar el valor de retorno.
- **Fugas de Memoria (Leaks) y Dangling Pointers**: Acceder a memoria ya liberada con `free()` o no liberarla nunca.
- **Punteros Dobles (`type **`)**: Usados para crear arrays dinámicos de punteros o para modificar el puntero de un llamador dentro de una función.
- **Punteros a Funciones**:
  - Sintaxis: `int (*accion)(Personaje *jugador, int param);`
  - Permiten implementar polimorfismo y tablas de métodos virtuales en C puro.
- **Linear Arena Allocator**:
  - En lugar de usar `malloc`/`free` continuos (que causan fragmentación de RAM mortal para consolas con 4MB de memoria como Nintendo DS), los videojuegos suelen reservar un bloque grande de memoria al arrancar y despachar memoria incrementando un puntero offset.

---

## Bloque 0.4: Manipulación de Bits, Endianness y Entrada/Salida Binaria

### Conceptos Clave
- **Tipos de Tamaño Fijo (`<stdint.h>`)**:
  - `uint8_t` (1 byte, 0..255), `uint16_t` (2 bytes, 0..65535), `uint32_t` (4 bytes, 0..4294967295).
  - En desarrollo de consolas se definen comúnmente como `u8`, `u16`, `u32` y `s8`, `s16`, `s32`.
- **Bitwise Operations**:
  - Máscaras: `flags |= FLAG_CORRER;` (activar bit), `flags &= ~FLAG_CORRER;` (desactivar bit), `if (flags & FLAG_CORRER)` (comprobar bit).
- **Endianness (Orden de Bytes)**:
  - **Little Endian** (ARM en NDS/GBA, x86 en PC): El byte menos significativo va en la dirección de memoria más baja. El valor `0x12345678` se almacena como `78 56 34 12`.
  - **Big Endian** (MIPS en N64, PowerPC en GameCube/Wii): El byte más significativo va primero (`12 34 56 78`).
- **Entrada/Salida Binaria (`stdio.h`)**:
  - Modos `"rb"` (read binary) y `"wb"` (write binary).
  - `fread(&estructura, sizeof(estructura), 1, archivo)` lee exactamente los bytes del disco a la memoria.

### Proyecto Final de Fase 0: Lector de Cabeceras de ROM NDS
Escribirás un programa que abra un archivo `.nds` y lea su cabecera oficial:
- Bytes 0x00..0x0B: Título del juego (12 caracteres).
- Bytes 0x0C..0x0F: Código del juego (ej. `YKGP` para KH 358/2 Days versión europea).
- Bytes 0x14: Capacidad del cartucho (expresada en potencia de 2).
- Bytes 0x6C..0x6D: Checksum de la cabecera.
