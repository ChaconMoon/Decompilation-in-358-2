# El cartucho y el binario en ARM

## El cartucho

Un cartucho **NUNCA** contiene el código fuente de un software. Ese código original en C o C++ sigue guardado en algún repositorio en las oficinas de Osaka o Tokio. Lo que nosotros extraemos del cartucho es el resultado de compilar ese proyecto según la consola de destino:

| Consola de destino | Compilador Histórico (Toolchain) |
| --- | --- |
| GBA | `agbcc` |
| DS | MetroWerks CodeWarrior `mwccarm 3.0` |
| 3DS | Nintendo CTR SDK `armcc` / `gcc` |
| Switch | Nintendo SDK Clang / LLVM |

Esto da como resultado **el binario**, que dentro del cartucho o ROM se empaqueta como un fichero de código ejecutable (por ejemplo, en Nintendo 3DS es el fichero `.code` extraído de la partición del juego).

## Matcheando el binario

En una decompilación de **matching** se busca recrear el binario original, es decir, que el resultado de compilar nuestro código C sea **idéntico** al original del cartucho, byte a byte.

Se busca esta exactitud porque hacer lo mismo a nivel de comportamiento en C puede dar como resultado diferentes binarios. Por ejemplo:

```asm
0        mov       r1, #250
2        lsl       r1, #2
4        add       r0, r1
6        bx        lr
```

```c
s32 offsetFar(s32 x) {
    int y = 250;
    y *= 4;
    return x + y;
}
```

Pero si por ejemplo cambiamos el tipo de dato que devuelve la función, el binario resultante será diferente aunque matemáticamente produzca el mismo número:

```c
s16 offsetFar(s32 x) {
    int y = x + 1000;
    return y;
}
```

Al devolver `s16` en lugar de `s32`, el compilador inyecta instrucciones de extensión de signo (`lsl` + `asr`) para truncar el resultado a 16 bits, generando más bytes en el binario y rompiendo el match.

Estudiando la función en assembly podemos crear una función en C que devuelva exactamente el mismo binario, consiguiendo así una réplica "perfecta" del código original.

Mi objetivo va a ser poder ayudar a decompilar un binario real de ARM aprendiendo las instrucciones de assembly y cómo se traducen a código C.
