#!/usr/bin/env python3
"""
tools/newsletter/export_substack.py

Generador de borradores para Substack a partir de las entradas del diario
en docs/diario/dia-XX.md.

Uso:
    python3 tools/newsletter/export_substack.py --desde 10 --hasta 11 --titulo "Cierre del Bloque 0.1: Dominando Punteros y Tests Unitarios"
    python3 tools/newsletter/export_substack.py --hito "0.1" --titulo "Hito 0.1: De Cero a un Sistema de Speedrunning en C"
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIARIO_DIR = REPO_ROOT / "docs" / "diario"
OUTPUT_DIR = REPO_ROOT / "docs" / "newsletter" / "publicaciones"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Compila entradas del diario en un borrador de Substack."
    )
    parser.add_argument("--desde", type=int, help="Día de inicio del rango (ej. 1)")
    parser.add_argument("--hasta", type=int, help="Día de fin del rango (ej. 11)")
    parser.add_argument("--hito", type=str, help="Identificador del hito (ej. 0.1)")
    parser.add_argument("--titulo", type=str, required=True, help="Título del artículo")
    parser.add_argument("--salida", type=str, help="Nombre del archivo de salida")
    return parser.parse_args()


def get_diary_files(desde=None, hasta=None):
    """Busca archivos dia-XX.md en el rango de días especificado."""
    if not DIARIO_DIR.exists():
        return []

    available = []
    for f in DIARIO_DIR.glob("dia-*.md"):
        m = re.match(r"dia-(\d+)\.md", f.name)
        if m:
            day_num = int(m.group(1))
            if desde is not None and day_num < desde:
                continue
            if hasta is not None and day_num > hasta:
                continue
            available.append((day_num, f))

    available.sort(key=lambda x: x[0])
    return [f for _, f in available]


def extract_sections_from_diary(file_path):
    """Extrae bloques temáticos ignorando notas privadas."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    day_match = re.search(r"dia-(\d+)", file_path.name, re.IGNORECASE)
    if not day_match:
        day_match = re.search(r"Día\s*(\d+)", content)
    day_num = day_match.group(1) if day_match else "?"

    extracted = {
        "day": day_num,
        "objectives": [],
        "concepts": [],
        "review": [],
        "commits": [],
    }

    current_section = None
    buffer = []

    def flush_section():
        nonlocal current_section, buffer
        if not current_section:
            return
        text = "\n".join(buffer).strip()
        if not text:
            buffer = []
            return

        if "objetivos" in current_section.lower():
            extracted["objectives"].append(text)
        elif "conceptos" in current_section.lower() or "bajo nivel" in current_section.lower():
            extracted["concepts"].append(text)
        elif "revisión" in current_section.lower() or "casos borde" in current_section.lower():
            extracted["review"].append(text)
        elif "commit" in current_section.lower():
            extracted["commits"].append(text)

        buffer = []

    for line in lines:
        if line.startswith("## "):
            flush_section()
            header = line[3:].strip()
            # Ignorar sección privada de notas y próximos pasos
            if "mis notas" in header.lower() or "próximos pasos" in header.lower():
                current_section = None
            else:
                current_section = header
        elif current_section is not None:
            buffer.append(line)

    flush_section()
    return extracted


