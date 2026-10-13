# Diccionario de Ensamblador ARM a C: GBA · NDS · 3DS · Switch

Guía técnica y de referencia para matching decompilation en las cuatro generaciones portátiles e híbridas de Nintendo:
- **Game Boy Advance (GBA)**: CPU ARM7TDMI (`ARMv4T`, 32-bit / Thumb 16-bit), compilador `agbcc`.
- **Nintendo DS (NDS)**: CPU ARM946E-S (`ARMv5TE`, 32-bit / Thumb + DSP), compilador MetroWerks CodeWarrior `mwccarm 3.0 build 139`.
- **Nintendo 3DS (3DS)**: CPU ARM11 MPCore (`ARMv6K`, 32-bit + VFPv2), compiladores Nintendo CTR SDK `armcc` y devkitARM `gcc`.
- **Nintendo Switch (Switch)**: CPU Nvidia Tegra X1 Cortex-A57 (`ARMv8-A AArch64`, 64-bit puro + NEON), compiladores Nintendo SDK `clang` / LLVM y `aarch64-none-elf-gcc`.

---

## 0. Matriz Comparativa de Arquitecturas ARM en Nintendo

| Característica | Game Boy Advance (GBA) | Nintendo DS (NDS) | Nintendo 3DS (3DS) | Nintendo Switch (Switch) |
| :--- | :--- | :--- | :--- | :--- |
| **CPU Principal** | ARM7TDMI (16.78 MHz) | ARM946E-S (67.03 MHz) | ARM11 MPCore (268 / 804 MHz) | 4x Cortex-A57 (1.02 GHz) |
| **Arquitectura** | **ARMv4T** (32-bit) | **ARMv5TE** (32-bit) | **ARMv6K** (32-bit) | **ARMv8-A / AArch64** (64-bit) |
| **Modos de Instrucción** | ARM32, Thumb-1 (16-bit) | ARM32, Thumb-1, DSP-E | ARM32, Thumb-1/2, SIMD v6 | **A64** (32-bit longitud fija, 64-bit ops) |
| **Compilador Histórico** | `agbcc` (GCC 2.95.2) | CodeWarrior `mwccarm 3.0` | ARM RealView `armcc` / `gcc` | **Nintendo SDK Clang / LLVM** |
| **Coma Flotante (`float`)** | Soft-float / Punto fijo | Soft-float / BIOS | **VFPv2 Hardware** (`s0`–`s31`) | **NEON / VFPv4 Hardware** (`v0`–`v31`) |
| **División (`/` y `%`)** | BIOS SWI `0x06` / Software | **Hardware MMIO** (`CP_SetDiv`) | Software / Runtime CRT | **Hardware Nativo** (`sdiv`, `udiv`) |
| **Carga Constantes 32/64b** | Literal Pools (`[pc, #imm]`) | Literal Pools (`[pc, #imm]`) | `movw` + `movt` / Pools | **`movz` + `movk`**, o **`adrp` + `add`** |
| **Paso de Argumentos** | Primeros 4 en `r0`–`r3` | Primeros 4 en `r0`–`r3` | Primeros 4 en `r0`–`r3` | **Primeros 8 en `x0`–`x7`** |
| **Retorno de Función** | `bx lr` / `pop {r3}; bx r3` | `pop {..., pc}` / `bx lr` | `pop {..., pc}` / `bx lr` | **`ret`** (retorna usando `x30`) |
| **Acceso a Memoria Doble** | `ldmia` / `stmia` | `ldmia` / `stmia` | `ldmia` / `stmia` | **`ldp` / `stp`** (Load/Store Pair) |
| **Registro CERO Hardware** | No (requiere registro) | No (requiere registro) | No (requiere registro) | **`xzr` (64-bit) / `wzr` (32-bit)** |

---

## 1. Registros de la CPU y Convenciones de Llamada

### A. Consolas de 32 bits (GBA, NDS y 3DS - Convención AAPCS32):
Existen 16 registros enteros (`r0`–`r15`):

