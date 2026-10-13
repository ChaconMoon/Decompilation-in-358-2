# Diccionario de Ensamblador PowerPC a C

Guía rápida de consulta para decompilación e ingeniería inversa de **Nintendo GameCube (Gekko / PowerPC 750CXe)**, **Nintendo Wii (Broadway / PowerPC 750CL)**, **Nintendo Wii U (Espresso / PowerPC 750CL tri-core)**, **Xbox 360 (Xenon)** y **PlayStation 3 (Cell PPE)**.

---

## 1. Registros de la CPU y Convención de Llamada (PowerPC EABI / System V ABI)

PowerPC posee 32 registros de propósito general de 32 bits (`r0`–`r31`), 32 registros de coma flotante de 64 bits (`f0`–`f31`) y registros especiales dedicados para control de flujo y bucles:

| Registro | Nombre ABI | Propósito en C | ¿Quién lo preserva? |
| :--- | :--- | :--- | :--- |
| **`r0`** | Scratch | Registro temporal volátil. Usado en prólogos para mover `LR`. *(¡Ver regla de cero!)* | *Caller-saved* (volátil) |
| **`r1`** | **`sp`** | **Stack Pointer** (apunta a la cabecera del marco actual de la pila; **nunca debe ser nulo**) | Preservado |
| **`r2`** | `rtoc` / SDA2 | Puntero a la **Small Data Area 2** (constantes y datos globales de solo lectura) | Preservado |
| **`r3`** | `a1` / Retorno | **Argumento 1** de entrada / **Valor de retorno** entero o puntero principal | *Caller-saved* (volátil) |
| **`r4`** | `a2` / Retorno | **Argumento 2** / Parte baja o alta de retorno de 64 bits (`u64` / `s64`) | *Caller-saved* (volátil) |
| **`r5`–`r10`** | `a3`–`a8` | **Argumentos 3 al 8** de entrada de funciones | *Caller-saved* (volátil) |
| **`r11`–`r12`** | Scratch | Registros temporales volátiles (a menudo usados para llamadas indirectas) | *Caller-saved* (volátil) |
| **`r13`** | SDA | Puntero a la **Small Data Area** (datos globales pequeños de lectura/escritura) | Preservado |
| **`r14`–`r31`** | Locales | **Variables locales** persistentes (CodeWarrior las asigna desde `r31` hacia abajo) | **Callee-saved** (debe preservarse en stack) |
| **`f1`** | F-Ret / F-Arg1 | **Valor de retorno flotante** (`float`/`double`) y **Argumento 1 flotante** | *Caller-saved* (volátil) |
| **`f2`–`f8`** | F-Arg2..8 | Argumentos flotantes 2 al 8 | *Caller-saved* (volátil) |
| **`f14`–`f31`** | F-Locales | Variables locales flotantes persistentes | **Callee-saved** |
| **`LR`** | Link Register | **Link Register**: guarda la dirección de retorno tras una llamada `bl` | Preservado si llama a otras |
| **`CTR`** | Count Register | **Count Register**: contador de bucles por hardware (`bdnz`) o destino de salto (`bctr`) | Volátil |
| **`CR`** | Condition Reg | **Condition Register**: 32 bits divididos en 8 campos de 4 bits (`cr0`–`cr7`) | `cr2`–`cr4` preservados |

> [!CAUTION]
> **La regla semántica de `r0` como CERO**:
> En muchas instrucciones de direccionamiento y carga aritmética (como `addi`, `addis`, `lwz`, `stw`), si se especifica `r0` como registro base `rA`, la CPU no lee el contenido del registro `r0`, sino que **lo interpreta literalmente como el valor numérico `0`**. Por ejemplo, `addi r3, 0, 10` (escrito `li r3, 10`) usa `r0` en el opcode para indicar que no hay base. Sin embargo, en instrucciones lógicas como `mr r3, r0` (`or r3, r0, r0`), `r0` sí se lee normalmente.

---

## 2. Movimiento de Datos y Constantes

En PowerPC todas las instrucciones ocupan 32 bits. Las constantes de 32 bits completas se construyen cargando primero los 16 bits altos y luego los 16 bits bajos:

