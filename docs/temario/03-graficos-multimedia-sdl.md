# Temario Detallado · Fase 3: Librerías Gráficas y Multimedia con SDL (El Puente a PC)

La **Fase 3** te enseña la tecnología necesaria para construir un **Source Port**: cómo tomar el código de un juego que originalmente dependía de los chips gráficos de una consola y adaptarlo para que se ejecute en un ordenador moderno con una ventana gráfica, sonido y controles.

---

## Bloque 3.1: Arquitectura de SDL (SDL2 y SDL3)

### ¿Por qué SDL?
- Simple DirectMedia Layer (SDL) es la biblioteca multiplataforma estándar en C utilizada por ports de juegos comerciales (Doom, Quake, Sonic CD, Mario 64 PC Port, Zelda Ship of Harkinian). Proporciona una interfaz unificada para:
  - Creación y gestión de ventanas nativas (X11/Wayland en Linux, Win32 en Windows, Cocoa en macOS).
  - Inicialización acelerada por GPU o por software.
  - Gestión de eventos de entrada (teclado, ratón, gamepads modernos con soporte háptico).
  - Salida de audio sin latencia.

### El Game Loop Canónico en C
```c
int ejecutando = 1;
SDL_Event evento;
const u32 MS_POR_FRAME = 1000 / 60; // 60 FPS fijos (~16.6ms)

while (ejecutando) {
    u32 tiempo_inicio = SDL_GetTicks();

    // 1. Procesar eventos (Input)
    while (SDL_PollEvent(&evento)) {
        if (evento.type == SDL_QUIT) ejecutando = 0;
    }

    // 2. Actualizar lógica del juego (Update)
    actualizar_logica();

    // 3. Renderizar pantalla (Render)
    renderizar_graficos();

    // 4. Control de tiempo (Frame pacing)
    u32 tiempo_transcurrido = SDL_GetTicks() - tiempo_inicio;
    if (tiempo_transcurrido < MS_POR_FRAME) {
        SDL_Delay(MS_POR_FRAME - tiempo_transcurrido);
    }
}
```

---

## Bloque 3.2: Framebuffers Retro y Renderizado 2D

### Simular una Pantalla de Nintendo DS
- La pantalla de una Nintendo DS tiene una resolución nativa de **256×192 píxeles**.
- En SDL, podemos crear una textura en memoria que represente exactamente este buffer de píxeles:
  ```c
  SDL_Texture *framebuffer = SDL_CreateTexture(
      renderer,
      SDL_PIXELFORMAT_RGBA8888,
      SDL_TEXTUREACCESS_STREAMING,
      256, 192
  );
  ```
- Al final de cada frame, copiamos nuestro array de píxeles en la textura con `SDL_UpdateTexture()` y la dibujamos escalada a la ventana completa con `SDL_RenderCopy()`. Esto permite jugar en monitores modernos a 1080p o 4K conservando el pixel art original o aplicando filtros.

---

## Bloque 3.3: Entrada, Audio y Dear ImGui

### Mapeo de Mandos con `SDL_Gamepad`
- Nintendo DS cuenta con: D-Pad (4 direcciones), botones A, B, X, Y, L, R, Start y Select.
- Crearemos una capa de abstracción de entrada que convierta las pulsaciones del teclado de PC o de un mando de Xbox/PlayStation al formato de bits del registro de botones original (`REG_KEYINPUT`).

### Overlays de Depuración con Dear ImGui
- Dear ImGui es una librería ligera de interfaz gráfica inmediata. Integrada en nuestra ventana SDL, nos permite crear menús de desarrollo superpuestos:
  - Cambiar la velocidad del juego (cámara lenta / avance rápido).
  - Ver el mapa de memoria en tiempo real (visores de variables y structs de personajes).
  - Activar modos de depuración (invencibilidad, selector de salas).

### Hito de Validación de Fase 3
Crear el **`mini-visor-kh`**: una pequeña aplicación en C/SDL que cargue un sprite o textura de *Kingdom Hearts 358/2 Days*, lo pinte en pantalla y permita mover la cámara con el teclado.
