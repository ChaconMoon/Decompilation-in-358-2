# Contexto del Proyecto: KHDays – 358,5 Días de Decompilación

---

## 👤 Perfil del Estudiante
- **Nombre**: Carlos.
- **Rol profesional**: Instructor de Formación Profesional (FP) de Programación e Informática en España.
- **Idiomas**: Español e Inglés.
- **Nivel en C**: Básico, con experiencia previa trasteando en homebrew de Nintendo 3DS, Wii y Nintendo Switch.
- **Entorno de trabajo**: VS Code en Linux (Ubuntu/Debian) para código y ejercicios en C. Notas, conceptos y bitácora estructurados en **Obsidian**.
- **Preferencia pedagógica**: Énfasis profundo en el **"por qué"** (arquitectura de CPU, layout de memoria, convenciones de llamada), nunca limitarse a soluciones para copiar/pegar.

---

## 🏛️ Repositorios Base

### 1. `Yokimitsuro/khdays-decomp`
- Decompilación *matching* (byte-exact 100%) de *Kingdom Hearts 358/2 Days* (Nintendo DS).
- **Herramientas de compilación**: `dsd`, compilador original CodeWarrior `mwccarm 3.0 build 139`.
- **Tooling de análisis**: Python (`capstone`, `pyelftools`, `ndspy`).
- **Estructura clave**:
  - `src/auto/`: código autogenerado/delinkeado.
  - `src/calls/`: tablas y llamadas del motor.
  - `src/asm_stubs/`: stubs y funciones aún en ensamblador puro.
  - `config/arm9/`: configuración de memoria y mapas de la CPU principal.
  - `sdk/`: implementaciones y headers de NitroSDK.

### 2. `Yokimitsuro/khdays-port`
- Runtime nativo experimental para PC escrito en **C++20, SDL3 y Vulkan**.
- **Arquitectura de capas**:
  - Importadores de assets de Nintendo DS (NitroFS, modelos, texturas, sonido).
  - Capa de recursos neutral y agnóstica de plataforma.
  - Motor del juego.
- **Submódulo Git**: Consume `khdays-decomp` como submódulo fijado a un commit/revisión concreta.
- **Plataformas de destino**:
  - `platform/pc/`: Runtime nativo para Linux/Windows.
  - `platform/3ds`: Port específico para Nintendo 3DS (homebrew).

