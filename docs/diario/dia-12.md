# Diario de aprendiendo a decompilar en 358/2 dias - Dia 12: (Newsletter (parte 1))

### Info:
- **Fecha**: 8 de Octubre de 2026
- **Objetivo general de la sesión**: Empezar a planificar la fase 2 del proyecto y seguir desarrollando la newsletter
- **Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel

<img src="./diario-images/day-12.png" width="100%" alt="day-12 card">

---

## Empezando a escribir la newsletter

En este día ya he decidido qué estructura va a seguir la newsletter, la misma que tiene esta entrada:

```mermaid
graph TD
    A["📑 Entrada de Diario (.md)"] --> B["1. Info: (Fecha, Objetivo, Fase)"]
    A --> C["2. 🖼️ Tarjeta Gráfica (day-XX.png)"]
    A --> D["3. 📝 Reflexión y Momento Técnico (RAM / CPU / Retos)"]
    A --> E["4. ✅ Checklist: (Micro-objetivos alcanzados)"]
    A --> F["5. 🏷️ Tags: (#DecompilandoEn358Dias...)"]
```

Info: Resumen de la sesión, con fecha y demás, una especie de resumen rápido.

(Imagen de cabecera)

(Anécdota y resumen de la sesión)

(Checklist)

(Tags)

Esta estructura es obligatoria y tengo a Antigravity revisando que todas las entradas tengan esta estructura.

Mi idea es escribir un sistema universal que pueda llevar a cualquier sitio que admita meterle un fichero Markdown —que no son precisamente pocos—. Originalmente tenía pensado Substack, pero no me termina de convencer, así que probaré otras.

Mi idea es publicar de forma retroactiva todas y luego seguir por ahí, aunque me preocupa el formato: estas entradas de texto son muy densas y quiero hacerlas lo más legibles posible, así que no me extrañaría reestructurar entradas de forma retroactiva.

## Planificando la fase 2

Adicionalmente estoy empezando a planear mi banco de pruebas para la fase 2 del proyecto, en el que haré una prueba de decompilar parte de un software, aunque de eso hablaré más en profundidad más adelante.

```mermaid
flowchart LR
    ROM["🎮 Cartucho 3DS<br/>(NCSD .3ds)"] --> Part0["📦 Partición 0<br/>(NCCH Aplicación)"]
    Part0 --> ExeFS["📁 ExeFS<br/>(code.bin 4.42 MB)"]
    ExeFS --> Decomp["🔄 Descompresión<br/>FastLZSS / BLZ"]
    Decomp --> Raw["🎯 code.raw.bin<br/>(7.38 MB ARM11)"]
    Raw --> RAM["🧠 RAM CTR<br/>@ 0x00100000"]
```

Aunque bueno, lo podéis ver en el repo, creo que es un reto que me queda grande, pero no es mi intención decompilar el juego entero, sino que había pensado en algún Mario y Luigi.

Espero que el reto no me quede grande, lo veremos en su momento.

Nos vemos jeje.

### Checklist:

- [x] Empezar la implementación del sistema universal de notas en Markdown
- [x] Extracción de datos del juego de 3DS para su posterior análisis (De momento solo en el equipo local, posteriormente se hará un reto aparte)

### Tags:

#DecompilandoEn358Dias #Nintendo3DS #ARM11 #FastLZSS #YokaiWatch2 #ReverseEngineering #Newsletter