| Registro | Nombre AAPCS | Propósito en C | Preservación | Comportamiento |
| :--- | :--- | :--- | :--- | :--- |
| **`r0`** | `a1` | **Argumento 1** / **Retorno de función** | *Caller-saved* (volátil) | En GBA/DS devuelve también `float` en soft-float. |
| **`r1`** | `a2` | **Argumento 2** / Parte alta de retorno 64-bit | *Caller-saved* (volátil) | Parte alta de `u64`, `s64` o `double` soft-float. |
| **`r2`** | `a3` | **Argumento 3** | *Caller-saved* (volátil) | Parámetro 3 de funciones. |
| **`r3`** | `a4` | **Argumento 4** | *Caller-saved* (volátil) | Parámetro 4 (argumentos 5+ van a la pila). |
| **`r4`–`r11`**| `v1`–`v8` | **Variables locales persistentes** | **Callee-saved** | Guardadas en prólogo (`push`). CodeWarrior las asigna según orden de declaración. |
| **`r12`** | `ip` | *Intra-procedure scratch* | *Caller-saved* (volátil) | Usado por el enlazador en llamadas lejanas (*trampolines*). |
| **`r13`** | `sp` | **Stack Pointer** (puntero de pila) | Preservado | Alineado a 4 bytes (GBA) u 8 bytes (NDS/3DS AAPCS). |
| **`r14`** | `lr` | **Link Register** (dirección de retorno) | Preservado si no es leaf| Almacena la dirección a la que volver tras `bl`/`blx`. |
| **`r15`** | `pc` | **Program Counter** | - | Apunta a la instrucción en ejecución + offset de pipeline. |

---

### B. Nintendo Switch (64 bits - Convención AAPCS64 / AArch64):
Switch utiliza la arquitectura **AArch64**. Cada registro de propósito general puede leerse como palabra completa de 64 bits (`x0`–`x30`) o como sus 32 bits inferiores (`w0`–`w30`):

| Registro (64-bit) | Vista 32-bit | Propósito en C (Switch) | Preservación |
| :--- | :--- | :--- | :--- |
| **`x0`** | `w0` | **Argumento 1** de entrada / **Valor de retorno principal** | *Caller-saved* (volátil) |
| **`x1`–`x7`** | `w1`–`w7` | **Argumentos 2 al 8** de entrada (¡hasta 8 parámetros en registros!) | *Caller-saved* (volátil) |
| **`x8`** | `w8` | **Indirect Result**: puntero para retornar `structs` grandes (> 16 bytes) | *Caller-saved* (volátil) |
| **`x9`–`x15`** | `w9`–`w15` | **Variables temporales de scratch** | *Caller-saved* (volátil) |
| **`x16`–`x17`**| `w16`–`w17` | Intra-procedure scratch (`IP0`/`IP1`), usado en tablas PLT/dinámicas | *Caller-saved* (volátil) |
| **`x18`** | `w18` | Registro reservado por la plataforma (Horizon OS) | Reservado |
| **`x19`–`x28`**| `w19`–`w28` | **Variables locales persistentes** | **Callee-saved** (debe preservarse en stack) |
| **`x29`** | `w29` | **Frame Pointer (`FP`)** (cadena de marcos en pila) | **Callee-saved** |
| **`x30`** | `w30` | **Link Register (`LR`)** (dirección de retorno tras llamada `bl`) | **Callee-saved** si llama a otras |
| **`sp`** | `wsp` | **Stack Pointer** (debe estar **estrictamente alineado a 16 bytes**) | Preservado |
| **`xzr`** | **`wzr`** | **Zero Register**: constante `0` por hardware (lectura = 0, escritura = descarta) | Hardware |

---

### C. Registros de Coma Flotante y SIMD (3DS vs Switch):
- **Nintendo 3DS (VFPv2)**:
  - 32 registros `float` de 32 bits: `s0`–`s31`.
  - Agrupables en 16 registros `double` de 64 bits: `d0`–`d15`.
  - `s0` devuelve el resultado flotante; `s16`–`s31` son callee-saved.
