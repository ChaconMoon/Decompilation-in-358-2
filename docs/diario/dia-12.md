# Diario de Aprendizaje · Día 12
**Fecha**: 8 de Octubre de 2026  
**Fase**: Fase 0 · Cimientos de C y Memoria de Bajo Nivel  
**Módulos**: Proyecto Independiente (*Yo-kai Watch 2*), Newsletter Substack y Fundamentos  
**Hito**: Integración de Yo-kai Watch 2 (3DS), Arquitectura de Newsletter y Entrada Fundacional Día 1

---

## 🎯 Objetivos de la Sesión
- [x] Commit oficial y cerrado de la jornada previa: `Day-11: Modularización en C, include guards y suite de tests unitarios con sanitizers`.
- [x] Integración de **_Yo-kai Watch 2: Mentespectros_ (Nintendo 3DS)** como proyecto objetivo independiente de decompilación en [`docs/contexto-proyecto.md`](../contexto-proyecto.md).
- [x] Elaboración de la hoja de ruta y especificación técnica de ingeniería inversa para 3DS en [`docs/proyectos/yokai-watch-2/README.md`](../proyectos/yokai-watch-2/README.md).
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

### 2. Pipeline de Binarios en 3DS (GodMode9 → ExeFS → `code.bin`)
- Una ROM de 3DS (`.3ds` / `.cia`) almacena el código ejecutable en la partición **ExeFS**.
- El archivo ejecutable principal es `code.bin` (habitualmente comprimido mediante la variante Nintendo Extended LZSS / BLZ) junto con `exheader.bin` (que define el tamaño de stack y privilegios del sistema operativo).
- Descomprimir `code.bin` genera el binario plano ARM11 cargado en la dirección base `0x00100000` para su posterior análisis estático (Ghidra, IDA Pro o decomp.me).

### 3. Modelo Editorial Híbrido (Bitácora Interna vs Publicación en Substack)
- **Desacoplamiento**: El diario en `docs/diario/dia-XX.md` sirve como registro técnico atómico diario de 15–45 min sin fricción.
- **Publicación consolidada**: La newsletter en Substack se alimenta de estas entradas para generar ensayos técnicos semanales o por hitos completados, aportando valor formativo real a la comunidad sin riesgo de saturación.

---

## 📝 Mis Notas y Reflexiones (Espacio para editar)
*(Escribe aquí tus conclusiones personales antes de la siguiente sesión)*

- 

---

## 🚀 Próximos Pasos (Planificación para el Día 13)
- [ ] **Revisión y publicación de la Newsletter**: Revisar y pulir las entradas acumuladas del diario con el objetivo de publicar la primera edición completa de cara al Día 13.
- [ ] **Arranque del Bloque 0.2 de C (Cadenas y Memoria)**:
  - Resolver **0.2.1**: Arrays de caracteres y demostración práctica del terminador nulo `\0`.
  - Resolver **0.2.2**: Implementar `mi_strlen()` y `mi_strcmp()` mediante aritmética de punteros `const char *s`.
- [ ] **Recepción de la ROM de 3DS**: Extraer `code.bin` y verificar las cabeceras una vez concluido el volcado legal de la consola.

---

## 📦 Commit de GitHub
```text
Day-12: Integración de Yo-kai Watch 2 (3DS), sistema de newsletter para Substack y pulido de entrada Día 1
```