### 3. Proyecto Objetivo de Formación: *Yo-kai Watch 2: Mentespectros* (Nintendo 3DS)
- **Desarrollador / Plataforma**: Level-5 / Nintendo 3DS (arquitectura **ARM11 MPCore / ARMv6K**).
- **Rol en el reto**: Proyecto propio e independiente de Carlos para aprender y aplicar ingeniería inversa y decompilación real.
- **Canales de publicación previstos**: Plataforma colaborativa [decomp.dev](https://decomp.dev/) y scratches interactivos en [decomp.me](https://decomp.me/).
- **Ecosistema técnico**:
  - Formato contenedor: ROM legítima dumpeada por el usuario (`.3ds` / `.cia` / ExeFS).
  - Binario ejecutable: `code.bin` (descomprimido de ExeFS) y cabecera de extensión `exheader.bin`.
  - Herramientas de análisis: Ghidra / IDA Pro / Capstone (ARMv6K), `ctrtool`, scripts Python para desempaquetado de formatos de Level-5.
  - Sinergia pedagógica: `khdays-decomp` (NDS) actúa como el laboratorio guiado y maduro de referencia, mientras que *Yo-kai Watch 2* es el proyecto pionero donde Carlos aplica de forma práctica cada lección.

---

## 🎯 Objetivos del Reto

1. **Aprender decompilación de videojuegos y matching de código**: empezar por lo elemental (decomp.me, funciones de NitroSDK).
2. **Dominar C a bajo nivel**: memoria física, alineación, punteros, structs, manipulación de bits y ensamblador ARM.
3. **Documentar con rigor**: aprender a documentar repositorios de decompilación, bitácoras y Architecture Decision Records (ADRs).
4. **Desarrollar un wrapper de render con SDL y un port mantenible**: desacoplar el hardware de la consola original de la capa de render moderna.
5. **Meta simbólica**: 358,5 días de dedicación constante.
   - **Inicio oficial**: 27 de Septiembre de 2026 (Día 1).
   - **Fin aproximado**: 21 de Septiembre de 2027.
6. **Motivación y divulgación continua**: progreso visible día a día mediante `#Decompilando358`, tarjetas visuales de progreso e informes de aprendizaje.

---

## 🗺️ Hoja de Ruta en Fases

- **Fase 0**: Cimientos de C y conceptos de ingeniería inversa (*matching*, *delink*, relocación, por qué importa el compilador original `mwccarm`).
- **Fase 1**: Proyecto simple de decompilación (*decomp.me* + funciones sencillas de NitroSDK en `sdk/`).
- **Fase 2**: Comprensión profunda de la arquitectura de `khdays-decomp`.
- **Fase 3**: Documentación como oficio (técnicas de documentación técnica e ingeniería inversa).
- **Fase 4**: `khdays-port`, wrapper de render con SDL3 y diseño de software mantenible.
- **Fase 5+**: Iteración continua entre decompilación y el port nativo.

---

## 📅 Línea de Tiempo y Progreso Acumulado

- **Día 1 (27/09/2026)**: Inicio oficial del reto de 358,5 días.
- **Día 2 (28/09/2026)**: Lectura de la *Guía de Beej para C* (caps. 1–4, hasta la pág. 30). Tabla de equivalencias de control de flujo Python → C.
- **Día 4 (30/09/2026)**: Publicación en LinkedIn con el hashtag **#Decompilando358**. Diseño del concepto de tarjetas de avance diario inspiradas en la pantalla de días de *Kingdom Hearts 358/2 Days*.
- **Día 5 (01/10/2026)**: Estudio de los capítulos 1–6 de Beej (punteros, arrays, memoria, pág. ~60). Planteamiento del proyecto de dificultad media-alta `p3-runlog`.
- **Punto de inflexión**: Se intentó abordar la primera función real de `khdays-decomp`, pero el salto técnico resultó abrupto. Decisión acertada: afianzar primero los cimientos de C y memoria a bajo nivel antes de decompilar en ARM.
- **Día 7 (03/10/2026)**: Experimentación en el port para 3DS (`platform/3ds`). La escena de ejemplo funciona. Objetivos pendientes en 3DS:
  - Carga y reproducción de cinemáticas (MODS / MobiClip).
  - Quitar el cartel de "DEMO UNAVAILABLE" en el gameplay.
  - Relación de aspecto 4:3 en pantalla superior (estilo DS) con barras laterales blancas sin estirar.
  - Optimización del render por software (framerate y nitidez).
- **Día 10 (06/10/2026)**: Proyecto `p3-runlog`:
  - Implementación de intercambio de filas por puntero (`swap_rows` con `change_pointers`).
  - Ordenamiento de matrices 2D por mejor tiempo acoplando misión y registro.
  - Blindaje ante intentos no jugados (`-1`) en `best_mision` y `calculate_ranking`.
  - Compilación limpia con `gcc -Wall -Wextra -Werror`.
  - Creación del sistema de diario de aprendizaje diario en `docs/diario/`.

---

## 🤝 Reglas de Oro de Acompañamiento (Para el Tutor / IA)

1. **Pedagogía Activa**: No hacer el trabajo por el estudiante. Guiar, formular preguntas reflexivas y explicar con claridad el razonamiento y la memoria.
2. **Protección Legal y Ética**: **No reproducir código fuente real del juego con copyright**. Tanto `khdays-decomp` como `khdays-port` exigen legalmente una copia legítima de la ROM de Nintendo DS aportada por el usuario.
3. **Honestidad y División de Tareas**: Si una meta o función es excesivamente compleja, avisar con total franqueza y ayudar a trocearla en micro-objetivos atómicos de 15–45 min.
4. **Mantenimiento Documental**:
   - Bitácora de aprendizaje diaria en `docs/diario/dia-XX.md`.
   - Glosario de términos de bajo nivel.
   - Notas de matching decompilation.
   - ADRs (*Architectural Decision Records*) concisos para las decisiones de arquitectura del port y el wrapper SDL.
