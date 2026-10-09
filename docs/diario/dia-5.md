# Diario de aprendiendo a decompilar en 358/2 dias - Dia 5: (Punteros, matrices y demás)

### Info:
- **Fecha**: 1 de Octubre de 2026
- **Objetivo general de la sesión**: Funciones en C, paso por referencia y desreferenciación de memoria con punteros.
- **Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel

<img src="./diario-images/day-5.png" width="100%" alt="day-5 card">

He seguido avanzando con [la guia de Beej para C](https://beej.us/guide/bgc/) y he terminado los capitulos 4 y 5, que son las funciones y los punteros respectivamente, las funciones son lo tipico de todos los lenguajes de programación, un fragmento de código al que puedes llamar desde otras partes del proyecto, pero creo que lo he entendido.

***De ahora en adelante siempre que aprenda algo nuevo voy a explicarlo en las entradas del diario, este tiene la finalidad de que me demuestre a mi mismo si he comprendido lo que estoy aprendiendo, es un parte técnica, pero espero hacerlo digerible.***

## Las funciones en C

Puede que me falle la memoria pero hasta donde recuerdo en Python debes implementar una función en el momento en el que la declaras, pues en C no tienes porque hacerlo asi, la declaración es independiente de la implementación: **SIEMPRE** debe declararse antes de llamarse, aunque se implemente despues. Imagino que internamente funciona de esta forma: al declarar una función esta recibe un espacio o símbolo en memoria al que se llama cada vez que se usa la función, por lo que al momento de compilar ya sabe donde esta la función en memoria y luego cuando se implemente ya sabe que instrucciones tiene. Y todas las funciones se declaran con un tipo (`int`, `bool`, `float` o `void`) según lo que se desea devolver; es decir, una función no deja de ser un bloque de instrucciones en memoria. Además tiene la particularidad de que en C una función **SOLO PUEDE DEVOLVER UN ÚNICO VALOR**, por lo que no se puede devolver un array completo de golpe directamente.

## Los punteros

La gran particularidad de C, los punteros. En esencia un puntero es una variable que almacena una dirección de memoria. Es decir, cuando declaro `int *vida` estoy diciendo que esta variable almacena la dirección de memoria de un entero. Para obtener la dirección de una variable se le asigna con el operador `&`:

```C
int ps = 10;
int *vida = &ps;
```

Es decir, en este fragmento de código, `vida` vale la dirección de memoria de `ps`. Si hacemos esto:

```C
*vida = 20;

printf("%d\n", ps);
```

Aquí se imprime 20, ¿pero cómo, si no hemos tocado `ps` directamente?

Sí, sí lo hemos hecho. Gracias a `*vida` (operador de desreferencia) hemos accedido exactamente a la dirección física donde está ubicado `ps` en la memoria RAM y hemos cambiado su valor directamente. Este es el mayor potencial de C: al trabajar directamente sobre la RAM el control que tenemos sobre nuestro software es total y será mi mayor aliado al decompilar.

Por último, esto permite resolver una de las aparentes limitaciones de C: el solo poder devolver un valor por función. Puesto que podemos alterar la memoria externa dentro de la función pasando direcciones, no necesitamos devolver nada (`void`).

Un ejemplo clásico de esto es el intercambio de valores:

```C
void intercambiar_valores(int *mem_a, int *mem_b)
{
        int temp = *mem_a; // Guardamos el valor que hay dentro de la dirección de a
        *mem_a = *mem_b;   // Escribimos en la RAM de a lo que hay en la RAM de b
        *mem_b = temp;     // Escribimos en la RAM de b el valor original de a
} 

int a = 5;
int b = 10;

intercambiar_valores(&a, &b);

printf("%d\n", a); // Imprime el 10
printf("%d\n", b); // Imprime el 5
```

Es decir, aquí tenemos una función que modifica 2 valores en su origen, algo para lo que en otros lenguajes necesitaríamos devolver una tupla, un array o un objeto; en este caso no. Y personalmente me flipa, siento que he desbloqueado los "cheats" de la programación: si aprendo a usarlos mi potencial como programador será ilimitado (bueno, ojalá).

Esto es lo que he aprendido hoy. Es duro, es muy duro, aún tengo miedo de equivocarme haciendo cosas así o de bloquearme, pero tengo un año para dominarlo y espero conseguirlo.

Lo siguiente serán los arrays. No creo que se diferencien mucho de otros lenguajes, pero los punteros serán una parte fundamental; ya iré contando.

### Checklist:

#### Guia de Beej para la programación en C
- [x] Capitulo 4. Funciones.
- [x] Capitulo 5. Punteros.

### Tags:
#DecompilandoEn358Dias #C #Punteros #MemoriaRAM #UnderTheHood

