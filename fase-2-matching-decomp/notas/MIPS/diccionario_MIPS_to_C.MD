# Diccionario de Ensamblador MIPS a C

Guía rápida de consulta para decompilación e ingeniería inversa de **Nintendo 64 (VR4300 / MIPS III)**, **Sony PlayStation 1 (R3000A / MIPS I)**, **Sony PlayStation 2 (Emotion Engine R5900 / MIPS IV)** y **Sony PSP (Allegrex / MIPS32)**.

---

## 1. Registros de la CPU y Convención de Llamada (ABI o32 / N64)

La arquitectura MIPS posee 32 registros de propósito general de 32 bits (o 64 bits en N64/PS2, usando modo o32/n32), identificados por número (`$0`–`$31`) o por nombre mnemónico de convención ABI:

| Registro | Nombre ABI | Propósito en C | ¿Quién lo preserva? |
| :--- | :--- | :--- | :--- |
| **`$0`** | **`$zero`** | Constante `0` fija cableada por hardware (las escrituras se ignoran) | Cableado fijo |
| **`$1`** | **`$at`** | *Assembler Temporary* (reservado para pseudo-instrucciones del ensamblador) | Volátil |
| **`$2`–`$3`** | **`$v0`–`$v1`** | **Valores de retorno** de funciones / Expresiones | *Caller-saved* (volátil) |
| **`$4`–`$7`** | **`$a0`–`$a3`** | **Argumentos 1 a 4** de entrada de funciones | *Caller-saved* (volátil) |
| **`$8`–`$15`** | **`$t0`–`$t7`** | **Variables temporales** de corta duración | *Caller-saved* (volátil) |
| **`$16`–`$23`** | **`$s0`–`$s7`** | **Variables locales** persistentes | **Callee-saved** (debe preservarse en stack) |
| **`$24`–`$25`** | **`$t8`–`$t9`** | Temporales adicionales (en llamadas PIC, `$t9` guarda dirección de función) | *Caller-saved* (volátil) |
| **`$26`–`$27`** | **`$k0`–`$k1`** | Reservados para el kernel y manejadores de interrupciones | Kernel |
| **`$28`** | **`$gp`** | **Global Pointer** (puntero a datos globales pequeños `.sdata` / `.sbss`) | Preservado |
| **`$29`** | **`$sp`** | **Stack Pointer** (puntero de pila en RAM, crece hacia abajo) | Preservado |
| **`$30`** | **`$fp` / `$s8`** | **Frame Pointer** o 9º registro local preservado | **Callee-saved** |
| **`$31`** | **`$ra`** | **Return Address** (dirección de retorno tras `jal` / `jalr`) | Preservado si llama a otras |
| **`HI` / `LO`** | - | Registros especiales para resultados de multiplicación y división | *Caller-saved* |

> [!NOTE]
> **Registros de Coma Flotante (COP1 / FPU)**:
> - `$f0`, `$f2`: Valores de retorno de funciones con `float` o `double`.
> - `$f12`, `$f14`: Argumentos flotantes de entrada de funciones en ABI o32.
> - `$f20`–`$f31`: Registros flotantes preservados (*callee-saved*).

---

## 2. Movimiento de Datos y Constantes

MIPS tiene instrucciones de longitud fija estricta de 32 bits (4 bytes). Los valores inmediatos están limitados a 16 bits, por lo que las constantes grandes requieren dos instrucciones:

| Instrucción MIPS | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `move $v0, $a0` | `a = b;` | Pseudo-instrucción: en realidad ejecuta `addu $v0, $a0, $zero` o `or $v0, $a0, $zero`. |
| `li $a0, 42` | `a = 42;` | Pseudo-instrucción: `addiu $a0, $zero, 42` (constante con signo de 16 bits). |
| `lui $v0, 0x1234`<br>`ori $v0, $v0, 0x5678` | `a = 0x12345678;` | Carga de constante de 32 bits: *Load Upper Immediate* (16 bits altos) + `ori` o `addiu`. |
| `lui $at, %hi(g_Var)`<br>`lw $v0, %lo(g_Var)($at)` | `a = g_Var;` | Carga el valor de una variable global de 32 bits desde su dirección física en RAM. |
| `lw $v0, %gprel(g_Var)($gp)` | `a = g_Var;` | Carga rápida desde la sección `.sdata` usando el Global Pointer. |

