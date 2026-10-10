# Decompilation in 358-2

<p align="center">
  <img src="https://raw.githubusercontent.com/ChaconMoon/Decompilation-in-358-2/master/docs/diario/diario-images/day-13.png" alt="Reto 358/2 Días" width="85%">
</p>

<p align="center">
  <strong>El viaje formativo de 358,5 días para dominar C a bajo nivel, memoria física, arquitectura de CPU y matching decompilation de consolas retro.</strong>
</p>

<p align="center">
  <a href="#-fases-del-proyecto"><img src="https://img.shields.io/badge/Fase-0%20%C2%B7%20Cimientos%20de%20C-0052cc?style=for-the-badge" alt="Fase 0"></a>
  <a href="#-submódulos-y-repositorios"><img src="https://img.shields.io/badge/Subm%C3%B3dulo-Yo--kai%20Watch%202%20(3DS)-e11d48?style=for-the-badge" alt="Yo-kai Watch 2"></a>
  <a href="https://github.com/ChaconMoon/Decompilation-in-358-2"><img src="https://img.shields.io/badge/Hashtag-%23DecompilandoEn358Dias-7c3aed?style=for-the-badge" alt="Hashtag"></a>
  <a href="#-licencia-y-ética"><img src="https://img.shields.io/badge/Licencia-MIT-10b981?style=for-the-badge" alt="Licencia"></a>
</p>

---

## 📖 Acerca del Reto

* **Estudiante / Autor**: Carlos Chacón ([@ChaconMoon](https://github.com/ChaconMoon)), profesor de Formación Profesional de informática en España.
* **Duración oficial**: 358,5 días (del **27 de septiembre de 2026** al **21 de septiembre de 2027**).
* **Filosofía**: **Hábitos Atómicos**. Sesiones de estudio diarias enfocadas en 1 o 2 micro-objetivos medibles (15 a 45 minutos) para aprender de forma sólida sin saturación.
* **Bitácora y Devlog**: Documentación diaria con rigor de bajo nivel (RAM, CPU y ensamblador) en [`docs/diario/`](docs/diario/).

---

## 🏛️ Submódulos y Proyectos de Decompilación

El proyecto se estructura con una suite formativa principal y proyectos de ingeniería inversa vinculados como submódulos:

| Repositorio / Submódulo | Plataforma | CPU / Arquitectura | Estado | Propósito |
| :--- | :--- | :--- | :---: | :--- |
| **[Decompilation in 358-2](https://github.com/ChaconMoon/Decompilation-in-358-2)** *(Este repo)* | PC / Linux | x86_64 / Multiplataforma | 🟢 Activo | Repositorio maestro, temario, diario y ejercicios de bajo nivel. |
| **[Yo-kai Watch 2 Decompilation](https://github.com/ChaconMoon/yokai-watch-2-decompiled)** *(Submódulo)* | Nintendo 3DS | ARM11 MPCore @ 268 MHz (ARMv6K) | 🟡 Fase 2 (En pausa) | Matching byte-exact del motor de Level-5 (*Shin'uchi* / CTR). |
| **`Yokimitsuro/khdays-decomp`** *(Referencia)* | Nintendo DS | ARM946E-S @ 67 MHz (ARMv5TE) | 🔍 Referencia | Decompilación byte-exact de *Kingdom Hearts 358/2 Days*. |
| **`Yokimitsuro/khdays-port`** *(Referencia)* | PC / 3DS | C++20 / SDL3 / Vulkan | 🔍 Referencia | Source port nativo que consume la decompilación de DS. |

---

## 🗺️ Fases del Proyecto

El reto se divide en 5 grandes etapas estructuradas en la [**Hoja de Ruta Maestra (`docs/ROADMAP.md`)**](docs/ROADMAP.md):

1. **Fase 0 · Cimientos de C y Memoria de Bajo Nivel** *(Fase actual)*:
   * **Bloque 0.1** (Completado ✅): Punteros, paso por referencia, matrices 2D en memoria física (*Row-Major Order*), modularización (`.c` vs `.h`), testing unitario y *AddressSanitizer*. Proyecto: `runlog`.
   * **Bloque 0.2** (En curso 🚀): Cadenas y terminador nulo `\0`, estructuras (`struct`), enumeraciones (`enum`), padding de memoria y el sistema de paneles de KH.
   * **Bloque 0.3**: Gestión dinámica de memoria (`malloc`/`free`), punteros dobles y *Arena Allocators*.
   * **Bloque 0.4**: Manipulación de bits, *Endianness*, I/O binario y parser de cabeceras de ROMs de NDS.
2. **Fase 1 · Lectura y Anatomía de Decompilaciones Reales**:
   * Ecosistema decomp.dev, hardware de DS (ARM946E-S, MMIO, NitroSDK y Overlays).
3. **Fase 2 · Matching Decompilation (El Arte del 100% Match)**:
   * Ensamblador ARMv5TE y ARMv6K, calling conventions AAPCS, decomp.me, objdiff y submódulo de Yo-kai Watch 2.
4. **Fase 3 · Librerías Gráficas y Multimedia con SDL**:
   * Framebuffers 256×192, bucle a 60 FPS, entrada, audio e integración de Dear ImGui.
5. **Fase 4 · Source Ports Nativos a PC**:
   * Compilación nativa, arquitectura del port de PC de KH Days, decodificación NitroFS y modding en C/C++.

---

## 📂 Estructura del Repositorio

```text
.
├── Makefile                     # Orquestador maestro de compilación de ejercicios
├── AGENTS.md                    # Directrices y reglas de acompañamiento del tutor IA
├── docs/                        # Documentación técnica maestra
│   ├── ROADMAP.md               # Hoja de ruta con checklist de micro-objetivos
│   ├── contexto-proyecto.md     # Manifiesto, hardware y perfil del estudiante
│   ├── diario/                  # Devlog y diario de aprendizaje día a día
│   └── temario/                 # Apuntes de bajo nivel, memoria y ensamblador
├── fase-0-fundamentos-c/        # Ejercicios y proyectos de bajo nivel en C
│   ├── drills/                  # Prácticas de conceptos concretos (punteros, arrays, etc.)
│   └── proyectos/               # Proyectos modulares (p1-sensores, p2-calificador, p3-runlog)
├── fase-2-matching-decomp/      # Proyectos y scratches de matching decompilation
│   └── yokai-watch-2-decompiled # [Submódulo Git] Repo independiente de decompilación 3DS
└── tools/                       # Herramientas auxiliares del reto
    └── khdays-card/             # Generador web interactivo de tarjetas de redes
```

---

## 🛠️ Compilación y Verificación

Todo el código de ejercicios y proyectos se compila con estándares estrictos de la industria:
```bash
# Compilar todos los proyectos y drills con Make
make all

# Limpiar binarios y temporales
make clean
```
> Cada programa se compila con `-Wall -Wextra -Werror` y se testea con AddressSanitizer (`-fsanitize=address,undefined`) para garantizar ausencia total de memory leaks o comportamientos indefinidos.

---

## ⚖️ Política Legal y Ética

Este repositorio y sus submódulos **NUNCA alojan código comercial protegido por copyright, claves de cifrado ni ROMs de videojuegos**. 
* Toda la ingeniería inversa y matching decompilation se realiza con fines exclusivamente educativos y de preservación histórica.
* Cualquier extracción de binarios ejecutables requiere legalmente que el usuario proporcione su propia copia legítima del juego dumpeada desde su consola física personal.

---

<p align="center">
  Hecho con pasión por la preservación retro y el software artesanal.<br>
  <strong>#DecompilandoEn358Dias</strong>
</p>