- **Nintendo Switch (NEON / Advanced SIMD)**:
  - 32 registros vectoriales de 128 bits: **`v0`–`v31`**.
  - Vistas escalares:
    - `b0`–`b31`: 8 bits.
    - `h0`–`h31`: 16 bits (*half-precision float*).
    - `s0`–`s31`: 32 bits (*single-precision float*).
    - `d0`–`d31`: 64 bits (*double-precision float*).
    - `q0`–`q31`: 128 bits (*vector quadword*).
  - **Convención en Switch**: `v0`–`v7` pasan hasta 8 argumentos flotantes y devuelven el resultado; solo los 64 bits inferiores de `v8`–`v15` (`d8`–`d15`) son *callee-saved*.

---

## 2. Movimiento de Datos y Carga de Constantes

| Patrón en Ensamblador | Plataforma | Equivalente en C | Explicación Técnica |
| :--- | :--- | :--- | :--- |
| `mov r0, #42` | GBA / NDS / 3DS | `a = 42;` | Inmediato pequeño en ARM32. |
| `mov w0, #42`<br>`mov x0, #42` | **Switch** | `a = 42;` | Inmediato de 32 o 64 bits en ARM64. |
| `mvn r0, r1`<br>`mvn w0, w1` | Todas | `a = ~b;` | *Move Negative*: complementario a 1 bit a bit. |
| `ldr r0, [pc, #offset]`<br>*(Literal Pool)* | **GBA / NDS** *(y 3DS)* | `a = 0x12345678;`<br>o `ptr = &g_Var;` | **Obligatorio en GBA y NDS**: Carga desde la piscina de literales contigua en memoria. |
| `movw r0, #0x5678`<br>`movt r0, #0x1234` | **Solo 3DS** | `a = 0x12345678;` | Carga inmediata de 32 bits en 2 instrucciones sin literal pools. |
| `movz x0, #0x5678, lsl #0`<br>`movk x0, #0x1234, lsl #16` | **Solo Switch** | `a = 0x12345678;` | ARM64: *Move Zero* (pone a 0 el resto) + *Move Keep* (inserta en los bits indicados). |
| `adrp x0, g_Var`<br>`add  x0, x0, :lo12:g_Var` | **Solo Switch** | `ptr = &g_Var;` | **Direccionamiento PC-Relativo de Switch**: calcula la página de 4KB (`adrp`) y suma el offset inferior (`:lo12:`). Clave para el ASLR de Horizon OS. |
| `mov x0, xzr` | **Solo Switch** | `a = 0;` | Carga cero instantáneamente usando el Zero Register sin consumir memoria. |

---

## 3. Operaciones Aritméticas

| Instrucción ARM32 | Instrucción Switch (ARM64) | Equivalente en C | Explicación |
| :--- | :--- | :--- | :--- |
| `add r0, r1, r2` | `add w0, w1, w2`<br>`add x0, x1, x2` | `r0 = r1 + r2;` | Suma de enteros (32 bits con `w`, 64 bits con `x`). |
| `sub r0, r1, r2` | `sub w0, w1, w2`<br>`sub x0, x1, x2` | `r0 = r1 - r2;` | Resta de enteros: `r1 - r2`. |
| `mul r0, r1, r2` | `mul w0, w1, w2`<br>`mul x0, x1, x2` | `r0 = r1 * r2;` | Multiplicación entera de 32 o 64 bits. |
| `smull r0, r1, r2, r3` | `smull x0, w1, w2` | `(s64)res = (s64)w1 * (s64)w2;` | Multiplicación con signo de dos `int` de 32 bits a un `long` de 64 bits. |
| `rsb r0, r1, #0` *(ARM32)* | `neg w0, w1`<br>`neg x0, x1` | `r0 = -r1;` | Negación aritmética (`-r1`). |

---

## 4. División y Módulo: Comparativa de las 4 Consolas