---

## 3. Operaciones Aritméticas

| Instrucción MIPS | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `addu $v0, $a0, $a1` | `v0 = a0 + a1;` | Suma de enteros sin trampa de overflow (estándar emitido por compiladores de C). |
| `addiu $a0, $a0, 1` | `a0 += 1;` | Incremento inmediato (sumar constante con signo de 16 bits). |
| `subu $v0, $a0, $a1` | `v0 = a0 - a1;` | Resta clásica: `a0 - a1`. |
| `negu $v0, $a0` | `v0 = -a0;` | Pseudo-instrucción: ejecuta `subu $v0, $zero, $a0` (`0 - a0`). |
| `mult $a0, $a1`<br>`mflo $v0` | `v0 = a0 * a1;` | Multiplicación entera con signo de 32 bits. El resultado bajo queda en `LO` y se extrae con `mflo`. |
| `multu $a0, $a1`<br>`mfhi $v1`<br>`mflo $v0` | `(u64)v = (u64)a0 * a1;` | Multiplicación de 64 bits sin signo: parte alta en `HI`, parte baja en `LO`. |
| `div $a0, $a1`<br>`mflo $v0`<br>`mfhi $v1` | `cociente = a0 / a1;`<br>`resto = a0 % a1;` | División entera con signo por hardware: `mflo` extrae el cociente y `mfhi` el resto (`%`). |
| `divu $a0, $a1` | `a0 / a1` (sin signo) | División entera sin signo. |

> [!WARNING]
> En MIPS, las instrucciones `add` y `sub` disparan una excepción de hardware (*Integer Overflow Trap*) si hay desbordamiento. Dado que el estándar C define el desbordamiento de enteros sin signo como modular y el con signo no debe abortar por hardware, **los compiladores de C emiten casi exclusivamente `addu`, `addiu` y `subu`**.

---

## 4. Desplazamientos de Bits (Shifts)

En MIPS, los desplazamientos tienen instrucciones dedicadas según si la cantidad a desplazar es una constante fija (*shamt*, 5 bits) o una variable dinámica en otro registro:

| Instrucción MIPS | Operación en C | Significado |
| :--- | :--- | :--- |
| `sll $v0, $a0, 2` | `v0 = a0 << 2;` | Shift lógico a la izquierda (equivale a `a0 * 4`). |
| `srl $v0, $a0, 3` | `v0 = (u32)a0 >> 3;` | Shift lógico a la derecha (**sin signo**, rellena con ceros). |
| `sra $v0, $a0, 1` | `v0 = (s32)a0 >> 1;` | Shift aritmético a la derecha (**con signo**, preserva el bit de signo). |
| `sllv $v0, $a0, $a1` | `v0 = a0 << a1;` | Shift lógico a la izquierda con cantidad variable en registro `$a1`. |
| `srlv $v0, $a0, $a1` | `v0 = (u32)a0 >> a1;` | Shift lógico a la derecha con cantidad variable. |
| `srav $v0, $a0, $a1` | `v0 = (s32)a0 >> a1;` | Shift aritmético a la derecha con cantidad variable. |

---

## 5. Operaciones Lógicas (Bitwise)

| Instrucción MIPS | Operación en C | Uso común en videojuegos |
| :--- | :--- | :--- |
| `and $v0, $a0, $a1` | `v0 = a0 & a1;` | Máscara de bits entre dos registros. |
| `andi $v0, $a0, 0xFF` | `v0 = a0 & 0xFF;` | Máscara con constante inmediata sin signo (ej. casting a `u8`). |
| `or $v0, $a0, $a1` | `v0 = a0 \| a1;` | Unión de bits / encender flags. |
| `ori $v0, $a0, 0x10` | `v0 = a0 \| 0x10;` | Encender flag inmediato. |
| `xor $v0, $a0, $a1` | `v0 = a0 ^ a1;` | Alternar bits (*toggle*) o XOR. |
| `nor $v0, $a0, $zero` | `v0 = ~a0;` | Inversión bit a bit (`NOT` lógico): `NOR` con `$zero` equivale a `~a0`. |

