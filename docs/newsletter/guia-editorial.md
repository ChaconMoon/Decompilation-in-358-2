# Guía Editorial: Newsletter del Reto #DecompilandoEn358Dias

Esta guía establece los criterios de redacción, tono y arquitectura de publicación para la newsletter oficial en **Substack**.

---

## 1. Misión y Filosofía Editorial

- **Estrategia Híbrida (Semanal + Hitos Clave)**:
  - **Día a día (Bitácora Interna)**: Cada jornada de trabajo se registra en `docs/diario/dia-XX.md` con enfoque en micro-objetivos atómicos (15–45 min), depuración de código y notas técnicas.
  - **Entrega Pública en Substack**: Se publica **1 vez por semana** (Resumen semanal / *Weekly Digest*) o **al culminar un hito importante** de la hoja de ruta (ej. Cierre del Bloque 0.1, extracción de la ROM de 3DS, primer 100% match).
  - **Ventaja**: Elimina la fatiga diaria y permite entregar artículos con narrativa sólida, código pulido y valor formativo real.

- **Voz y Tono**:
  - **El Profe en la Trinchera**: Eres un profesor de FP de informática que también se sienta a aprender y ensuciarse las manos con ensamblador y bajo nivel. Tono humilde, curioso, pedagógico y sin tecnicismos innecesarios.
  - **Enfoque Físico ("Bajo el Capó")**: No explicar solo la sintaxis abstracta; explicar siempre la RAM física, la CPU (ARM), los registros y por qué ocurren los fallos.
  - **Cultura Gamer / Consolas**: Conectar los problemas con juegos reales: *Kingdom Hearts 358/2 Days* (Nintendo DS) y *Yo-kai Watch 2: Mentespectros* (Nintendo 3DS).

---

## 2. Estructura Fija de cada Edición

Cada número en Substack sigue un formato de **5 bloques reconocibles**:

1. **El Gancho (Hook / Introducción)**:
   - Una anécdota del aula o del teclado, una pregunta provocadora o un error común que rompe juegos.
2. **Bajo el Capó (El Concepto de la Semana)**:
   - Explicación visual y sencilla de un concepto de memoria (ej. *Row-Major order*, *terminador nulo `\0`*, *padding de structs*, *AAPCS en ARM*).
   - Uso de diagramas esquemáticos en texto.
3. **En la Trinchera (El Reto Técnico y el Bug Resuelto)**:
   - Fragmento de código C real (máx. 15–25 líneas).
   - El caso borde: *"El bug que casi me vuelve loco y qué nos enseñó sobre la máquina"*.
4. **Conexión Consolas (NDS / 3DS)**:
   - Cómo se refleja esto en hardware real: ARM9 vs ARM11, lectura de cabeceras, tablas de nombres o decompilación en [decomp.me](https://decomp.me/).
5. **Píldora Pedagógica y Tarjeta del Reto**:
   - Una reflexión sobre el aprendizaje continuo y hábitos atómicos.
   - Imagen de la tarjeta exportada con `tools/khdays-card`.
   - Enlace al repositorio de GitHub y llamada a suscribirse.

---

## 3. Tooling Automatizado

Para generar borradores listos para Substack a partir de las entradas del diario:

```bash
# Exportar una edición recopilatoria indicando rango de días
python3 tools/newsletter/export_substack.py --desde 1 --hasta 11 --titulo "De Cero a Modularizar con Sanitizers en C"

# Exportar un hito concreto
python3 tools/newsletter/export_substack.py --hito "0.1" --titulo "Hito 0.1: Speedrunning, Punteros y Tests Unitarios"
```

El script genera un archivo `.md` optimizado en `docs/newsletter/publicaciones/` con formato limpio para copiar y pegar directamente en el editor de Substack.
