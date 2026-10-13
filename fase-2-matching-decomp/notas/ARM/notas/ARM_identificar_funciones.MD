# Identificando las funciones.

En un proyecto de decompilación real nadie te va a dar nada escrito, por lo que he es importante que identificar las partes de la función que está en en dirección de memoria `0x00104D18`:

```asm
func_00104D18:
    ldr     r1, [pc, #4]        @ r1 = dirección de g_flag_00814E54
    strb    r0, [r1]            @ *(u8 *)0x00814E54 = r0
    bx      lr                  @ regresar al llamador

    .word   0x00814E54         @ dirección de la variable global
```

## Nombre de la función:

Lo primero de todo, siguiendo la nomenclaura "estandar" la función debe llamarse es `func_(dirección de memoria de la función)`, en este caso: `func_00104D18`

## Parametros de la función

Los parametros de la función son `r0` y r`r1` 