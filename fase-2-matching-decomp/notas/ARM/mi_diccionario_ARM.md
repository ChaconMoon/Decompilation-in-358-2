# Mi Diccionario Personal de Ensamblador ARM a C

**Autor**: Carlos  
**Enfoque**: Patrones empíricos, trucos de matching y equivalencias descubiertas en decompilaciones reales (GBA, NDS, 3DS, Switch).

---

## 1. Movimiento de Datos y Carga de Constantes

### mov

Asigna un vlaor a un operador.

```asm
0        mov       r0, #42
```

Equivale a esto en C:

```C
r0 = 42;
```

---

## 2. Operaciones Aritméticas

### add

#### add con 2 operandos

add con 2 operandos suma el valor de la segunda posición a la de la primera.

```asm
0        add       r0, r1
```

El equivalente en C:

```C
r0+=r1;
```

#### add con 3 operandos

add con 3 operandos suma el valor de la segunda y tercera posición a la de la primera:

```asm
0        add       r0, r1, r2
```

El equivalente en C:

```C
r0= r1 + r2;
```

### sub

#### sub con 2 operandos

sub con 2 operandos resta el valor de la segunda posición a la de la primera.

```asm
0        sub       r0, r1
```

El equivalente en C:

```C
r0-=r1;
```

#### Con 3 operandos

sub con 3 operandos resta el valor de la segunda y tercera posición a la de la primera:

```asm
0        sub       r0, r1, r2
```

El equivalente en C:

```C
r0= r1 - r2;
```

### neg

#### neg con 2 operandos diferentes

neg con 2 operandos diferentes asigna al origen el operador del destino.

```asm
0        neg       r0, r1
```

```c
r0 = -r1;
```

#### neg con 2 operandos iguales

neg con 2 operandos iguales invierte el signo del operando.

```asm
0        neg       r0, r0
```

```c
r0 = -r0;
```

o

```c
return -r0;
```

---

## 3. Desplazamientos y Operaciones de Bits (Bitwise)

### lsl

Desplaza una determinada cantidad de el origen:

```asm
lsl       r0, r1, #2 @Desplaza 2 bits a la izquierda, es decir *2*(tercer campo)
```

En C equivalente a esto:

```c
    return a<<=2;
```

Tambien se puede hacer asi:

```c
    return a*(2*2);
```

### ldr

Lee un valor de 32 bits desde una dirección de memoria calculada a partir de un registro base y un desplazamiento.

En este caso, `pc` representa el contador de programa, es decir, la dirección de ejecución. En ARM state, al utilizarlo como operando, su valor observado suele ser la dirección de la instrucción actual más 8 bytes.

```asm
func_00104D18:
    ldr     r1, [pc, #4]
    strb    r0, [r1]
    bx      lr

    .word   0x00814E54
```

Si el `ldr` está en `0x00104D18`, la CPU calcula:

```text
pc efectivo          = 0x00104D18 + 8 = 0x00104D20
dirección de lectura = 0x00104D20 + 4 = 0x00104D24
```

En `0x00104D24` se encuentra:

```text
.word 0x00814E54
```

Por tanto:

```text
r1 = memoria[0x00104D24]
r1 = 0x00814E54
```

Después, `strb` utiliza el valor de `r1` como una dirección y escribe un byte:

```asm
strb r0, [r1]
```

Conceptualmente:

```c
*(u8 *)0x00814E54 = (u8)r0;
```

En este ejemplo, `ldr` lee un valor del literal pool. Ese valor representa una dirección, por lo que posteriormente se utiliza como puntero.
---

## 4. Acceso a Memoria: Punteros, Arrays y Structs

---

## 5. Control de Flujo: Condiciones, Saltos y Bucles

---

## 6. Anatomía de Funciones: Prólogos, Epílogos y Retornos

---

## 7. Trucos de Matching y Comportamientos de Compiladores
