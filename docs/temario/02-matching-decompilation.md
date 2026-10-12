# Temario Detallado · Fase 2: Matching Decompilation (El Arte del 100% Match)

En la **Fase 2** pasarás de ser un lector pasivo de código decompilado a convertirte en un desensamblador activo. Aprenderás a escribir código en C que empareje con exactitud matemática el ensamblador original.

**Estado actual:** Proyecto Yo-kai Watch 2 inicializado como repositorio independiente. Ya existe la estructura base, el archivo `.code`, el script `tools/extract_rom.py` y un `code.raw.bin` extraído. Todavía no hay funciones C decompiladas ni un primer *match* validado.

La prioridad inmediata no es decompilar el juego completo, sino preparar un flujo reproducible: documentar la extracción, identificar una primera función pequeña y crear un *scratch* aislado antes de intentar el matching.

---

## Bloque 2.1: Ensamblador ARM y Calling Conventions

### Arquitecturas ARM de referencia
- **Nintendo DS / `khdays-decomp`**: ARM946E-S, basada en ARMv5TE. Es la plataforma de referencia para estudiar una decompilación matching madura.
- **Nintendo 3DS / Yo-kai Watch 2**: ARM11 MPCore, basada en ARMv6K. Es la arquitectura del proyecto activo de esta fase.
- Las convenciones de llamada, el modo de instrucción y las extensiones disponibles deben confirmarse para cada binario antes de escribir C. No se debe asumir que una técnica válida para Nintendo DS produce el mismo ensamblador en Nintendo 3DS.

### Registros de una CPU ARM de 32 bits
- **Registros de Propósito General**:
  - `r0`–`r3`: Primeros 4 parámetros de entrada de funciones y valor de retorno (`r0`). Son registros volátiles (*scratch registers*); el llamador asume que su valor se perderá tras la llamada.
  - `r4`–`r11`: Registros preservados (*callee-saved*). Si una función los usa, debe guardarlos en el stack al entrar (*prólogo*) y restaurarlos antes de salir (*epílogo*).
  - `sp` (`r12` / `r13`): Puntero al stack.
  - `lr` (`r14`): Registro de enlace (*link register*), guarda la dirección a la que volver tras un `BL` (Branch with Link).
  - `pc` (`r15`): Contador de programa (*program counter*), dirección de la instrucción en ejecución.
- **El Registro de Estado (`CPSR`) y Ejecución Condicional**:
  - En ARM, casi cualquier instrucción puede ejecutarse de forma condicional agregando un sufijo: `MOVEQ` (mover si es igual), `ADDNE` (sumar si no es igual). Esto permite escribir código sin ramas de salto (*branches*), acelerando la ejecución en CPUs sin predicción de saltos compleja.

---

## Bloque 2.2: Compiladores Históricos y Herramientas

### Toolchains y compiladores históricos
- En *Kingdom Hearts 358/2 Days*, el compilador de referencia es MetroWerks CodeWarrior `mwccarm 3.0 build 139`.
- En Yo-kai Watch 2, la toolchain y sus opciones todavía deben identificarse a partir del binario, los metadatos y la documentación del proyecto. No se debe trasladar automáticamente la configuración de Nintendo DS al objetivo de Nintendo 3DS.
- Su generador de código tiene comportamientos peculiares:
  - Orden particular de asignación de variables en registros según el orden en que se declaran en el bloque de C.
  - Generación de literales numéricos en bloques contiguos (*literal pools*).

### La Plataforma [decomp.me](https://decomp.me/)
- Permite crear "Scratches": entornos aislados donde pegas el ensamblador objetivo, seleccionas la plataforma (ej. Nintendo DS), el compilador y los flags, y escribes código C con retroalimentación visual inmediata.
- **Códigos de Color del Diff**:
  - **Verde/Rojo**: Instrucciones distintas o faltantes.
  - **Amarillo/Naranja**: Misma instrucción pero con un registro diferente (ej. el original usó `r2` y tu código produjo `r3`).
  - **Blanco**: Coincidencia perfecta.

---

## Bloque 2.3: Técnicas de Matching

### 1. El Juego de los Registros
Si tu código en C produce `ADD r3, r1, #4` pero el ensamblador original tiene `ADD r2, r1, #4`:
- Significa que el compilador decidió colocar esa variable local en `r2`.
- Puedes influir en la decisión del compilador **reordenando las declaraciones de variables** al inicio de la función o alterando el orden en que se usan por primera vez.

### 2. Equivalencias de Bucles
- Un bucle `for` en C a menudo compila a una comprobación al final en lugar del principio si el compilador detecta que siempre se ejecuta al menos una vez, comportándose como un `do-while`.
- Si el diff muestra un salto extra incondicional `B` al inicio, cambia tu `for` por un `while` o `do-while`.

### 3. Tipos y Castings Ocultos
- Operar con tipos de 8 bits (`u8`) o 16 bits (`u16`) a menudo fuerza al compilador a insertar instrucciones de extensión de signo o ceros (`AND r0, r0, #0xFF` o `UXTB`). Si el original no las tiene, significa que la variable en el código fuente original era probablemente un entero de 32 bits (`int`).

### Hitos de Validación de Fase 2
1. Documentar el estado inicial del proyecto y reproducir la extracción de `code.raw.bin` desde una copia legal de la ROM.
2. Seleccionar una primera función pequeña y registrar su dirección, arquitectura, convención de llamada y bytes de referencia sin incluir datos comerciales en el repositorio.
3. Conseguir el primer **100% MATCH** en una función real, en decomp.me o en un repositorio local, y añadir el informe a `fase-2-matching-decomp/matches/`.
