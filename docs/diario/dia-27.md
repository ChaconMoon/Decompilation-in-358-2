# Diario de aprendiendo a decompilar en 358/2 dias - Dia 27: (Clasificando estructuras)

### Info:

- **Fecha**: 23 de Octubre de 2026
- **Objetivo general de la sesión**: Aprender cómo se estructuran las clases finales en base a los métodos decompilados.
- **Fase**: Fase 0-1 · Práctica de Decomp Academy


<img src="./diario-images/dia-27.png" width="100%" alt="dia-27 card">

---

### Estructurando clases

Como siempre he dicho estoy aquí para aprender y aprender significa volver atrás y mejorar lo hecho, si es posible, y de hecho hoy he aprendido algo vital para mis proyectos de decompilación y es cómo se estructuran, es decir cómo se hace un proyecto profesional, eso lo explicaré a continuación.

#### De funciones a estructuras.

Cuando empecé a decompilar Yokai Watch 2 empecé decompilando funciones sueltas como aprendí en Decomp.dev, es decir: dirección de memoria `0x00340CE8` recibe un número de parámetros con una longitud en concreto y devuelve algo, un comportamiento normal, pero eso son solo funciones sueltas. Aquí entra mi criterio de decir, vale, mientras reciba la misma cantidad de parámetros y devuelva lo indicado todo OK, pero un proyecto no se construye solo en base a enteros de 32 bits o de 16 bits o una posición a memoria, pero una posición de memoria es también una estructura, por lo que lo ideal es devolver una estructura, es más, es lo que debemos hacer, así que a llamar todo mediante estructuras en los headers. De ahí el origen de los ficheros .h

#### De estructuras a clases.

C no soporta programación orientada a objetos, por eso toca tirar de estructuras, una estructura no deja de ser 2 valores juntos puestos en una posición de memoria, eso me recuerda, de momento usaré números hexadecimales en lugar de los decimales, sé que se usan en diferentes contextos, pero aún no lo tengo muy claro en qué caso se usa cada uno, así que de momento lo dejaré en hexadecimal por si acaso, cuando sepa cuándo usar cada uno lo revisaré.

Pero por fin he conseguido lo que se espera de una decompilación, el código final, he recompilado una clase entera, la clase NexElement del CTR-SDK ([NexElement.cpp](../../fase-2-matching-decomp/yokai-watch-2-decompiled/src/ctr/nn/nex/NexElement.cpp)), esta clase no tiene mucho, varios constructores y destructores, pero me ha servido para por fin conseguir estructurar una clase real como se verá en la decompilación final, por cierto no he avanzado, solo la he reestructurado, pero la funcionalidad es la misma solo que ahora la estructura es correcta.

He decidido que a partir de ahora empezaré a decompilar por clases, básicamente es lo que he visto que se hace en decompilaciones como la de Animal Crossing New Leaf, así que creo que es lo ideal, pero aún no sé cuál es la siguiente, pero seguiré. Por cierto hay una clase con 2000 funciones que me está dando algo de mala espina. Además por el nombre no sé qué hace. XD.


### Despedida.

No tengo mucho más que decir, la decompilación no ha avanzado como tal, pero sí que lo que he aprendido me va a ser extremadamente útil y me permitirá decompilar de forma más fluida, espero tardar menos en decompilar la siguiente clase.

Por último, ajeno a este proyecto me he hecho una especie de entorno de pruebas, en el que podré trastear decompilando software, sin que afecte al proyecto de Yo-kai Watch 2. Si veo que de ese campo de pruebas saco algo interesante lo haré público, si noooo. Bueno se quedará en mi PC.

Seguiré informando.

---

### Checklist:

- [x] Pasar de pensar en funciones sueltas a pensar en estructuras y clases.
- [x] Reestructurar los métodos de `0x00340CE8` en una clase C++ real: `NexElement` en `src/ctr/nn/nex/NexElement.cpp`.
- [x] Definir la estructura y cabecera de la clase en `include/ctr/nex.h`.
- [x] Decidir el flujo de trabajo para las siguientes sesiones: decompilar agrupando por clases como en Animal Crossing.
- [x] Montar un entorno de pruebas privado y aislado para trastear con decompilación sin ensuciar Yo-kai Watch 2.

---

### Tags:

#DecompilandoEn358Dias #BajoNivel #ReverseEngineering #Nintendo3DS #ARM11 #MemoriaRAM #IngenieriaInversa #CleanCode #FPInformatica
