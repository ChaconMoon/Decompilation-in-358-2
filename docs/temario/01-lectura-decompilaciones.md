# Temario Detallado · Fase 1: Lectura y Anatomía de Decompilaciones Reales

La **Fase 1** marca tu entrada al mundo de la ingeniería inversa aplicada y a la comprensión de cómo se estructuran los proyectos de decompilación colaborativos modernos (bajo el estándar de [decomp.dev](https://decomp.dev/)).

---

## Bloque 1.1: Ecosistema y Estructura de Proyectos

### ¿Qué es una Decompilación Matching?
- A diferencia de una descompilación automática convencional con Ghidra o IDA Pro (que produce pseudo-código aproximado, a menudo ilegible o que no compila), una **matching decompilation** busca reconstruir el código fuente original en C de tal manera que, al pasarlo por el compilador histórico exacto, genere un archivo binario **idéntico byte por byte (100% match)** a la ROM original del cartucho.

### Anatomía de Directorios Típica
```
proyecto-decomp/
├── asm/            # Código desensamblado de funciones aún no migradas a C
├── src/            # Código C ya decompilado que compila byte-a-byte idéntico
├── include/        # Declaraciones compartidas de structs, enums y prototipos
├── config/         # Archivos de configuración de memoria, overlays y símbolos
├── tools/          # Compilador histórico emulado y scripts de verificación de diff
└── expected/       # Binario original extraído de la ROM para comparar
```

### Linker Scripts y Tablas de Símbolos
- **Linker Scripts (`.ld`)**: Indican al enlazador exactamente en qué dirección de memoria RAM debe ubicarse cada función y variable (ej. `0x02000000` en Nintendo DS).
- **Tablas de Símbolos (`syms.txt`)**: Listan la dirección exacta de cada función conocida en la ROM, permitiendo llamar a funciones aún no decompiladas mediante punteros globales.

---

## Bloque 1.2: Hardware de Nintendo DS para Lectores de C

### La Arquitectura Dual ARM
- **ARM946E-S (ARM9)**: Procesador principal a 67 MHz con memoria caché de instrucciones (8 KB) y caché de datos (4 KB). Ejecuta la lógica del juego, cálculo 3D, física y bucle de eventos.
- **ARM7TDMI (ARM7)**: Coprocesador a 33 MHz dedicado a la gestión del hardware de bajo nivel: chip de sonido, Wi-Fi, pantalla táctil y alimentación.

### Registros MMIO (Memory-Mapped I/O)
- En Nintendo DS, el hardware no se comunica mediante llamadas al sistema operativo (como en Windows o Linux), sino mediante **direcciones de memoria físicas especiales**:
  - `0x04000000`: Control de pantalla (`REG_DISPCNT`).
  - `0x04000130`: Registro de entrada de botones (`REG_KEYINPUT`).
- En C, esto se modela como punteros volátiles:
  ```c
  #define REG_KEYINPUT (*(volatile uint16_t *)0x04000130)
  ```
  La palabra clave `volatile` es fundamental: indica al compilador que el valor puede cambiar en cualquier momento por el hardware, evitando que optimice la lectura eliminándola.

### El Sistema de Overlays
- La Nintendo DS sólo dispone de 4 MB de memoria RAM principal.
- Para juegos grandes como *Kingdom Hearts 358/2 Days*, los desarrolladores dividieron el código en **Overlays**: archivos binarios individuales cargados dinámicamente desde el cartucho según la escena (ej. `ov000` para logos, `ov002` para Twilight Town, `ov006` para selección de personajes).

---

## Bloque 1.3: Lectura y Análisis de `khdays-decomp`

### Guía de Exploración de Código
1. **Punto de Entrada**: Inspeccionar la función de arranque en `src/boot/` y entender el paso de control de la BIOS de la consola al juego.
2. **Máquinas de Estado de Escena**: Estudiar la estructura del bucle de escenas: cómo el juego conmuta entre menús, cinemáticas y modo de batalla.
3. **Gestión de Entidades y Jugador**: Localizar el struct de Roxas (posición X,Y,Z en coma fija o punto flotante, animación activa, Keyblade equipada, puntos de vida).

### Hito de Validación de Fase 1
Elegirás un subsistema de *Kingdom Hearts 358/2 Days* o *Kingdom Hearts: Chain of Memories* y redactarás un documento técnico en `fase-1-lectura-decomp/analisis/` explicando su funcionamiento interno con diagramas de flujo y pseudo-código comentado.