| Instrucción PowerPC | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `mr r3, r4` | `a = b;` | Pseudo-instrucción: ejecuta `or r3, r4, r4` (copia registro). |
| `li r3, 10` | `a = 10;` | Pseudo-instrucción: `addi r3, 0, 10` (inmediato de 16 bits con signo). |
| `lis r3, 0x1234`<br>`ori r3, r3, 0x5678` | `a = 0x12345678;` | Carga de 32 bits: *Load Immediate Shifted* (`0x12340000`) + `ori` (`0x5678`). |
| `lis r3, g_Var@ha`<br>`lwz r4, g_Var@l(r3)` | `a = g_Var;` | Carga de variable global usando dirección ajustada con signo (`@ha` = high adjusted, `@l` = low). |
| `lwz r3, offset(r13)` | `a = g_SmallVar;` | Carga directa desde la Small Data Area (SDA) en una única instrucción. |

---

## 3. Operaciones Aritméticas

| Instrucción PowerPC | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `add r3, r4, r5` | `r3 = r4 + r5;` | Suma de dos registros. |
| `addi r3, r4, 5` | `r3 = r4 + 5;` | Suma inmediata con constante de 16 bits con signo. |
| `addis r3, r4, 2` | `r3 = r4 + (2 << 16);` | Suma inmediata desplazada 16 bits a la izquierda. |
| `subf r3, r4, r5` | `r3 = r5 - r4;` | *Subtract From*: resta el primer operando del segundo (`r5 - r4`). |
| `subfic r3, r4, 10` | `r3 = 10 - r4;` | Resta de constante menos registro (`10 - r4`). |
| `neg r3, r4` | `r3 = -r4;` | Pseudo-instrucción: `subfic r3, r4, 0` (`0 - r4`). |
| `mullw r3, r4, r5` | `r3 = r4 * r5;` | Multiplicación entera de 32 bits (*Multiply Low Word*). |
| `divw r3, r4, r5` | `r3 = r4 / r5;` | División entera con signo por hardware. |
| `divwu r3, r4, r5` | `r3 = (u32)r4 / (u32)r5;` | División entera sin signo. |
| `add. r3, r4, r5` | `r3 = r4 + r5;`<br>`if (r3 == 0)...` | El sufijo con punto (`.`) actualiza automáticamente el campo `cr0` según el resultado (< 0, > 0, == 0). |

---

## 4. Desplazamientos, Rotaciones y la Magia de `rlwinm`

PowerPC incluye una de las instrucciones más versátiles de la historia de los microprocesadores: **`rlwinm`** (*Rotate Left Word Immediate then AND with Mask*). En un solo ciclo de reloj rota un registro, le aplica una máscara de bits contiguos entre el bit inicial `MB` y el final `ME`, y guarda el resultado:

| Instrucción PowerPC | Operación en C | Significado |
| :--- | :--- | :--- |
| `slwi r3, r4, 2` | `r3 = r4 << 2;` | Pseudo-instrucción de `rlwinm r3, r4, 2, 0, 29` (shift izquierdo). |
| `srwi r3, r4, 3` | `r3 = (u32)r4 >> 3;` | Pseudo-instrucción de `rlwinm r3, r4, 29, 3, 31` (shift derecho sin signo). |
| `srawi r3, r4, 1` | `r3 = (s32)r4 >> 1;` | Shift aritmético a la derecha con signo (actualiza flag CA en XER). |
| `slw r3, r4, r5` | `r3 = r4 << r5;` | Shift a la izquierda con cantidad variable en registro `r5`. |
| `srw r3, r4, r5` | `r3 = (u32)r4 >> r5;` | Shift a la derecha sin signo con cantidad variable. |
| `rlwinm r3, r4, 0, 16, 31` | `r3 = r4 & 0x0000FFFF;` | Máscara de bits sin desplazamiento (equivale a `(u16)r4`). |
| `rlwimi r3, r4, 8, 16, 23` | *(Inserta campo de bits)* | *Rotate Left Word Immediate Mask Insert*: inserta bits en `r3` sin alterar los demás. |

