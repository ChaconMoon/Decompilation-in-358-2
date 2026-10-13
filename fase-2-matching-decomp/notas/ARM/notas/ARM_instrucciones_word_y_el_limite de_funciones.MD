# Los datos en assembly, los .word

En assembly debemos almacenar variables, pero al almacenar las instrucciones en 2 bytes (Thumb), el tamaño de los datos inmediatos que podemos codificar dentro de una instrucción está limitado a 1 byte (es decir, hasta 255). Ese es el valor máximo directo que se puede asignar o sumar en una sola instrucción.

```text
[ 15 14 13 12 11 ] [ 10  9  8 ] [  7  6  5  4  3  2  1  0  ]
+-----------------+------------+---------------------------+
|  0  1  0  0  1  |  Registro  |      Offset Inmediato     |
| (Opcode de LDR) |  Destino   |          (8 bits)         |
+-----------------+------------+---------------------------+
     5 bits           3 bits                 8 bits
```

En caso de que se deseen manejar valores mayores, el compilador intentará primero resolverlos usando operaciones aritméticas simples, por ejemplo:

```c
int x = 1000;
```

En assembly el resultado sería algo así:

```asm
0       mov     r0, #250
2       lsl     r0, #2
```

Es decir, para poder representarlo sin gastar memoria extra, el compilador opera el valor: por ejemplo, en lugar de almacenar `65536` en la ROM, se puede expresar como `128 << 9` ($128 \times 2^9 = 2^{16} = 65536$). Esto ahorra reservar un fragmento del binario para almacenar el valor numérico.

Si el compilador no puede obtener el valor mediante alguna operación aritmética sencilla, lo almacena en el binario como un **`.word`** (dentro del Literal Pool):

```asm
8       .word     74565
```

### ¿Qué almacena un .word?

En arquitectura ARM de 32 bits, la directiva **`.word` ocupa SIEMPRE 4 bytes (32 bits)**. No cambia de tamaño:
- Para 8 bits existe `.byte`.
- Para 16 bits existe `.hword`.
- Para 32 bits existe `.word`.

Un `.word` puede contener:
1. **Un valor numérico entero grande** de 32 bits (ej: `74565` o `0x00012345`).
2. **Un número en coma flotante** de 32 bits (`float`).
3. **Una dirección de memoria (puntero de 32 bits)**: La dirección en RAM o ROM donde se encuentra un dato de cualquier tipo (`u8`, `u16`, `u32`), una cadena de texto, un struct o una función.

## El límite de funciones y el alcance del Literal Pool (1 KB)

En Thumb, la instrucción que lee el `.word` (`ldr r0, [pc, #offset]`) tiene un límite de alcance físico: solo puede acceder a datos que estén a un máximo de **1020 bytes (~1 KB)** de distancia respecto al contador de programa (`pc`).

Por lo tanto:

- Si una función es pequeña, todos sus `.word` se colocan juntos al final de la función (tras el `bx lr`).
- Si una función es muy larga y supera 1 KB de código máquina, el compilador no puede esperar al final; se ve obligado a crear **islas de literales intermedias** en medio de la función, protegidas por un salto incondicional `b` para que la CPU no intente ejecutar esos datos como si fueran código.
