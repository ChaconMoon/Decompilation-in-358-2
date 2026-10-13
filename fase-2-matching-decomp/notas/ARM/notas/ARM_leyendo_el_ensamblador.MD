# Leyendo el ensamblador

Una vez extraído el juego obtendremos el ensamblador, el código máquina, las instrucciones que recibe directamente el procesador. Estas instrucciones se ven así:

```asm
0        mov       r0, #7
2        bx        lr
```

Las instrucciones de assembly se leen a una instrucción por línea desde arriba hacia abajo.

## Las instrucciones Thumb, las direcciones

La "primera columna" de las instrucciones es la dirección de memoria relativa (offset). Cada instrucción ocupa 2 bytes empezando desde el 0:

```asm
0
2
```

Es decir, esta función ocupa 4 bytes (del byte 0 al 4, dos por línea). Esto nos servirá más adelante cuando necesitemos acceder a un valor en una posición concreta del ensamblador o debamos tener en cuenta hacia qué dirección salta una estructura de control.

## Los mnemotécnicos y los operandos

Toda instrucción de assembly Thumb se divide en 2 secciones: el **mnemotécnico** y los **operandos**.

### El mnemotécnico

El mnemotécnico se refiere, en esencia, a la operación a realizar, por ejemplo: `add`, `sub`, `mul` o `mov`. Es la acción que se va a ejecutar en esa línea y la operación que deberemos recrear en C.

Mira el diccionario de ARM a C para ver los mnemotécnicos disponibles.

### Los operandos

Los operandos son los datos, registros y valores con los que trabajamos y que tendremos que recrear en C:

```asm
0        mov       r0, #7
```

Por ejemplo, aquí los operandos son `r0` (el registro destino) y `#7` (el valor inmediato).

En assembly los registros no tienen nombres personalizados de variables, sino que están numerados. En este caso `r0` representa una variable a la que nosotros daremos un nombre descriptivo en C.

### Los registros

Los operandos pueden ser valores numéricos directos (inmediatos, precedidos de `#`) o registros de la CPU. En GBA, DS y 3DS el conjunto de registros principales es de 16 (del `r0` al `r15`):

- **`r0` - `r7` (Los registros bajos)**: Estos 8 registros pueden manipularse libremente con casi cualquier instrucción Thumb. Casi toda la lógica del juego ocurre aquí.
- **`r8` - `r12` (Los registros altos)**: Son 5 registros que en modo Thumb apenas se tocan directamente con operaciones aritméticas normales.
- **`sp` (`r13`)**: El puntero de pila (*Stack Pointer*), gestiona la memoria de la pila en RAM.
- **`lr` (`r14`)**: El registro de enlace (*Link Register*), guarda la dirección de memoria a la que la función debe volver al terminar.
- **`pc` (`r15`)**: El contador de programa (*Program Counter*), apunta a la instrucción que se encuentra actualmente en ejecución.

En Thumb estamos limitados principalmente a los 8 registros bajos (`r0`–`r7`) para operar de forma directa.

## Introducción a la decompilación

### Instrucciones de 2 operandos

```asm
0        mov       r0, #7
2        bx        lr
```

- En una instrucción como `mov r0, #7`, el primer operando es el destino y el segundo el valor a copiar. Equivale a una asignación directa: `r0 = 7;`.
- En instrucciones aritméticas de 2 operandos como `add r0, #7`, el primer registro actúa a la vez como destino y acumulador: `r0 += 7;`.

### Instrucciones de 3 operandos

```asm
0        add       r1, r0, #7
2        bx        lr
```

Con 3 operandos la sintaxis en ARM sigue el orden: **(destino), (origen 1), (origen 2 o inmediato)**:

El valor inmediato `#7` va siempre al final. Esto equivale en C a:
```c
r1 = r0 + 7;
```

### El retorno

```asm
2        bx        lr
```

La mayoría de funciones hoja terminan con `bx lr` (*Branch and Exchange to Link Register*). Esta instrucción salta a la dirección guardada en `lr`, marcando el retorno de la función (el equivalente a `return;` o `return r0;` en C).

## Nota

No es necesario memorizar todas las instrucciones; en cualquier momento puedo consultar el diccionario de ARM a C para ver exactamente qué hace cada mnemotécnico.
