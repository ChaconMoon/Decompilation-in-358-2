# Publicación de LinkedIn — Día 23: Estructurando el proyecto

> **Metadatos de Publicación**
> - **Red Social**: LinkedIn
> - **Fecha de publicación sugerida**: 20 de Octubre de 2026
> - **Entrada del diario relacionada**: [`docs/diario/dia-23.md`](../../diario/dia-23.md)
> - **Imagen adjunta recomendada**: [`docs/diario/diario-images/dia-23.png`](../../diario/diario-images/dia-23.png)
> - **Hashtag del reto**: `#DecompilandoEn358Dias`

---

## Texto para copiar y pegar en LinkedIn

¿Se pueden tardar 13 años en decompilar un videojuego de Nintendo 3DS?

Matemáticamente, sí.

Haciendo números esta semana en mi reto personal #DecompilandoEn358Dias:
Llevo 45 funciones verificadas byte a byte en Yo-kai Watch 2 (Mentespectros). Eso representa el 0,01% del ejecutable. A un ritmo puramente manual de 300 bytes al día, terminarlo me llevaría más de una década... y no entra en mis planes tirarme hasta los 36 picando ensamblador en solitario.

Pero esta semana alcancé un punto de inflexión clave: logré entender y estructurar la arquitectura modular del juego en 3 capas:

1️⃣ CTR-SDK (Nintendo): El diálogo directo con el microkernel de la 3DS, la gestión de memoria y la conversión de color por hardware (Y2R).
2️⃣ Engine (Level-5): El motor propietario que el estudio reutiliza en sagas como Inazuma Eleven o el Profesor Layton (máquinas de estado basadas en bucles y memory pools).
3️⃣ Game: La lógica real de combate táctico, exploración y eventos.

Además, analizando los binarios comerciales descubrí una genialidad de la ingeniería retro:
Fantasqueletos y Carnánimas son idénticos al 99,999987%. ¿La única diferencia en 7,5 MB de binario? Un solo byte en el offset 0x47B0 que actúa como selector de edición. Mentespectros, la edición definitiva, solo añade 241 KB de código para todas sus nuevas zonas y eventos.

Sobre el uso de IA y la ética profesional:
Para que un reto como este sea viable, utilizo IA (Gemini) como copiloto técnico. Pero me niego al "vibe-coding" o a pegar código que no comprendo. En mi repositorio he publicado una política formal de transparencia: cada función y cada nota técnica especifica con total honestidad qué porcentaje es autoría mía y qué parte ha sido asistida.

Como docente de informática tengo una máxima: si yo no lo entiendo a bajo nivel, no sirve. Decompilar no es solo hacer que el código coincida; es rescatar la artesanía del software.

El proyecto es de código abierto y podéis seguir el progreso diario en GitHub:
👉 https://github.com/ChaconMoon/Decompilation-in-358-2

¿Cómo gestionáis vosotros el equilibrio entre acelerar vuestro aprendizaje con IA y preservar la comprensión profunda de lo que programáis? Os leo en comentarios. 👇

#DecompilandoEn358Dias #ReverseEngineering #LowLevel #Nintendo3DS #CProgramming #CleanCode #SoftwareArchitecture #EdTech

---

## 💡 Recomendaciones para la publicación:
1. **Imagen**: Sube la tarjeta `docs/diario/diario-images/dia-23.png` como imagen principal del post.
2. **Primer comentario**: Puedes dejar un enlace directo a la entrada completa del diario en GitHub en el primer comentario para no penalizar el algoritmo de alcance del post principal.

