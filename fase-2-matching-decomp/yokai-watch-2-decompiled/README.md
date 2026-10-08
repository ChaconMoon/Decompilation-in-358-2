# Yo-kai Watch 2: Mentespectros — Matching Decompilation (Nintendo 3DS)

**Juego**: *Yo-kai Watch 2: Mentespectros* (*Shin'uchi* / *Psychic Specters*)  
**Desarrollador**: Level-5  
**Plataforma**: Nintendo 3DS (CTR)  
**Title ID**: `00040000001B2900` (Edición Europea)  
**Arquitectura de CPU**: **ARM11 MPCore (ARMv6K)** @ 268 MHz (32-bit Little Endian)  
**Coprocesador**: ARM946E-S (Seguridad / OS IO)  
**Objetivo**: Decompilación matching byte-exact en C/C++ y publicación comunitaria en [decomp.dev](https://decomp.dev/) y [decomp.me](https://decomp.me/).

---

## 1. Estructura del Proyecto

```text
yokai-watch-2-decompiled/
├── Makefile              # Orquestador de compilación, extracción y tests
├── .gitignore            # Protección estricta de ROMs y binarios con copyright
├── README.md             # Esta documentación técnica
├── config/               # Configuración de memoria, linker scripts y símbolos
│   └── symbols.txt       # Tabla de símbolos conocidos y direcciones de funciones
├── tools/                # Scripts de soporte y descompresión
│   └── extract_rom.py    # Extractor de NCSD/NCCH, ExeFS y descompresor LZSS
├── asm/                  # Ensamblador de funciones pendientes de decompilar (.s)
├── src/                  # Código fuente en C decompilado 100% matching
├── include/              # Tipos base de CTR-SDK y estructuras del motor de Level-5
├── scratches/            # Registro de scratches creados en decomp.me
└── extracted/            # [Ignorado en Git] Binarios extraídos de la ROM legal
    ├── exheader.bin
    ├── code.bin          # Comprimido original de ExeFS
    └── code.raw.bin      # Ejecutable plano descompromido ARM11 (@ 0x00100000)
```

---

## 2. Flujo de Trabajo (Pipeline)

### Paso 1: Extracción del Ejecutable Legal
Coloca tu copia legal dumpeada en esta carpeta (ej. `00040000001B2900_v00.3ds`) y ejecuta:
```bash
make extract
```
Esto:
1. Extrae la partición 0 (NCCH de la aplicación).
2. Extrae `exheader.bin` y `exefs/code.bin`.
3. Descomprime el ejecutable Nintendo Extended LZSS a `extracted/code.raw.bin`.
4. Muestra y valida el hash SHA-256 de referencia.

### Paso 2: Análisis Estático y Scratches en decomp.me
1. Inspecciona `extracted/code.raw.bin` en Ghidra cargándolo como **ARMv6T2 / ARMv6K (32-bit Little Endian)** con dirección base `0x00100000`.
2. Identifica funciones aisladas (cálculo de daño, tablas de Yo-kai).
3. Sube la función a [decomp.me](https://decomp.me/) y experimenta con C hasta conseguir el match.
4. Traslada el código C verificado a `src/`.

---

## 3. Política Legal y Ética
Este repositorio **nunca contiene código comercial ni activos protegidos por derechos de autor**. Todo el flujo de compilación y matching requiere que el usuario aporte su propia copia legítima del juego dumpeada de su consola Nintendo 3DS personal.