---

## 6. Acceso a Memoria (Punteros, Structs y Arrays)

### Tipos de carga y guardado:
- `lw` / `sw`: 32 bits (*Word*, `u32` / `s32` / punteros).
- `lh` / `lhu`: 16 bits (*Halfword*, con signo / sin signo `u16` / `s16`).
- `sh`: 16 bits (*Store Halfword*).
- `lb` / `lbu`: 8 bits (*Byte*, con signo / sin signo `u8` / `s8`).
- `sb`: 8 bits (*Store Byte*).
- `lwl` / `lwr`: Carga de palabras desalineadas en memoria (par de instrucciones imprescindible en MIPS I).

### Modos de direccionamiento y su traducción a C:

En MIPS el único modo de direccionamiento nativo es **base + offset de 16 bits con signo**: `offset($base)`.

| Modo de Ensamblador | Equivalente en C | Contexto de videojuego |
| :--- | :--- | :--- |
| `lw $v0, 0($a0)` | `v0 = *a0;` | Desreferenciar un puntero directo. |
| `sw $v0, 0($a0)` | `*a0 = v0;` | Escribir a través de un puntero. |
| `lw $v0, 8($a0)` | `v0 = a0->campo;` | Acceso a miembro de un `struct` en offset `+8`. |
| `sb $v0, 1($a0)` | `a0->flag = v0;` | Escribir un `bool` o `u8` en un struct. |
| `sll $t0, $a1, 2`<br>`addu $t0, $a0, $t0`<br>`lw $v0, 0($t0)` | `v0 = a0[a1];` | Lectura de array: calcula `base + (index * 4)` y carga la palabra. |

> [!IMPORTANT]
> MIPS **exige alineación estricta de memoria**. Una instrucción `lw` en una dirección no múltiplo de 4 provocará una excepción de hardware (*Address Error Exception*). Si el código maneja datos empaquetados o no alineados, los compiladores emiten pares `lwl` / `lwr` (*load word left / right*).

---

## 7. Control de Flujo, Condiciones y Bucles

A diferencia de ARM o x86, **MIPS no tiene registro de flags (como CPSR o EFLAGS)**. Las comparaciones o bien se evalúan en saltos directos o se calculan en un registro de propósito general con la familia `slt` (*Set on Less Than*):

### Comparaciones (`slt` / Set on Less Than):

| Instrucción MIPS | Operación en C | Significado |
| :--- | :--- | :--- |
| `slt $t0, $a0, $a1` | `t0 = (a0 < a1);` | `$t0 = 1` si `a0 < a1` (con signo), de lo contrario `$t0 = 0`. |
| `sltu $t0, $a0, $a1` | `t0 = ((u32)a0 < (u32)a1);` | Comparación menor que **sin signo**. |
| `slti $t0, $a0, 10` | `t0 = (a0 < 10);` | Comparación menor que contra constante inmediata con signo. |
| `sltiu $t0, $a0, 10` | `t0 = ((u32)a0 < 10);` | Menor que contra constante sin signo. |

### Saltos condicionales y llamadas:

| Instrucción MIPS | Equivalente en C | Explicación |
| :--- | :--- | :--- |
| `beq $a0, $a1, label` | `if (a0 == a1) goto label;` | Salta si ambos registros son iguales. |
| `bne $a0, $a1, label` | `if (a0 != a1) goto label;` | Salta si los registros son distintos. |
| `blez $a0, label` | `if (a0 <= 0) goto label;` | Salta si el registro es menor o igual a cero. |
| `bgez $a0, label` | `if (a0 >= 0) goto label;` | Salta si es mayor o igual a cero. |
| `bltz $a0, label` | `if (a0 < 0) goto label;` | Salta si es estrictamente menor a cero. |
| `bgtz $a0, label` | `if (a0 > 0) goto label;` | Salta si es estrictamente mayor a cero. |
| `j label` | `goto label;` | Salto incondicional absoluto en el mismo segmento de 256 MB. |
| `jal func` | `func();` | *Jump and Link*: llamada a función (guarda dirección de retorno en `$ra`). |
| `jr $ra` | `return;` o `return $v0;` | *Jump Register*: retorno de función saltando a `$ra`. |
| `jalr $t9` | `(*fn_ptr)();` | Llamada indirecta a través de puntero a función almacenado en `$t9`. |