| Plataforma | Método de División en C (`a / b` y `a % b`) | Cómo se identifica en el ensamblador |
| :--- | :--- | :--- |
| **GBA** | **BIOS SWI** o software | `swi 0x060000` (SWI `Div`) o llamada `bl __divsi3`. |
| **NDS** | **Hardware MMIO (NitroSDK)** | Escrituras en registros MMIO `0x04000290` (`CP_SetDiv`) y espera del resultado. |
| **3DS** | **Software Runtime CRT** para enteros / **VFP** para floats | `bl __aeabi_idiv` (enteros) / `vdiv.f32 s0, s1, s2` (flotantes por hardware). |
| **Switch** | **DIVISIÓN POR HARDWARE NATIVA (ARM64)** | **`sdiv w0, w1, w2`** (con signo 32-bit), **`udiv w0, w1, w2`** (sin signo), **`sdiv x0, x1, x2`** (64-bit). No requiere llamadas ni coprocesadores. |

*Para calcular el módulo (`a % b`) en Switch:*
ARM64 no tiene instrucción de módulo directa; calcula la división y luego hace una multiplicación con resta (*Multiply-Subtract*):
```asm
sdiv w2, w0, w1      @ w2 = a / b
msub w0, w2, w1, w0  @ w0 = a - (w2 * b)  == a % b
```

---

## 5. Desplazamientos y Manipulación de Bits

| Operación en C | GBA / NDS / 3DS (ARM32) | Nintendo Switch (ARM64) | Explicación |
| :--- | :--- | :--- | :--- |
| `r0 = r1 << 2;` | `lsl r0, r1, #2` | `lsl w0, w1, #2` (o `ubfm`) | Shift lógico a la izquierda (`* 4`). |
| `r0 = (u32)r1 >> 3;` | `lsr r0, r1, #3` | `lsr w0, w1, #3` | Shift lógico a la derecha (sin signo, rellena con ceros). |
| `r0 = (s32)r1 >> 1;` | `asr r0, r1, #1` | `asr w0, w1, #1` | Shift aritmético a la derecha (con signo, preserva bit 31). |
| `r0 = r1 + (r2 * 4);` | `add r0, r1, r2, lsl #2` | `add w0, w1, w2, lsl #2` | Suma con escalado: cálculo directo de `array[i]`. |
| `r0 = (u8)r1;` | `and r0, r1, #0xFF` *(GBA/DS)*<br>`uxtb r0, r1` *(3DS)* | `uxtb w0, w1` | Extensión a cero de byte (cast a `u8`). |
| `r0 = (u16)r1;` | Shifts *(GBA/DS)*<br>`uxth r0, r1` *(3DS)* | `uxth w0, w1` | Extensión a cero de halfword (cast a `u16`). |
| `r0 = (s8)r1;` | Shifts *(GBA/DS)*<br>`sxtb r0, r1` *(3DS)* | `sxtb w0, w1` | Extensión de signo de byte (cast a `s8`). |
| `r0 = (s16)r1;` | Shifts *(GBA/DS)*<br>`sxth r0, r1` *(3DS)* | `sxth w0, w1` | Extensión de signo de halfword (cast a `s16`). |
| Inversión Endianness | Bucles de shift *(GBA/DS)*<br>`rev r0, r1` *(3DS)* | `rev w0, w1` (32-bit)<br>`rev x0, x1` (64-bit) | Invierte el orden de bytes en memoria en 1 ciclo. |

---

## 6. Operaciones Lógicas (Bitwise)

| Operación en C | ARM32 (GBA / NDS / 3DS) | ARM64 (Switch) | Uso en Decompilación |
| :--- | :--- | :--- | :--- |
| `r0 = r1 & r2;` | `and r0, r1, r2` | `and w0, w1, w2` | Máscaras de bits. |
| `r0 = r1 \| r2;` | `orr r0, r1, r2` | `orr w0, w1, w2` | Encender flags (`flags \|= FLAG_ACTIVO`). |
| `r0 = r1 ^ r2;` | `eor r0, r1, r2` | `eor w0, w1, w2` | Alternar flags (*toggle*) o XOR. |
| `r0 = r1 & ~r2;` | `bic r0, r1, r2` | `bic w0, w1, w2` | *Bit Clear*: apagar bits usando una máscara. |
| `if (r0 & 1)` | `tst r0, #1` | `tst w0, #1` | Comprueba bits sin alterar registros (actualiza flags). |
| `r0 = r1 ^ ~r2;` | *(Múltiples instrucciones)* | `eon w0, w1, w2` | *Exclusive OR NOT* nativo en ARM64. |

