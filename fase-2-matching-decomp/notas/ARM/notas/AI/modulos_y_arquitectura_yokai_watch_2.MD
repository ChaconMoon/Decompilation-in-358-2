# Arquitectura y Módulos de Yo-kai Watch 2 (Nintendo 3DS)

> **Documento de Referencia Técnica**  
> **Autoría**: Generado por Asistente IA (Antigravity / Gemini) como material de apoyo y estudio.  
> **Ubicación en el repositorio**: `fase-2-matching-decomp/notas/ARM/notas/AI/modulos_y_arquitectura_yokai_watch_2.MD`  
> **Contexto formativo**: Reto [#DecompilandoEn358Dias](https://github.com/ChaconMoon/Decompilation-in-358-2) — Decompilación de *Yo-kai Watch 2: Mentespectros* (ARM11 MPCore / CTR).

---

## 1. Visión General del Binario

El ejecutable principal de *Yo-kai Watch 2* (`code.raw.bin`, extraído del contenedor ExeFS) es un binario monolítico de **~7,73 MB (7.737.344 bytes)** mapeado en memoria a partir de la dirección virtual base **`0x00100000`**.

Para poder abordar su decompilación matching de forma metódica y estructurada, el código se ha descompuesto en **tres macrocapas jerárquicas**:

```
+-------------------------------------------------------------+
| 3. CAPA DE JUEGO (src/game/)                                |
|    Lógica específica de Yo-kai Watch 2, loops de combate    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 2. MOTOR PROPIETARIO LEVEL-5 (src/engine/)                  |
|    Framework lfw, gestores de memoria lxp, core             |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 1. NINTENDO CTR-SDK & KERNEL (src/ctr/)                     |
|    Llamadas a supervisor (svc), nn::os, nn::y2r, nn::nex    |
+-------------------------------------------------------------+
```

---

## 2. Capa 1: Nintendo CTR-SDK y Kernel (`src/ctr/`)

Esta capa representa la interfaz más cercana al silicio de la consola. No contiene lógica del juego; su función es comunicarse con el microkernel de la 3DS y con sus coprocesadores de hardware.

### 2.1. `ctr/svc` (Supervisor Calls / Interrupciones de Kernel)
* **Propósito**: Son las **llamadas al sistema (*syscalls*)** de Nintendo 3DS. En ARMv6K se ejecutan mediante la instrucción `svc 0x??`, conmutando la CPU de modo usuario a modo supervisor con privilegios de kernel.
* **Módulos clave decompilados**:
  * **Hilos y Multitarea**:
    * `svcCreateThread`: Crea un nuevo hilo de ejecución en los núcleos de la CPU.
    * `svcSleepThread`: Cede tiempo de procesador y suspende el hilo actual durante un número determinado de nanosegundos.
    * `svcExitThread`: Finaliza la ejecución del hilo actual.
    * `svcGetThreadId`: Obtiene el identificador numérico de un hilo a partir de su *Handle*.
  * **Sincronización entre núcleos e hilos**:
    * `svcCreateEvent`: Crea un objeto de sincronización de eventos (manual o autorestart).
    * `svcWaitSynchronization1`: Bloquea el hilo hasta que un objeto de sincronización es señalado o expira el timeout.
    * `svcCreateAddressArbiter`: Mecanismo de sincronización ligero a nivel de dirección de memoria (futex del kernel de 3DS).
  * **Gestión de Memoria RAM**:
    * `svcControlMemory`: Asigna, libera o cambia los permisos de páginas de memoria virtual física (heap, stack).
    * `svcCreateMemoryBlock`: Crea bloques de memoria compartida.
  * **Control del Proceso**:
    * `svcExitProcess`: Cierra el ejecutable del juego y devuelve el control al menú Home de la 3DS.
    * `svcBreak`: Provoca una trampa de interrupción controlada para depuración o *panics*.
* **Relevancia en Matching**: Al ser funciones hoja (*leaf functions*) con patrones de registros fijos (cargar argumentos en `r0`-`r3`, código de interrupción y retorno), son los candidatos idóneos para lograr los primeros 100% matches exactos.

### 2.2. `ctr/nn/os` (Nintendo OS Subsystem)
* **Propósito**: Capa de abstracción del sistema operativo provista por Nintendo.
* **Componentes**:
  * **Página de Configuración del Sistema (`0x1FF80000`)**: Región de memoria mapeada en solo lectura donde el kernel expone información de la consola (idioma, región, modelo Old 3DS vs New 3DS). Por ejemplo, `func_001063F4` lee el offset `+0x40` de esta página para determinar capacidades de hardware.
  * **Sincronización por Spinlocks**: Funciones como `func_001274A0` implementan exclusión mutua de bajo nivel utilizando las instrucciones atómicas exclusivas de ARMv6K: `ldrex` (*load register exclusive*) y `strex` (*store register exclusive*).

### 2.3. `ctr/nn/y2r` (YUV to RGB Color Conversion Hardware)
* **Propósito**: Controlador del **acelerador de hardware de conversión de espacio de color**.
* **Fundamento**: Las cinemáticas pre-renderizadas (formato MobiClip) y las cámaras de la 3DS guardan las imágenes en formato **YUV / YCbCr** para ahorrar ancho de banda. La GPU PICA200 y el framebuffer requieren **RGB**.
* **Operación**: El hardware `Y2R` convierte flujos YUV a RGB de forma dedicada sin restar ciclos a la CPU principal. Incluye funciones de inicialización de buffers y enlace con el DSP de audio/vídeo (`func_001137C0`).

### 2.4. `ctr/nn/ndm` (Network Daemon Manager)
* **Propósito**: Gestión del demonio de comunicaciones inalámbricas.
* **Operación**: Controla los estados de la antena Wi-Fi, ahorro de energía, StreetPass en suspensión y conmutación entre modo ad-hoc local y conectividad de infraestructura.

### 2.5. `ctr/nn/nex` (Nintendo Network EXtension / Quazal Rendez-Vous)
* **Propósito**: Middleware de infraestructura de red online multijugador.
* **Operación**: Gestiona la autenticación en servidores de Nintendo Network, el emparejamiento de rivales (*matchmaking*), serialización de paquetes de red cifrados y sincronización de combates e intercambios Yo-kai en línea.

### 2.6. `ctr/crt` (C Runtime Startup)
* **Propósito**: Código de inicialización de bajo nivel.
* **Operación**: `clear_bss.s` ejecuta el bucle de puesta a cero de la sección `.bss` en RAM antes de transferir el flujo a `main()`.

---

## 3. Capa 2: Motor Propietario de Level-5 (`src/engine/`)

Son las librerías base desarrolladas por Level-5 para sus producciones de Nintendo 3DS (*Professor Layton*, *Inazuma Eleven GO*, *Yo-kai Watch*).

### 3.1. `engine/lfw` (Level-5 Framework)
* **Propósito**: El motor de ciclo de vida y **máquina de estados central**.
* **Arquitectura de Loops**:
  * Level-5 no utiliza un bucle de juego monolítico tradicional. En su lugar, utiliza una **Tabla de Descriptores de Bucles** (`LfwLoopClassInfo`) ubicada en la dirección virtual `0x00107478`.
  * Cada descriptor ocupa 12 bytes y define tres punteros a funciones polimórficas:
    ```c
    typedef struct LfwLoopClassInfo {
        void *(*createInstance)(void);  // Constructor del modo
        s32   (*getClassType)(void);    // ID de tipo
        const char *(*getClassName)(void); // Nombre en texto (ej. "ywCLoopBattle")
    } LfwLoopClassInfo;
    ```
  * `lfwCLoopEmpty`: Clase base para bucles nulos o de transición.

### 3.2. `engine/lxp` (Level-5 Cross-Platform / Memory Engine)
* **Propósito**: Gestor de recursos y asignación de memoria dinámica (`lxpCMemory`).
* **Fundamento**: En la Nintendo 3DS, con solo 128 MB de memoria física disponible para juegos convencionales, el uso continuo de `malloc` estándar genera fragmentación severa.
* **Operación**: Implementa *Memory Arenas* y *Pools* de tamaño predeterminado de los cuales se extraen y devuelven bloques contiguos a velocidad constante $O(1)$.

### 3.3. `engine/core`
* **Propósito**: Servicios utilitarios transversales: temporizadores de precisión, sincronización de frames a 30/60 FPS y operaciones matemáticas auxiliares.

---

## 4. Capa 3: Lógica Específica del Juego (`src/game/`)

Es la cúspide de la pirámide: el código donde se define la jugabilidad, combate y sistemas característicos de *Yo-kai Watch 2*.

### 4.1. `game/loops` (Implementaciones de Modos de Juego)
Cada modo del juego es una subclase concreta que se registra en la tabla de descriptores de `lfw`:
* **`ywCLoopRPG`**: Modo principal de exploración en Floridablanca y el pasado (movimiento del avatar, colisiones con el escenario, interacciones con NPCs).
* **`ywCLoopBattle`**: Sistema de combate táctico (gestión de la ruleta táctil de 6 Yo-kai, animaciones de espiritación y cálculo de animáximums).
* **`ywCLoopMenu`**: Menú del Yo-kai Pad, gestión del medallium, inventario de objetos y configuración.
* **`ywCLoopEvent`**: Intérprete de cinemáticas en tiempo real, diálogos scripteados y cámaras de eventos.
* **`ywCLoopCapsule`**: La máquina expendedora de cápsulas (*Expendekai / Gashapon*).
* **`ywCLoopOrgeTime`**: Minijuego de supervivencia y escape de la *Hora Terrorífica* frente a Gargaros (*Oni*).
* **`ywCLoopWatchmap`**: Sistema de radar del reloj Yo-kai y minimapa en pantalla táctil.
* **`ywCLoopQR`**: Escáner de medallas físicas coleccionables mediante las cámaras de la consola.

### 4.2. `game/core`
* **Propósito**: Reglas de negocio del juego: fórmulas de daño elemental, tablas de afinidad de espiritación, comprobación de estado de inventario y rutinas universales de saneamiento de datos (`func_0014A06C`).

---

## 5. Estrategia de Decompilación (Enfoque Bottom-Up)

Comprender la modularidad de *Yo-kai Watch 2* determina el orden táctico para lograr el 100% match:

```
[4. game/loops]  <-- Mayor complejidad (C++, objetos grandes, dependencias múltiples)
       ^
[3. engine/lfw]  <-- Nivel intermedio (tablas de despacho, memoria lxp)
       ^
[2. ctr/nn/os]   <-- Nivel accesible (lecturas MMIO, structs de sistema)
       ^
[1. ctr/svc]     <-- Punto de partida ideal (funciones hoja puras, match rápido)
```

1. **Fase 1 (Cimientos)**: Matchear todas las funciones hoja de `ctr/svc` y `ctr/crt`.
2. **Fase 2 (Subsistemas de hardware)**: Reconstruir `ctr/nn/os` y `ctr/nn/y2r`.
3. **Fase 3 (Estructuras de motor)**: Reconstruir las tablas de descriptores de `engine/lfw`.
4. **Fase 4 (Lógica de juego)**: Abordar las clases complejas de `game/loops` cuando los tipos base y punteros globales estén resueltos.

