# Diario de Aprendizaje · Día 12
**Fecha**: 8 de Octubre de 2026  
**Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel  
**Módulos**: Proyecto Independiente (*Yo-kai Watch 2*), Newsletter Substack y Fundamentos  
**Hito**: Integración de Yo-kai Watch 2 (3DS), Arquitectura de Newsletter y Entrada Fundacional Día 1

---

## 🎯 Objetivos de la Sesión
- [x] Commit oficial y cerrado de la jornada previa: `Day-11: Modularización en C, include guards y suite de tests unitarios con sanitizers`.
- [x] Integración de **_Yo-kai Watch 2: Mentespectros_ (Nintendo 3DS)** como proyecto objetivo independiente de decompilación en [`docs/contexto-proyecto.md`](../contexto-proyecto.md).
- [x] Reubicación del proyecto a [`fase-2-matching-decomp/yokai-watch-2-decompiled/`](../../fase-2-matching-decomp/yokai-watch-2-decompiled/) con estructura modular (`config/`, `tools/`, `asm/`, `src/`, `include/`, `scratches/`).
- [x] Implementación del pipeline de extracción en [`tools/extract_rom.py`](../../fase-2-matching-decomp/yokai-watch-2-decompiled/tools/extract_rom.py) y [`Makefile`](../../fase-2-matching-decomp/yokai-watch-2-decompiled/Makefile).
- [x] Blindaje estricto en `.gitignore` para excluir ROMs (`.3ds`), ejecutables (`.code`, `.bin`, `.raw`) y directorios temporales de Git.
- [x] Extracción y descompresión verificada de `.code` (4.42 MB) a `extracted/code.raw.bin` (7.38 MB, ARM11 @ `0x00100000`) con FastLZSS.
- [x] Cálculo y registro del SHA-256 oficial del ejecutable: `b536dfce0a7138f2d5691532604d782b1ea3e20731120cc662baee118c370547`.
- [x] Inspección de símbolos del motor de Level-5 (`CHARA_BASE_YOKAI_INFO`, `BTL_YOKAI_FAMILY_INFO`, `SoulCombi`, `RWSTDERR`).
- [x] Definición de la línea editorial híbrida (Semanal + Hitos) para la newsletter pública en [`docs/newsletter/guia-editorial.md`](../newsletter/guia-editorial.md).
- [x] Implementación y testeo del script de exportación automatizada a Substack en [`tools/newsletter/export_substack.py`](../../tools/newsletter/export_substack.py) con filtrado de notas privadas.
- [x] Creación, revisión y pulido de la entrada retroactiva del [`docs/diario/dia-1.md`](dia-1.md) ("La llave que guiará mi destino") integrando su tarjeta gráfica en [`docs/diario/diario-images/day-1.png`](diario-images/day-1.png).

---

## 🧠 Conceptos Clave de Arquitectura e Ingeniería Inversa

### 1. La Arquitectura de Nintendo 3DS frente a Nintendo DS
- **Hardware y CPU**:
  - Mientras que Nintendo DS se basa en un procesador ARM946E-S (arquitectura ARMv5TE a 67 MHz), Nintendo 3DS incorpora un procesador principal **ARM11 MPCore (arquitectura ARMv6K a 268 MHz)** de doble núcleo, con un ARM9 subordinado a tareas de seguridad y compatibilidad.
- **Sinergia en Calling Conventions (AAPCS)**:
  - Pese al salto de generación, ambas arquitecturas siguen el estándar **AAPCS (ARM Architecture Procedure Call Standard)**:
    - Argumentos de funciones: pasan en `r0`-`r3`.
    - Valor de retorno: viaja en `r0`.
    - Registros `r4`-`r11`: preservados por la función llamada mediante la pila (`push`/`pop` o `stmfd`/`ldmfd`).
    - Registros especiales: `sp` (`r13`, Stack Pointer), `lr` (`r14`, Link Register) y `pc` (`r15`, Program Counter).
  - Los fundamentos de memoria, punteros y structs que estamos aprendiendo en C son **directamente aplicables** al análisis del ejecutable de 3DS.

### 2. Pipeline de Binarios en 3DS (GodMode9 → ExeFS → `.code` → `code.raw.bin`)
- Una ROM de 3DS (`.3ds` / `.cia`) almacena el código ejecutable en la partición **ExeFS**.
- El archivo ejecutable principal es `.code` (comprimido con FastLZSS / BLZ invertido de Nintendo).
- Al descomprimir `.code` (4.42 MB), el ejecutable se expande a **7.38 MB (7.737.344 bytes)** cargado en la dirección virtual base **`0x00100000`** para ARM11.
- La presencia de cadenas de la biblioteca Rogue Wave (`RWSTDERR`) confirma la compilación con **ARM Compiler (RVCT / `armcc`)**.
- Este proyecto queda formalmente preparado y en reposo para retomarse con la decompilación activa cuando alcancemos la **Fase 2**.

### 3. Modelo Editorial Híbrido (Bitácora Interna vs Publicación en Substack)
- **Desacoplamiento**: El diario en `docs/diario/dia-XX.md` sirve como registro técnico atómico diario de 15–45 min sin fricción.
- **Publicación consolidada**: La newsletter en Substack se alimenta de estas entradas para generar ensayos técnicos semanales o por hitos completados, aportando valor formativo real a la comunidad sin riesgo de saturación.

---

## 📝 Mis Notas y Reflexiones (Espacio para editar)
*(Escribe aquí tus conclusiones personales antes de la siguiente sesión)*

- 

---

## 🚀 Próximos Pasos (Planificación para el Día 13)
- [ ] **Arranque del Bloque 0.2 de C (Cadenas y Memoria)**:
  - Resolver **0.2.1**: Arrays de caracteres y demostración práctica del terminador nulo `\0` en `fase-0-fundamentos-c/drills/cap07-strings/`.
  - Resolver **0.2.2**: Implementar `mi_strlen()` y `mi_strcmp()` mediante aritmética de punteros `const char *s`.
- [ ] **Revisión y Lanzamiento de la Newsletter**: Pulir las entradas acumuladas del diario con el objetivo de publicar la primera edición completa de cara al Día 13.
- [ ] *(Fase 2 - En pausa hasta alcanzar la fase)*: Análisis estático de `code.raw.bin` y primeros scratches en decomp.me.

---

## 📦 Commit de GitHub
```text
Day-12: Pipeline de decompilación para Yo-kai Watch 2 (3DS) en Fase 2, descompresión de .code y newsletter
```
