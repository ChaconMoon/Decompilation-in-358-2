# Hoja de Ruta Maestra: Aprendiendo a Decompilar en 358/2 Días

Este documento es tu **tablero de mando diario**. Aplica la filosofía de **Hábitos Atómicos**: cada micro-objetivo está diseñado para completarse en bloques de 15 a 45 minutos con un criterio de éxito medible (*Definition of Done*).

---

## Índice de Fases

- [Fase 0 · Cimientos de C y Memoria de Bajo Nivel](#fase-0--cimientos-de-c-y-memoria-de-bajo-nivel)
  - [Dojo de Matching (Decomp Academy · Entrenamiento Transversal)](#dojo-de-matching-decomp-academy--entrenamiento-transversal)
- [Fase 1 · Lectura y Anatomía de Decompilaciones Reales](#fase-1--lectura-y-anatomía-de-decompilaciones-reales)
- [Fase 2 · Matching Decompilation (El Arte del 100% Match)](#fase-2--matching-decompilation-el-arte-del-100-match)
- [Fase 3 · Librerías Gráficas y Multimedia con SDL](#fase-3--librerías-gráficas-y-multimedia-con-sdl)
- [Fase 4 · Source Ports Nativos a PC (Kingdom Hearts 358/2 Days)](#fase-4--source-ports-nativos-a-pc-kingdom-hearts-3582-days)

---

## Fase 0 · Cimientos de C y Memoria de Bajo Nivel
> Guía detallada: [docs/temario/00-fundamentos-c-y-memoria.md](temario/00-fundamentos-c-y-memoria.md)

### Dojo de Matching (Decomp Academy · Entrenamiento Transversal)
- [x] **0.D.1 (Primer Match en GBA Warm Up)** Completar todo el apartado *Warm Up / Foundations* de Game Boy Advance en Decomp Academy (Thumb assembly, convención AAPCS con retornos y argumentos en `r0`, operaciones aritméticas y literal pools con `agbcc`). ¡Múltiples **100% byte-matches** conseguidos!
- [ ] **0.D.2 (Aritmética y Constantes)** Completar bloque *Arithmetic* en Decomp Academy (sumas, restas, operandos invertidos, potencias de 2 optimizadas como shifts y división recíproca).
- [ ] **0.D.3 (Álgebra de Bits)** Completar bloque *Bitwise* en Decomp Academy (máscaras AND, flags OR/XOR, shifts lógicos vs aritméticos y empaquetado de campos de bits).
- [ ] **0.D.4 (Control de Flujo)** Completar bloque *Control Flow* en Decomp Academy (booleanos, saltos condicionales, clamps branchless con máscaras, guard clauses y switches).
- [ ] **0.D.5 (Bucles y Optimización)** Completar bloque *Loops* en Decomp Academy (`for` vs `while` vs `do-while`, strength reduction de variables de inducción y bucles decrecientes).
- [ ] **0.D.6 (Punteros y Structs)** Completar bloques *Pointers* y *Structs* en Decomp Academy (desreferenciación, arrays en memoria, padding, offsets de campos y punteros a funciones).
- [ ] **0.D.7 (Convenciones de Llamada y ABI)** Completar bloque *ABI & Calling Conventions* en Decomp Academy (paso de argumentos en registros, registros preservados *callee-saved*, funciones *leaf* y stack frames).

### Bloque 0.1: Repaso y Cierre de Fundamentos (Estado: 100% Completado ✅)
- [x] **0.1.1** Instalar GCC, Make y configurar `.vscode/tasks.json` en Linux.
- [x] **0.1.2** Escribir `helloworld` y verificar compilación con `-Wall -Wextra`.
- [x] **0.1.3** Manipular variables de tipos primitivos (`int`, `float`, `char`) e imprimir tamaños con `sizeof` y `%zu`.
- [x] **0.1.4** Control de flujo básico: condiciones con `if/else` y selección múltiple con `switch`.
- [x] **0.1.5** Bucles iterativos: recorrer secuencias con `while` y `for`.
- [x] **0.1.6** Funciones: paso de parámetros por valor y prototipos antes de `main()`.
- [x] **0.1.7** Punteros nivel 1: obtener dirección de memoria con `&` e imprimirla con `%p`.
- [x] **0.1.8** Punteros nivel 2: desreferenciar con `*` y modificar una variable local desde otra función.
- [x] **0.1.9** Arrays y memoria continua: comprobar que `arr == &arr[0]`.
- [x] **0.1.10** Matrices bidimensionales: declarar e indexar arrays 2D (`matrix[fila][col]`).
- [x] **0.1.11** Proyecto 1 completado: Analizador de sensores meteorológicos.
- [x] **0.1.12** Proyecto 2 completado: Módulo de calificación de respuestas.
- [x] **0.1.13 (Micro-reto)** En `runlog` (`fase-0-fundamentos-c/proyectos/p3-runlog`): Implementar `void calculate_averange(float (*array)[INTENTOS])` calculando la media ignorando los valores `-1`.
- [x] **0.1.14 (Micro-reto)** En `runlog`: Implementar `void calculate_ranking(float (*array)[INTENTOS])` generando un array auxiliar de índices ordenados por mejor tiempo.
- [x] **0.1.15 (Micro-reto)** En `runlog`: Implementar `void intercambiar(float *a, float *b)` y usarla en un algoritmo de ordenamiento sobre una copia local.
- [x] **0.1.16 (Hito de Graduación Bloque 0.1)**: Compilar `runlog` con `gcc -Wall -Wextra -Werror` con cero advertencias y verificar ejecución interactiva.

### Bloque 0.2: Cadenas, Structs, Enums y Alineación de Memoria
- [ ] **0.2.1** Escribir un programa que demuestre el terminador nulo `\0` en arrays de `char`.
- [ ] **0.2.2** Implementar tus propias versiones de `mi_strlen()` y `mi_strcmp()` recorriendo punteros `const char *s`.
- [ ] **0.2.3** Definir un `struct Personaje` con vida (`int hp`), nivel (`int lvl`) y nombre (`char nombre[16]`).
- [ ] **0.2.4** Crear una función `void curar(struct Personaje *p, int cantidad)` usando el operador flecha `->`.
- [ ] **0.2.5** Definir un `enum Estado` (`ESTADO_IDLE`, `ESTADO_ATACANDO`, `ESTADO_HERIDO`) y usarlo en una máquina de estados con `switch`.
- [ ] **0.2.6 (Bajo el Capó)** Inspeccionar el tamaño de un struct con miembros heterogéneos y observar el padding generado por el compilador.
- [ ] **0.2.7 (Bajo el Capó)** Aplicar `__attribute__((packed))` al struct y comparar el nuevo `sizeof` con el anterior en consola.
- [ ] **0.2.8 (Micro-reto Gamer)**: Modelar el sistema de paneles de *Kingdom Hearts 358/2 Days*: un array de `struct Panel` con ranuras y funciones para equipar/desequipar.

### Bloque 0.3: Gestión Dinámica de Memoria y Punteros Avanzados
- [ ] **0.3.1** Reservar memoria para un array de 10 enteros con `malloc()` y comprobar si el puntero devuelto es `NULL`.
- [ ] **0.3.2** Inicializar memoria dinámica con `calloc()`, reescalar con `realloc()` y liberar con `free()`.
- [ ] **0.3.3** Compilar con `-fsanitize=address` para detectar un error provocado deliberadamente de *use-after-free*.
- [ ] **0.3.4** Punteros dobles: escribir una función `void asignar_memoria(int **ptr, int tamano)` que modifique el puntero del llamador.
- [ ] **0.3.5** Declarar y usar un puntero a función simple: `int (*operacion)(int, int)`.
- [ ] **0.3.6** Crear un array de punteros a funciones para implementar una tabla de despacho de comandos de juego (Atacar, Magia, Objeto).
- [ ] **0.3.7 (Micro-reto Gamer)**: Implementar un *Arena Allocator* simple (un buffer fijo de 1024 bytes del que se van extrayendo bloques con un offset continuo).

### Bloque 0.4: Manipulación de Bits, Endianness y Entrada/Salida Binaria
- [ ] **0.4.1** Incluir `<stdint.h>` y reemplazar tipos estándar por `uint8_t`, `uint16_t`, `uint32_t`, `int32_t`.
- [ ] **0.4.2** Definir macros de alias clásicos de consolas: `typedef uint8_t u8;`, `typedef uint16_t u16;`, `typedef uint32_t u32;`.
- [ ] **0.4.3** Operadores de bits: usar `&`, `|`, `^`, `~`, `<<`, `>>` para encender, apagar y consultar flags individuales en una variable `u8`.
- [ ] **0.4.4** Comprobar el endianness de la máquina actual leyendo un `uint32_t = 0x12345678` a través de un puntero `uint8_t *`.
- [ ] **0.4.5** Implementar `u16 swap16(u16 val)` y `u32 swap32(u32 val)` para conversión Little Endian / Big Endian.
- [ ] **0.4.6** Abrir un archivo binario en C usando `fopen("archivo.bin", "rb")` y leer sus primeros 16 bytes con `fread()`.
- [ ] **0.4.7** Usar `fseek()` y `ftell()` para calcular el tamaño total en bytes de un archivo binario.
- [ ] **0.4.8 (Proyecto Fin de Fase 0)**: Crear el programa `rom_parser`: leer la cabecera real de una ROM de Nintendo DS (bytes 0x00 a 0xC0) e imprimir el título, código de juego (ej. `YKGP`), tamaño de ROM y checksum.

---

## Fase 1 · Lectura y Anatomía de Decompilaciones Reales
> Guía detallada: [docs/temario/01-lectura-decompilaciones.md](temario/01-lectura-decompilaciones.md)

### Bloque 1.1: Ecosistema y Estructura de Proyectos
- [ ] **1.1.1** Clonar como referencia de lectura el repositorio `khdays-decomp` de Yokimitsuro en `fase-1-lectura-decomp/referencias/khdays-decomp`.
- [ ] **1.1.2** Inspeccionar el árbol de directorios del proyecto e identificar el propósito de: `src/`, `include/`, `asm/`, `config/`, `tools/`.
- [ ] **1.1.3** Abrir y estudiar un archivo linker script (`.ld`) para comprender cómo se asignan las secciones `.text`, `.data`, `.rodata` y `.bss` en la memoria de la consola.
- [ ] **1.1.4** Buscar una dirección de función en el archivo de símbolos (`syms.txt`) y rastrear su código C correspondiente.

### Bloque 1.2: Hardware de Nintendo DS para Lectores de C
- [ ] **1.2.1** Leer el resumen de arquitectura de Nintendo DS en GBATEK: procesador ARM946E-S vs ARM7TDMI.
- [ ] **1.2.2** Localizar en los headers de NitroSDK cómo están declarados los registros MMIO para leer el estado de los botones (`REG_KEYINPUT`).
- [ ] **1.2.3** Entender qué es un *Overlay* de Nintendo DS: examinar la tabla de overlays (`ov000`, `ov002`, `ov006`) en `khdays-decomp`.

### Bloque 1.3: Lectura Guiada de Código de Kingdom Hearts Days
- [ ] **1.3.1** Abrir el overlay `ov000` (pantalla de logos de inicio) y seguir la secuencia de inicialización.
- [ ] **1.3.2** Localizar la función `BootTask_Construct` y entender cómo se inicializa la máquina de estados.
- [ ] **1.3.3** Localizar el overlay `ov006` (pantalla de selección de personajes) y examinar el array de los 13 miembros de la Organización XIII.
- [ ] **1.3.4 (Hito de Validación de Fase 1)**: Redactar en `fase-1-lectura-decomp/analisis/` un informe técnico en Markdown explicando paso a paso la estructura de datos y el flujo de una escena real del juego.

---

## Fase 2 · Matching Decompilation (El Arte del 100% Match)
> Guía detallada: [docs/temario/02-matching-decompilation.md](temario/02-matching-decompilation.md)

### Bloque 2.1: Ensamblador ARMv5TE y Calling Conventions
- [ ] **2.1.1** Familiarizarse con los registros de la CPU ARM: de `r0` a `r12` (propósito general), `sp` (`r13`), `lr` (`r14`), `pc` (`r15`).
- [ ] **2.1.2** Comprender el registro `CPSR` y cómo las instrucciones con sufijo condicional (`ADDEQ`, `SUBNE`, `BGT`) evitan saltos en ARM.
- [ ] **2.1.3** Estudiar la convención AAPCS: los primeros 4 argumentos entran en `r0`-`r3`, los retornos en `r0`, y `r4`-`r11` se preservan en el stack.

### Bloque 2.2: Cadena de Herramientas de Matching
- [ ] **2.2.1** Entrenar heurísticas de optimización en **Decomp Academy** (orden de declaración de variables, peephole optimizations y alineación de stack).
- [ ] **2.2.2** Crear una cuenta en **decomp.me** y explorar un scratch público de Nintendo DS o GBA.
- [ ] **2.2.3** Descargar y configurar **objdiff** en Linux para comparar archivos de objeto compilados localmente (`.o`).
- [ ] **2.2.4** Interpretar la salida del diff: diferencias en registros (amarillo), diferencias en instrucciones (rojo/verde) y desplazamientos en el stack.

### Bloque 2.3: Técnicas de Matching y Primer 100% Match
- [ ] **2.3.1** Crear un scratch propio en decomp.me con una función sencilla de biblioteca o lógica matemática de GBA/NDS.
- [ ] **2.3.2** Resolver discrepancias de registros reordenando la declaración de variables locales en C.
- [ ] **2.3.3** Resolver diferencias de bucles probando equivalencias entre `while`, `for` y `do-while`.
- [ ] **2.3.4 (Hito de Validación de Fase 2)**: Conseguir un **100% MATCH** verificado en una función real no trivial y registrar el resultado en `fase-2-matching-decomp/matches/`.

---

## Fase 3 · Librerías Gráficas y Multimedia con SDL
> Guía detallada: [docs/temario/03-graficos-multimedia-sdl.md](temario/03-graficos-multimedia-sdl.md)

### Bloque 3.1: Creación del Runtime Gráfico
- [ ] **3.1.1** Instalar librerías de desarrollo SDL en Linux (`libsdl2-dev` o `libsdl3-dev`).
- [ ] **3.1.2** Escribir un programa básico en C que inicialice SDL, abra una ventana de 800×600 y maneje el evento de cierre.
- [ ] **3.1.3** Implementar un bucle de juego (*Game Loop*) con control estricto de tiempo fijado a 60 FPS usando `SDL_GetTicks()`.

### Bloque 3.2: Framebuffer Retro y Renderizado 2D
- [ ] **3.2.1** Crear una textura SDL de streaming con formato `SDL_PIXELFORMAT_RGBA8888` y resolución nativa de DS (256×192 píxeles).
- [ ] **3.2.2** Implementar una función `void put_pixel(u32 *buffer, int x, int y, u32 color)` y pintar un degradado directamente en memoria.
- [ ] **3.2.3** Renderizar dos framebuffers simulando las pantallas superior e inferior de Nintendo DS en una sola ventana.

### Bloque 3.3: Entrada, Audio e Integración de Dear ImGui
- [ ] **3.3.1** Mapear teclas del teclado a los botones virtuales de Nintendo DS (Cruz direccional, A, B, X, Y, L, R, Start, Select).
- [ ] **3.3.2** Configurar un callback de audio en SDL y reproducir un tono senoidal o muestra PCM.
- [ ] **3.3.3** Integrar Dear ImGui en el proyecto SDL para mostrar una ventana flotante con los FPS y selector de opciones.
- [ ] **3.3.4 (Hito de Validación de Fase 3)**: Construir el `mini-visor-kh`: una aplicación que cargue una textura del juego original y permita mover la cámara con teclado/mando.

---

## Fase 4 · Source Ports Nativos a PC (Kingdom Hearts 358/2 Days)
> Guía detallada: [docs/temario/04-ports-nativos-a-pc.md](temario/04-ports-nativos-a-pc.md)

### Bloque 4.1: Arquitectura y Compilación del Port de PC
- [ ] **4.1.1** Clonar y revisar el repositorio `khdays-port` de Yokimitsuro en `fase-4-pc-port/port-source`.
- [ ] **4.1.2** Configurar el entorno de compilación de `khdays-port` en Linux con CMake y Ninja/Make.
- [ ] **4.1.3** Extraer los assets legales de una copia del juego usando los scripts del repositorio.
- [ ] **4.1.4** Compilar y ejecutar la demo interactiva de Twilight Town (`khdays-port --playable-demo`).

### Bloque 4.2: Comprensión del Código del Port
- [ ] **4.2.1** Analizar el subsistema `khdays::vfs`: cómo traduce peticiones de archivos NitroFS a la carpeta de assets de PC.
- [ ] **4.2.2** Analizar el módulo `khdays::game`: cómo reproduce el frame loop original y la máquina de estados de Roxas.
- [ ] **4.2.3** Analizar el menú de opciones de Dear ImGui ya integrado en el port.

### Bloque 4.3: Modding y Creación de Mejoras Propias
- [ ] **4.3.1** Modificar un asset 2D o textura de UI reemplazándola con un archivo PNG de alta resolución mediante el sistema de mods drop-in.
- [ ] **4.3.2** Modificar una variable del juego en código nativo (velocidad de movimiento de Roxas o cámara libre).
- [ ] **4.3.3** Añadir una opción personalizada en el menú de Dear ImGui del port (ej. selector de resolución o invencibilidad de depuración).
- [ ] **4.3.4 (Hito Final del Reto de 358/2 Días)**: Exportar la tarjeta final del Día 358/2 en `khdays-card`, publicando el video/capturas de tu propia modificación corriendo en el port nativo de PC.