---

## 7. Acceso a Memoria: Punteros, Structs y el Par `ldp` / `stp`

### Tamaños de Carga y Guardado:
- 64 bits: `ldr x0, [x1]` / `str x0, [x1]` (Solo Switch).
- 32 bits: `ldr r0, [r1]` (ARM32) / `ldr w0, [x1]` (Switch).
- 16 bits: `ldrh` / `strh`.
- 8 bits: `ldrb` / `strb`.
- 16/8 bits con extensión de signo: `ldrsh` / `ldrsb` (ARM32) o `ldrsw x0, [x1]` (carga 32-bit con signo a 64-bit en Switch).

### La Gran Revolución en Switch: `ldp` y `stp` (Load/Store Pair):
En Switch, casi todas las operaciones de pila y copia de estructuras contiguas utilizan **`stp`** y **`ldp`**, que leen o escriben **dos registros simultáneamente** en memoria contigua en una sola instrucción:

```asm
@ Guardar dos variables de 64 bits contiguas en el stack:
stp  x19, x20, [sp, #16]    @ Guarda x19 en [sp+16] y x20 en [sp+24]

@ Cargar dos registros y avanzar el puntero de pila (post-indexado):
ldp  x29, x30, [sp], #32    @ Carga x29 y x30, y luego hace sp += 32
```

---

## 8. Control de Flujo, Condiciones y Bucles

### A. Diferencia de Filosofía Condicional (ARM32 vs ARM64):
- **En ARM32 (GBA / NDS / 3DS)**:Casi cualquier instrucción puede tener sufijo condicional (`addeq`, `subne`, `ldreq`), evitando ramas de salto.
- **En ARM64 (Nintendo Switch)**: Se eliminó la ejecución condicional masiva para simplificar el pipeline de alta frecuencia. En su lugar, ARM64 ofrece:

1. **Instrucciones de Selección Condicional (`csel` = operador ternario `? :`)**:
   ```asm
   @ int res = (a == b) ? x : y;
   cmp   w0, w1
   csel  w0, w2, w3, eq     @ Si eq es verdadero, w0 = w2; si no, w0 = w3
   ```
2. **`cset` (Asignación booleana)**:
   ```asm
   @ bool es_igual = (a == b);
   cmp   w0, w1
   cset  w0, eq             @ w0 = 1 si eran iguales, 0 si no
   ```
3. **`cinc` (Incremento condicional)**:
   ```asm
   @ if (a > b) contador++;
   cmp   w0, w1
   cinc  w2, w2, gt         @ Incrementa w2 solo si w0 > w1
   ```
4. **Saltos Rápidos Comparativos en Switch**:
   - `cbz w0, label`: *Compare and Branch on Zero* (`if (w0 == 0) goto label;`).
   - `cbnz w0, label`: *Compare and Branch on Non-Zero* (`if (w0 != 0) goto label;`).
   - `tbz w0, #bit, label`: *Test Bit and Branch on Zero* (salta si un bit específico es 0).
   - `tbnz w0, #bit, label`: *Test Bit and Branch on Non-Zero*.

### B. Instrucciones de Retorno:
- **GBA**: `pop {r3}; bx r3` o `bx lr`.
- **NDS / 3DS**: `pop {..., pc}` o `bx lr`.
- **Nintendo Switch**: **`ret`** (salta incondicionalmente a la dirección contenida en el Link Register `x30`).

---

## 9. Anatomía de Funciones: Prólogos y Epílogos por Plataforma

