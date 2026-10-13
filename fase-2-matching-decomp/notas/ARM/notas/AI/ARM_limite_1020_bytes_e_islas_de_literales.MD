# El Límite de los 1020 Bytes en Thumb y las Islas de Literales

Guía de bajo nivel sobre la limitación física de alcance de las lecturas relativas al PC (`ldr [pc]`) en modo Thumb (16 bits) y el mecanismo de "islas de datos" utilizado por compiladores como `agbcc` y `mwccarm`.

---

## 1. El Origen del Límite: Anatomía de la Instrucción en 16 Bits

En la arquitectura ARM, el modo **Thumb** fue diseñado para ahorrar espacio de memoria en cartuchos con buses estrechos (Game Boy Advance y Nintendo DS). Cada instrucción mide **estrictamente 16 bits (2 bytes)**.

Cuando el procesador debe leer un `.word` (constante o dirección de memoria) mediante la instrucción:

```asm
ldr   r0, [pc, #offset]
```

La instrucción se codifica a nivel de hardware repartiendo sus 16 bits de la siguiente manera exacta:

```text
Bits:    [15 14 13 12 11]   [10  9  8]   [ 7  6  5  4  3  2  1  0 ]
Campo:   | 0  1  0  0  1 |  | Registro |  |    Offset Inmediato    |
Función:    Opcode LDR        Destino                 (8 bits)
              (5 bits)        (3 bits)
```

1. **5 bits para el Opcode (`01001`)**: Identifican ante la CPU que se trata de una instrucción de carga de palabra de 32 bits relativa al Program Counter (`PC`).
2. **3 bits para el Registro Destino**: Permiten direccionar exactamente $2^3 = 8$ registros posibles (`000` para `r0`, `001` para `r1` ... `111` para `r7`). Por eso en Thumb solo los registros bajos pueden recibir datos directamente con esta instrucción.
3. **8 bits para el Desplazamiento (*imm8*)**: Es todo el espacio físico que sobra dentro de la instrucción para indicar la distancia hasta el dato.

---

## 2. La Matemática del Hardware: ¿Por qué 1020 bytes y no 255?

Con 8 bits disponibles, el valor numérico máximo sin signo que se puede escribir es:

$$2^8 - 1 = 255 \quad (\text{binario } 11111111_2)$$

Si este número representara bytes directamente, el alcance máximo sería de apenas 255 bytes. Sin embargo, los diseñadores de ARM aplicaron una optimización clave:

1. Un `.word` ocupa **4 bytes** y en la memoria de la consola **siempre debe estar alineado a 4 bytes** (sus direcciones terminan siempre en `0x0`, `0x4`, `0x8` o `0xC`).
2. Al estar siempre alineado a 4 bytes, **los dos últimos bits de su dirección física son siempre cero (`00`)**.
3. El hardware de la CPU no almacena el desplazamiento en bytes, sino en **número de palabras (de 4 bytes cada una)**. Antes de sumar el desplazamiento al `PC`, la CPU lo multiplica automáticamente por 4 (un desplazamiento de 2 bits a la izquierda):

$$\text{Distancia real en bytes} = \text{imm8} \times 4$$

Por lo tanto, la distancia física máxima alcanzable hacia delante es:

$$255 \times 4 = 1020 \text{ bytes (apenas } \approx 1 \text{ KB)}$$

---

## 3. El Problema en Videojuegos Reales (Funciones > 1 KB)

En videojuegos comerciales de GBA y Nintendo DS, muchas funciones de combate, cinemáticas, menús o motores físicos ocupan **2 KB, 3 KB o más de 5 KB de código máquina** (miles de instrucciones Thumb contiguas).

Imagina una función larga con este esquema ingenuo:

```text
Offset 0x000:   ldr r0, [pc, #???]    ---> Necesita leer la dirección de g_Player
...
...             (2.500 bytes de instrucciones de combate en medio)
...
Offset 0x9C4:   bx  lr                ---> Fin de la función
Offset 0x9C6:   .word 0x02003A40      ---> &g_Player colocado al final de la función
```

En este escenario:
- La instrucción en `0x000` necesita leer el dato situado en `0x9C6` (a **2.502 bytes** de distancia).
- Como el alcance máximo físico en Thumb es de **1020 bytes**, los 8 bits de la instrucción no pueden representar ese salto.
- El compilador emitiría un error de ensamblado fatal:  
  `Error: literal pool out of range`.

---

## 4. La Solución del Compilador: "Islas de Literales" Intermedias

Para no superar jamás la barrera de los 1020 bytes, el compilador divide los Literal Pools y coloca **islas de datos intermedias en medio del flujo de código**.

Para evitar que la CPU intente ejecutar los datos numéricos o punteros como si fueran instrucciones de código, el compilador coloca **un salto incondicional (`b`) obligatorio** justo antes de la isla:

```asm
0x0F0:   ldr   r0, [pc, #8]       @ Lee el .word de la isla cercana (a solo 12 bytes)
0x0F2:   add   r1, r0, #4
...
0x0FA:   b     continuar_codigo   @ ¡SALTO OBLIGATORIO! Salta por encima de los datos

         @ ==========================================
         @ ISLA DE LITERALES INTERMEDIA (.pool)
         @ ==========================================
0x0FC:   .word 0x02003A40         @ Dirección física en RAM (&g_Player)
0x100:   .word 0x08004510         @ Puntero a tabla de datos en ROM

continuar_codigo:
0x104:   ldr   r2, [r0]           @ La ejecución continúa con normalidad
```

---

## 5. Cómo Identificar las Islas en Decompilación y Matching

Cuando estés analizando un desensamblado en Ghidra, IDA o decomp.me:

1. **El salto misterioso hacia delante**: Si ves una instrucción `b label` incondicional en mitad de una función, no busques un `if` o un bucle en C; mira qué hay inmediatamente después del salto. Si hay datos `.word`, se trata de una isla de literales.
2. **Directiva `.pool` o `.ltorg`**: En los archivos `.s` de decompilación, los desarrolladores utilizan la directiva `.pool` (en ARM) o `.ltorg` (en GNU as) para forzar al compilador a vaciar las constantes acumuladas en ese punto exacto.
3. **Impacto en el Matching**: Si al decompilar una función larga en C tus instrucciones coinciden pero tu binario es más largo o más corto que el original, suele deberse a que **el compilador original generó una isla de literales en un punto distinto al tuyo**. Alterar el orden de las variables locales o partir bloques `if` fuerza al compilador a ubicar la isla en el byte exacto requerido para el 100% match.