---

## 8. El Concepto Vital: Branch Delay Slot (Ranura de Retardo)

En la arquitectura MIPS con pipeline clásico de 5 etapas, cuando la CPU decodifica un salto (`j`, `jal`, `jr`, `beq`, `bne`), **la instrucción que se encuentra inmediatamente después en memoria SIEMPRE se ejecuta**, se cumpla o no la condición del salto.

### Ejemplo con `nop`:
```asm
    jal  CalcularVida
    nop                     @ DELAY SLOT: se ejecuta antes de saltar a CalcularVida
```

### Optimización del compilador (Mover código al delay slot):
Los compiladores de C aprovechan este ciclo para colocar una instrucción útil antes de saltar:
```asm
    jal  CalcularVida
    move $a0, $s0           @ DELAY SLOT: pasa el argumento a la función mientras salta
```
En C esto corresponde a una llamada normal: `CalcularVida(jugador);`.

---

## 9. Anatomía de una Función en MIPS (Prólogo y Epílogo)

### Función Hoja (*Leaf Function* - No llama a otras funciones):
No necesita crear stack frame ni alterar `$ra` si solo requiere los registros volátiles `$a0`–`$a3` y `$t0`–`$t7`:
```asm
# int Sumar(int a, int b) { return a + b; }
Sumar:
    jr   $ra
    addu $v0, $a0, $a1      @ DELAY SLOT: calcula y devuelve el valor en $v0 al salir
```

### Función Compleja (*Non-Leaf* - Llama a otras funciones o usa registros preservados):
Debe ajustar el puntero del stack `$sp` (siempre múltiplo de 8 o 16 bytes), guardar `$ra` y los `$s0`–`$s7` utilizados:
```asm
MiFuncion:
    addiu $sp, $sp, -24     # PRÓLOGO: reserva 24 bytes en la pila
    sw    $ra, 20($sp)      # Guarda la dirección de retorno
    sw    $s0, 16($sp)      # Guarda variable local preservada

    move  $s0, $a0          # s0 = arg1
    jal   OtraFuncion       # Llama a otra subrutina
    move  $a0, $s0          # DELAY SLOT: prepara el argumento para OtraFuncion

    lw    $s0, 16($sp)      # EPÍLOGO: restaura el registro s0
    lw    $ra, 20($sp)      # Restaura la dirección de retorno original
    jr    $ra               # Retorna al llamador
    addiu $sp, $sp, 24      # DELAY SLOT: libera el espacio del stack
```

---

## 10. Peculiaridades Clave en Decompilación de MIPS

1. **Reordenación por Branch Delay Slot**:
   - Al leer código decompilado, **nunca ignores la instrucción debajo de un salto**. Suele ser la preparación del argumento de la llamada o la liberación del stack.
2. **Constantes divididas en dos mitades (`%hi` / `%lo`)**:
   - `lui` carga los 16 bits altos. Si los 16 bits bajos tienen el bit 15 encendido (signo negativo), al usar `addiu` restará 1 a la parte alta. Por eso los ensambladores usan `%hi` con ajuste de signo o prefieren `ori` (que no extiende signo).
3. **MIPS I (PlayStation 1) y Load Delay Slots**:
   - En PS1 (R3000A), el dato cargado con `lw` o `lb` **no está disponible en la instrucción siguiente**. Se requería un `nop` o una instrucción independiente intermedia antes de leer el registro cargado. En N64 (VR4300) el hardware ya cuenta con bloqueo automático (*hardware interlock*).
4. **La sección Small Data (`.sdata` / `$gp`)**:
   - En N64 y PS2, los compiladores agrupan variables globales pequeñas (<= 8 bytes) en `.sdata`. Se accede a ellas con un solo `lw $reg, offset($gp)`, ahorrándose el par `lui`/`lw`.