### 1. Game Boy Advance (`agbcc` - Thumb-1):
```asm
MiFuncionGBA:
    push {r4, r5, lr}        @ Salva locales y LR
    sub  sp, #8              @ Reserva pila

    @ ... cuerpo ...

    add  sp, #8              @ Libera pila
    pop  {r4, r5}            @ Restaura locales
    pop  {r3}                @ Extrae retorno a r3
    bx   r3                  @ Retorna
```

### 2. Nintendo DS (CodeWarrior `mwccarm 3.0`):
```asm
MiFuncionNDS:
    push {r4, r5, lr}        @ PRÓLOGO
    sub  sp, sp, #12         @ Reserva pila

    @ ... cuerpo ...

    add  sp, sp, #12         @ Libera pila
    pop  {r4, r5, pc}        @ EPÍLOGO: retorna directamente en 1 ciclo
```

### 3. Nintendo 3DS (CTR SDK `armcc` / `gcc` con VFP):
```asm
MiFuncion3DS:
    push    {r4-r7, lr}      @ Salva enteros y LR
    vpush   {d8-d9}          @ Salva registros flotantes VFP (s16-s19)
    sub     sp, sp, #16      @ Reserva pila

    @ ... cuerpo matemático ...

    add     sp, sp, #16      @ Libera pila
    vpop    {d8-d9}          @ Restaura floats
    pop     {r4-r7, pc}      @ Retorna directamente
```

### 4. Nintendo Switch (Nintendo SDK Clang / LLVM - ARM64):
En Switch, **Clang genera de forma estricta la cadena de Frame Pointer** (`x29` = FP, `x30` = LR):
```asm
MiFuncionSwitch:
    stp     x29, x30, [sp, #-32]!   @ PRÓLOGO: reserva 32 bytes y guarda [FP, LR]
    mov     x29, sp                 @ Enlaza el marco de pila (Frame Pointer)
    stp     x19, x20, [sp, #16]     @ Guarda variables locales callee-saved (x19, x20)

    @ ... cuerpo de la función usando x19 y x20 ...

    ldp     x19, x20, [sp, #16]     @ EPÍLOGO: restaura variables locales
    ldp     x29, x30, [sp], #32     @ Restaura [FP, LR] y desapila 32 bytes
    ret                             @ Retorna al llamador (usando dirección en x30)
```

---

## 10. Resumen de Claves para Matching Decompilation por Consola

1. **GBA (`agbcc`)**:
   - Modo **Thumb-1** casi siempre.
   - Constantes > 255 van obligatoriamente a Literal Pools (`.pool`).
   - Sin hardware divide ni floats; busca llamadas BIOS `swi 0x06` o emulación soft-float.

2. **Nintendo DS (`mwccarm`)**:
   - Alternancia entre Thumb (lógica de juego) y ARM (ITCM rápida).
   - Multiplicaciones DSP aceleradas (`smlabb`, `clz`, `qadd`).
   - División matemática en hardware NitroSDK mediante MMIO en `0x04000280`.
   - Reordenar variables locales en C (`int a; int b;`) cambia directamente qué registro (`r4` vs `r5`) asigna CodeWarrior.

3. **Nintendo 3DS (`armcc` / `gcc`)**:
   - FPU nativa con **VFPv2** (`s0`–`s31`, `vadd.f32`, `vmul.f32`, `vldr`, `vstr`).
   - Carga de direcciones con el par `movw`/`movt` sin gastar pools de literales.
   - Instrucciones ARMv6 de empaquetado de bytes (`uxtb`, `rev`).

4. **Nintendo Switch (`clang`)**:
   - Arquitectura **64-bit pura (AArch64)** en binarios NSO.
   - Punteros y enteros de 64 bits usan registros `x`, operaciones de 32 bits usan `w`.
   - Pila siempre alineada a **16 bytes**.
   - Prólogos y epílogos dominados por pares **`stp`** y **`ldp`** gestionando `[x29, x30]`.
   - Direccionamiento de variables globales mediante pares **`adrp`** + **`add` / `ldr`** para soportar ASLR.
   - División entera nativa por hardware con **`sdiv`** y **`udiv`**.
