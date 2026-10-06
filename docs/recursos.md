# Catálogo de Recursos y Referencias Técnicas

Este documento reúne todas las fuentes oficiales, documentación de hardware, libros y herramientas que utilizaremos a lo largo del reto de 358/2 días.

---

## 1. Lenguaje C y Arquitectura de Memoria (Fase 0)

### Libros y Guías de Referencia
- **[Guía de Beej para la Programación en C (Versión en Español)](https://stefanogassmann.github.io/BGCSpanish/)**:
  - Tu texto de cabecera actual para la sintaxis de C. Consúltalo como manual de referencia para las estructuras básicas y funciones estándar.
- **[The C Programming Language (K&R, 2ª Edición)](https://en.wikipedia.org/wiki/The_C_Programming_Language)**:
  - El clásico fundacional de Brian Kernighan y Dennis Ritchie. Esencial para comprender la filosofía minimalista de C y los punteros directos.
- **[Modern C (Jens Gustedt)](https://modernc.gforge.inria.fr/)**:
  - Referencia avanzada para estándares C99, C11, modelos de memoria, tipos exactos `<stdint.h>` y disciplina de memoria.

### Herramientas de Inspección de Código
- **[Compiler Explorer (Godbolt)](https://godbolt.org/)**:
  - Herramienta indispensable para ver qué código máquina genera cada línea de C con compiladores como `ARM gcc` o `MIPS gcc`.
- **[Valgrind](https://valgrind.org/) / AddressSanitizer (`-fsanitize=address`)**:
  - Detección de fugas de memoria, accesos fuera de rango (*out-of-bounds*) y punteros colgantes (*dangling pointers*).

---

## 2. Hardware y Decompilación de Nintendo DS y GBA (Fases 1 y 2)

### Documentación de Hardware Oficial / Comunitario
- **[GBATEK — Gameboy Advance & Nintendo DS Technical Info (Martin Korth)](https://problemkaputt.de/gbatek.htm)**:
  - La "Biblia" definitiva de bajo nivel para GBA y NDS. Detalla los mapas de memoria física, registros MMIO (`REG_DISPCNT`, `REG_KEYINPUT`), DMA, formatos de pantalla 2D y 3D, y timing.
- **[ARM Architecture Reference Manual (ARMv5TE)](https://developer.arm.com/)**:
  - Manual de referencia oficial de instrucciones para el procesador ARM946E-S de Nintendo DS.
- **[ARM Architecture Procedure Call Standard (AAPCS)](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst)**:
  - La convención oficial de llamadas: cómo se pasan argumentos (`r0`–`r3`), cómo se devuelve memoria y qué registros deben salvarse en el stack.

### Filosofía y Plataformas de Decompilación
- **[decomp.dev](https://decomp.dev/)**:
  - Portal y manifiesto de la comunidad de decompilaciones matching. Explica las mejores prácticas, estructuras de repositorios y métricas de progreso.
- **[decomp.me](https://decomp.me/)**:
  - Plataforma colaborativa en línea para decompilar funciones individuales en tiempo real con diff interactivo.
- **[objdiff (GitHub)](https://github.com/encounter/objdiff)**:
  - Aplicación local moderna para comparar byte a byte archivos de objeto compilados (`.o`) contra los originales.
- **[m2c (mips-to-c)](https://github.com/matt-kempster/m2c)**:
  - Generador automático de pseudo-C a partir de ensamblador desensamblado.

### Repositorios de Referencia
- **[khdays-decomp (Yokimitsuro)](https://github.com/Yokimitsuro/khdays-decomp)**:
  - Decompilación 1:1 de *Kingdom Hearts 358/2 Days* (Nintendo DS). Compilador: MetroWerks CodeWarrior `mwccarm` 3.0 build 139.
- **[khcom (Pheenoh)](https://github.com/Pheenoh/khcom)**:
  - Decompilación de *Kingdom Hearts: Chain of Memories* (Game Boy Advance).
- **[zeldaret/mm](https://github.com/zeldaret/mm)**:
  - Decompilación completa de *The Legend of Zelda: Majora's Mask* (Nintendo 64).

---

## 3. Librerías Gráficas, Audio y Source Ports (Fases 3 y 4)

### Librerías Gráficas y Multimedia
- **[Documentación Oficial de SDL3 / SDL2 (Simple DirectMedia Layer)](https://wiki.libsdl.org/)**:
  - La librería multiplataforma estándar para crear ventanas, framebuffers, reproducir audio y manejar mandos de juego en PC.
- **[Lazy Foo' Productions — Beginning Game Programming v2.0 (SDL2)](https://lazyfoo.net/tutorials/SDL/)**:
  - El tutorial clásico paso a paso para dominar renderers, texturas y timing en SDL.
- **[Dear ImGui (ocornut/imgui)](https://github.com/ocornut/imgui)**:
  - Librería de interfaz gráfica inmediata para C/C++ usada para construir consolas de desarrollo, inspectores de memoria y menús de opciones en source ports.

### Source Ports de Nintendo DS a PC
- **[khdays-port (Yokimitsuro)](https://github.com/Yokimitsuro/khdays-port)**:
  - Runtime nativo experimental de *Kingdom Hearts 358/2 Days* para PC. Desarrollado en C++ / SDL3 con renderizado GPU y carga de assets NitroFS.