---

## 5. Operaciones Lógicas (Bitwise)

| Instrucción PowerPC | Operación en C | Uso común en videojuegos |
| :--- | :--- | :--- |
| `and r3, r4, r5` | `r3 = r4 & r5;` | Máscara de bits entre dos registros. |
| `andi. r3, r4, 0xFF` | `r3 = r4 & 0xFF;` | Máscara inmediata (siempre actualiza el campo `cr0`). |
| `or r3, r4, r5` | `r3 = r4 \| r5;` | Unión de bits / encender flags. |
| `ori r3, r4, 0x10` | `r3 = r4 \| 0x10;` | Encender flag inmediato. |
| `xor r3, r4, r5` | `r3 = r4 ^ r5;` | Inversión de bits (*toggle*) o XOR. |
| `nor r3, r4, r4` | `r3 = ~r4;` | Pseudo-instrucción `not r3, r4`: `NOR` consigo mismo es complementario a uno. |
| `andc r3, r4, r5` | `r3 = r4 & ~r5;` | *AND with Complement*: apaga bits de `r4` usando la máscara `r5` (como `bic` en ARM). |
| `orc r3, r4, r5` | `r3 = r4 \| ~r5;` | *OR with Complement*. |

---

## 6. Acceso a Memoria (Punteros, Structs y Arrays)

### Tipos de carga y guardado:
- `lwz` / `stw`: 32 bits (*Word*, `u32` / `s32` / punteros; la `z` significa *zero-extended*).
- `lhz` / `sth`: 16 bits (*Halfword*, sin signo `u16`).
- `lha`: 16 bits (*Halfword Algebraic*, con signo extendido a 32 bits `s16`).
- `lbz` / `stb`: 8 bits (*Byte*, sin signo `u8` / `bool`).

### Modos de direccionamiento y actualización automática:

| Modo de Ensamblador | Equivalente en C | Contexto de videojuego |
| :--- | :--- | :--- |
| `lwz r3, 0(r4)` | `r3 = *r4;` | Desreferenciar un puntero. |
| `stw r3, 0(r4)` | `*r4 = r3;` | Escribir a través de un puntero. |
| `lwz r3, 8(r4)` | `r3 = r4->campo;` | Acceso a miembro de `struct` en offset `+8`. |
| `stb r3, 1(r4)` | `r4->flag = r3;` | Guardar `bool` o `u8` en struct. |
| `lwzx r3, r4, r5` | `r3 = *(r4 + r5);` | Indexado por registros: lee de `base + offset`. |
| `lwzu r3, 4(r4)` | `r3 = *++r4;` | **Update Mode**: avanza el puntero `r4` en 4 bytes y luego lee. |
| `stwu r1, -32(r1)` | *(Crea stack frame)* | **Store Word with Update**: escribe el viejo SP y reserva 32 bytes en la pila. |

---

## 7. Control de Flujo, Condiciones y Bucles

En PowerPC las comparaciones evalúan contra un campo del **Condition Register** (`cr0` a `cr7`, por defecto `cr0`):

### Instrucciones de comparación:

| Instrucción PowerPC | Operación en C | Significado |
| :--- | :--- | :--- |
| `cmpw cr0, r3, r4` | `(r3 == r4)` / `(r3 < r4)` | Comparación entera con signo de 32 bits. |
| `cmpwi cr0, r3, 0` | `(r3 == 0)` | Comparación contra constante inmediata con signo. |
| `cmplw cr0, r3, r4` | `((u32)r3 < (u32)r4)` | Comparación lógica (**sin signo**). |
| `cmplwi cr0, r3, 10` | `((u32)r3 < 10)` | Comparación lógica contra inmediato sin signo. |

### Saltos condicionales y llamadas:

