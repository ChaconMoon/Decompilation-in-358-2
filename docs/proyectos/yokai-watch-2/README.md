# Proyecto Objetivo: Yo-kai Watch 2: Mentespectros (Nintendo 3DS)

**Juego**: *Yo-kai Watch 2: Mentespectros* (*Shin'uchi* / *Psychic Specters*)  
**Desarrollador**: Level-5  
**Plataforma**: Nintendo 3DS (CTR)  
**Arquitectura de CPU**: **ARM11 MPCore (ARMv6K)** a 268 MHz (doble núcleo principal)  
**Coprocesador**: ARM946E-S (Seguridad / Procesador de Entrada/Salida del Sistema)  
**Meta pública**: Documentación y decompilación matching progresiva en [decomp.dev](https://decomp.dev/) y scratches en [decomp.me](https://decomp.me/).

---

## 1. Justificación Pedagógica y Estrategia Dual

En el reto de **358/2 Días**, este proyecto se integra como el **gran objetivo independiente (Capstone)** de Carlos:

| Eje | `khdays-decomp` (NDS) | *Yo-kai Watch 2* (3DS) |
| :--- | :--- | :--- |
| **Rol** | **Laboratorio guiado de referencia** | **Proyecto independiente de investigación** |
| **Arquitectura** | ARM946E-S (ARMv5TE, 67 MHz) | ARM11 MPCore (ARMv6K, 268 MHz) |
| **Calling Convention** | AAPCS (`r0-r3`, ret `r0`, `r4-r11` preserved) | AAPCS (`r0-r3`, ret `r0`, `r4-r11` preserved) |
| **Compilador Probable** | CodeWarrior `mwccarm 3.0` | ARM Compiler (RVCT 4.x / `armcc` / `armclang`) |
| **Estado en la Scene** | Proyecto maduro con tooling (`dsd`, `splat`) | Terreno pionero en decompilación 3DS |

> **Principio Clave**: La convención de llamada de registros (AAPCS), el layout de memoria (Stack, Heap, `.text`, `.rodata`), la alineación de structs y la manipulación de punteros son **100% transferibles**. Lo que aprendemos en C y en NDS se aplica directamente a 3DS.

---

## 2. Anatomía de una ROM de 3DS y Pipeline de Extracción

Cuando se dumpea una copia legal de la consola mediante **GodMode9**, la estructura interna se desglosa así:

```
[ Cartucho físico / Dump .3ds o .cia ]
                  │
                  ▼ (Extracción con ctrtool / GodMode9)
         ┌────────┴────────┐
         ▼                 ▼
   [ ExeFS ]            [ RomFS ]
 (Ejecutable)        (Assets: modelos, textos, .fa)
         │
    ┌────┴──────────────────────────┐
    ▼                               ▼
code.bin (Binario ARM11)       exheader.bin (Permisos, memoria, stack)
    │
    ▼ (Descompresión LZSS/BLZ si aplica)
code.bin (descomprimido)
    │
    ├─► 1. Análisis de Cadenas (.rodata) y Símbolos en Ghidra / IDA
    ├─► 2. Identificación del compilador (armcc vs gcc) y banderas de optimización
    └─► 3. Scratches interactivos en decomp.me
```

---

## 3. Hoja de Ruta de Ingeniería Inversa (3DS)

1. **Recepción del Dump Legal**:
   - Obtener el volcado del juego propio (preferiblemente `code.bin` y `exheader.bin` ya extraídos con GodMode9, o la ROM `.3ds`/`.cia`).
2. **Extracción y Descompresión del Ejecutable**:
   - En Nintendo 3DS, el archivo `code.bin` dentro de ExeFS suele estar comprimido con LZSS/BLZ invertido (Nintendo Extended LZSS).
   - Descomprimir el binario para obtener el código máquina puro en texto plano.
3. **Análisis Estático Inicial (Ghidra / IDA Pro)**:
   - Configurar la arquitectura base: **ARM v6T2 / ARMv6K (32-bit little endian)**.
   - Base address típica de carga para aplicaciones de usuario en 3DS: `0x00100000`.
   - Localizar el punto de entrada (*Entry Point*) y las rutinas de inicialización de CTR-SDK.
4. **Identificación de Funciones Candidatas**:
   - Funciones matemáticas simples (trigonometría, cálculo de daño, estadísticas de Yo-kai).
   - Rutinas de manipulación de cadenas de texto y búsqueda de IDs en inventarios.
5. **Primer Scratch en decomp.me**:
   - Subir el ensamblador de una función seleccionada a [decomp.me](https://decomp.me/) y reproducir la lógica en C buscando el byte-match exacto.

---

## 4. Política de Protección Legal
- **Nunca se incluirán binarios protegidos por derechos de autor en el repositorio de Git**.
- Todos los scripts y tooling requerirán que el usuario aporte sus propios archivos extraídos de su consola legítima.