def build_newsletter_draft(titulo, hito, dias_info, files_parsed):
    """Construye el contenido en formato Markdown listo para Substack."""
    rango_dias_str = ""
    if len(files_parsed) == 1:
        rango_dias_str = f"Día {files_parsed[0]['day']}"
    elif len(files_parsed) > 1:
        rango_dias_str = f"Días {files_parsed[0]['day']} al {files_parsed[-1]['day']}"
    else:
        rango_dias_str = "Entrega Especial"

    draft = []
    draft.append(f"# {titulo}")
    draft.append(f"*Crónicas de un profesor de FP aprendiendo C a bajo nivel, memoria y decompilación*")
    draft.append("")
    draft.append(f"> 📅 **Período**: {rango_dias_str} | 🏷️ **Reto**: `#DecompilandoEn358Dias`" + (f" | 🎯 **Hito**: Bloque {hito}" if hito else ""))
    draft.append("")
    draft.append("---")
    draft.append("")

    # 1. El Gancho
    draft.append("## 🎣 1. El Gancho: La trinchera del aula y la pantalla negra")
    draft.append(
        "Cuando enseñas programación a diario, es fácil acostumbrarse a las comodidades de los lenguajes modernos. "
        "Pero cuando decides quitar las ruedas de entrenamiento y mirar qué ocurre físicamente dentro de la memoria "
        "y el procesador de una consola retro, el mundo cambia por completo."
    )
    draft.append("")
    draft.append(
        "En esta entrega recapitulamos los avances recientes de nuestro viaje de 358,5 días para dominar C y decompilar "
        "videojuegos legendarios desde sus entrañas."
    )
    draft.append("")

    # 2. Bajo el Capó
    draft.append("## 🧠 2. Bajo el Capó: Lo que la CPU y la RAM nos enseñaron")
    if files_parsed:
        for item in files_parsed:
            if item["concepts"]:
                draft.append(f"### 📍 Conceptos Clave (Día {item['day']})")
                draft.append("\n\n".join(item["concepts"]))
                draft.append("")
    else:
        draft.append("*(Inserta aquí la explicación técnica del concepto central con diagramas de memoria)*\n")

    # 3. En la Trinchera
    draft.append("## 🛠️ 3. En la Trinchera: El código y los bugs que casi nos vuelven locos")
    if files_parsed:
        for item in files_parsed:
            if item["review"]:
                draft.append(f"### 🔍 Auditoría y depuración (Día {item['day']})")
                draft.append("\n\n".join(item["review"]))
                draft.append("")
    draft.append(
        "Uno de los mayores aprendizajes al trabajar a bajo nivel es que el compilador no siempre te salvará: "
        "la disciplina de compilar con `-Wall -Wextra -Werror` y apoyar los tests con `-fsanitize=address,undefined` "
        "convierte horas de depuración a ciegas en fallos inmediatos y reproducibles."
    )
    draft.append("")

    # 4. Conexión Gamer
    draft.append("## 🎮 4. Conexión Gamer: De Nintendo DS a Nintendo 3DS")
    draft.append(
        "- **Nintendo DS (Kingdom Hearts 358/2 Days)**: Nuestro laboratorio de referencia con el procesador ARM946E-S. "
        "Observamos cómo la convención de llamadas AAPCS y la disposición contigua de memoria organizan las misiones y estados de Roxas."
    )
    draft.append(
        "- **Nintendo 3DS (Yo-kai Watch 2: Mentespectros)**: Nuestro gran proyecto independiente de ingeniería inversa. "
        "La CPU ARM11 MPCore comparte las mismas convenciones y arquitectura base de registros, preparando el terreno "
        "para cuando extraigamos y analicemos el ejecutable `code.bin`."
    )
    draft.append("")

    # 5. La Píldora del Profe & Cierre
    draft.append("## 🎓 5. La Píldora del Profe: Hábitos Atómicos y Aprendizaje Continuo")
    draft.append(
        "Aprender decompilación no es cuestión de sentarse 8 horas un fin de semana a leer documentación árida; "
        "es el resultado acumulativo de micro-retos de 30 minutos al día. Si un concepto parece inabordable, "
        "se trocea hasta que quepa en la palma de la mano."
    )
    draft.append("")
    draft.append("---")
    draft.append("")
    draft.append("### 📊 Estado del Reto y Código Fuente")
    draft.append("- 💻 **Repositorio en GitHub**: [Decompilation in 358-2](https://github.com/) *(Actualizado diariamente)*")
    draft.append("- 🏷️ **Hashtag de seguimiento en redes**: `#DecompilandoEn358Dias`")
    draft.append("")
    draft.append("*¡Nos vemos en la siguiente entrega bajo el capó!*")

    return "\n".join(draft)


def main():
    args = parse_arguments()
    files = get_diary_files(args.desde, args.hasta)

    if not files and (args.desde is not None or args.hasta is not None):
        print(f"⚠️ No se encontraron archivos de diario en el rango especificado ({args.desde} a {args.hasta}).")
        print("Buscando todos los diarios disponibles...")
        files = get_diary_files()

    parsed = [extract_sections_from_diary(f) for f in files]

    content = build_newsletter_draft(
        titulo=args.titulo,
        hito=args.hito,
        dias_info=f"{args.desde}-{args.hasta}" if args.desde else None,
        files_parsed=parsed,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.salida:
        out_name = args.salida
        if not out_name.endswith(".md"):
            out_name += ".md"
    else:
        slug = re.sub(r"[^\w\s-]", "", args.titulo.lower()).strip()
        slug = re.sub(r"[-\s]+", "-", slug)
        out_name = f"newsletter-{slug[:40]}.md"

    out_file = OUTPUT_DIR / out_name
    out_file.write_text(content, encoding="utf-8")

    print(f"✅ Borrador para Substack generado exitosamente:")
    print(f"   📄 Archivo: {out_file.relative_to(REPO_ROOT)}")
    print(f"   📝 Entradas de diario procesadas: {len(parsed)}")


if __name__ == "__main__":
    main()