| Instrucción PowerPC | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `beq label` | `if (a == b) goto label;` | Salta si el bit EQ del Condition Register está activo. |
| `bne label` | `if (a != b) goto label;` | Salta si los valores comparados no son iguales. |
| `blt label` | `if (a < b) goto label;` | Salta si es menor que (*Less Than*). |
| `bgt label` | `if (a > b) goto label;` | Salta si es mayor que (*Greater Than*). |
| `ble label` / `bge label` | `if (a <= b)` / `if (a >= b)` | Menor/mayor o igual. |
| `b label` | `goto label;` | Salto incondicional relativo. |
| `bl func` | `func();` | *Branch with Link*: llamada a función (guarda el retorno en `LR`). |
| `blr` | `return;` o `return r3;` | *Branch to Link Register*: retorno canónico de función. |
| `bctr` | `(*fn_ptr)();` o `switch` | *Branch to Count Register*: salto indirecto a la dirección en `CTR`. |

### El Registro CTR y Bucles Hardware (`bdnz`):

PowerPC permite implementar bucles ultrarrápidos sin gastar instrucciones en comparar ni decrementar índices:
```asm
    mtctr r4            # Carga el número de iteraciones en CTR
loop:
    # ... operaciones del bucle ...
    bdnz  loop          # Decrementa CTR; si CTR != 0, salta a loop
```
En C esto corresponde a un bucle directo: `for (int i = n; i > 0; i--)` o `do { ... } while (--n);`.

---

## 8. Anatomía de una Función en PowerPC (Prólogo y Epílogo)

En PowerPC la pila en RAM siempre mantiene una cadena enlazada hacia atrás (*back-chain*). El primer entero de 32 bits apuntado por `r1` (`0(r1)`) contiene siempre la dirección del marco del llamador, y `4(r1)` almacena su dirección de retorno (`LR`).

### Función Hoja (*Leaf Function* - No llama a nadie más):
No toca la pila ni altera el registro `LR`:
```asm
# int Duplicar(int x) { return x * 2; }
Duplicar:
    slwi r3, r3, 1
    blr
```

### Función Compleja (*Non-Leaf* con CodeWarrior):
Guarda `LR` en `r0`, reserva espacio en la pila con `stwu` y salva registros locales (`r14`–`r31`):
```asm
MiFuncion:
    mflr  r0                # PRÓLOGO: extrae la dirección de retorno de LR
    stw   r0, 4(r1)         # Guarda LR en el frame del llamador
    stwu  r1, -0x20(r1)     # Reserva 32 bytes y enlaza el back-chain en 1 ciclo
    stw   r31, 0x1C(r1)     # Salva variable local preservada (r31)

    # ... cuerpo de la función usando r31 ...

    lwz   r31, 0x1C(r1)     # EPÍLOGO: restaura variable local r31
    addi  r1, r1, 0x20      # Libera el marco de pila (desapila 32 bytes)
    lwz   r0, 4(r1)         # Recupera la dirección de retorno
    mtlr  r0                # Vuelve a colocar la dirección en LR
    blr                     # Retorna al llamador
```

---

## 9. Peculiaridades Clave en Decompilación de PowerPC (CodeWarrior)

1. **Orden de asignación de registros locales**:
   - Compiladores como MetroWerks CodeWarrior asignan los registros locales preservados **en orden inverso**, empezando siempre por `r31`, luego `r30`, `r29`... hasta `r14`.
   - Si un diff en decomp.me te pide usar `r30` y tu código usa `r31`, revisa el orden de declaración o primer uso de tus variables locales.
2. **Endianness**:
   - GameCube, Wii y Wii U son sistemas estrictamente **Big-Endian**. El byte más significativo se almacena en la dirección de memoria más baja.
3. **Mnemónicos simplificados vs código real**:
   - Muchas instrucciones que parecen independientes (`mr`, `li`, `subi`, `not`, `slwi`, `srwi`, `nop`) son simples alias (*mnemónicos simplificados*) de instrucciones primitivas como `or`, `addi`, `rlwinm` u `ori r0, r0, 0`.
4. **Optimización con Small Data Area (`r13` / `r2`)**:
   - Variables globales con atributos `__declspec(section ".sdata")` o menores de cierto umbral (`-sdata 8`) se direccionan con un solo `lwz rX, offset(r13)` sin requerir la costosa pareja `lis`/`lwz`.

