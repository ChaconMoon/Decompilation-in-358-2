#!/usr/bin/env python3
"""
tools/newsletter/publish_devto.py

Sube o actualiza entradas del diario a Dev.to como borradores (drafts) para revisión manual.
- Agrupa automáticamente las entregas en la serie "Decompilando en 358 Días".
- Asigna la tarjeta del día como imagen de portada (main_image).
- Transforma rutas relativas a URLs públicas de GitHub.
- NUNCA publica automáticamente: siempre se crea como 'published: false'.

Uso:
    python3 tools/newsletter/publish_devto.py --dia 1
    python3 tools/newsletter/publish_devto.py --dia 10
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIARIO_DIR = REPO_ROOT / "docs" / "diario"
ENV_PATH = REPO_ROOT / ".env"
DEVTO_API_URL = "https://dev.to/api/articles"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ChaconMoon/Decompilation-in-358-2/master/docs/diario/"
GITHUB_REPO_BLOB = "https://github.com/ChaconMoon/Decompilation-in-358-2/blob/master/"
GITHUB_REPO_TREE = "https://github.com/ChaconMoon/Decompilation-in-358-2/tree/master/"


def get_api_key():
    """Obtiene la API key de Dev.to desde .env o el entorno."""
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("DEVTO_API_KEY"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")

    key = os.environ.get("DEVTO_API_KEY")
    if key:
        return key.strip().strip('"').strip("'")

    return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sube una entrada del diario a Dev.to como borrador (draft)."
    )
    parser.add_argument("--dia", type=int, help="Número de día del diario (ej: 1, 10)")
    parser.add_argument("--archivo", type=str, help="Ruta al archivo Markdown")
    return parser.parse_args()


def sanitize_tag(tag):
    """Limpia un tag para cumplir con las restricciones de Dev.to (alfanumérico, sin espacios ni caracteres especiales)."""
    tag = tag.lower().replace("#", "").strip()
    tag = re.sub(r"[^a-z0-9]", "", tag)
    return tag[:20]


def prepare_devto_article(content, dia_num=None):
    """Prepara el título, portada, etiquetas y cuerpo en Markdown optimizado para Dev.to."""
    lines = content.splitlines()
    title = "Diario de decompilación"
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    if dia_num is None:
        dia_match = re.search(r"Dia\s+(\d+)", title, re.IGNORECASE)
        if dia_match:
            dia_num = int(dia_match.group(1))

    # Portada oficial de Dev.to a partir de la tarjeta gráfica
    cover_image = f"{GITHUB_RAW_BASE}diario-images/day-{dia_num}.png" if dia_num is not None else None

    # Extraer tags y normalizarlos para Dev.to (máximo 4 tags)
    tags = []
    tags_match = re.search(r"### Tags:\s*\n([^\n#]*#.*)", content)
    if tags_match:
        raw_tags = re.findall(r"#([\w-]+)", tags_match.group(1))
        for t in raw_tags:
            clean = sanitize_tag(t)
            if clean and clean not in tags and clean not in ["decompilandoen358dias"]:
                tags.append(clean)

    # Asegurar tags relevantes de programación si faltan
    default_tags = ["c", "gamedev", "programming", "reverseengineering"]
    for dt in default_tags:
        if len(tags) < 4 and dt not in tags:
            tags.append(dt)
    tags = tags[:4]

    # Preparar el cuerpo de Markdown
    body_md = content

    # 1. Eliminar título h1 principal (Dev.to ya lo muestra como cabecera del artículo)
    body_md = re.sub(r"^# .*\n+", "", body_md)

    # 2. Eliminar cabecera '### Entrada del diario:' si estuviera presente
    body_md = re.sub(r"### Entrada del diario:\s*\n+", "", body_md, flags=re.IGNORECASE)

    # 3. Eliminar la imagen de cabecera si ya la estamos usando como cover_image
    if dia_num is not None:
        body_md = re.sub(
            rf'<img[^>]*src=["\']\./diario-images/day-{dia_num}\.png["\'][^>]*>\s*\n*',
            "",
            body_md,
            flags=re.IGNORECASE,
        )
        body_md = re.sub(
            rf'!\[.*?\]\(\./diario-images/day-{dia_num}\.png\)\s*\n*',
            "",
            body_md,
            flags=re.IGNORECASE,
        )

    # 4. Transformar cualquier otra imagen relativa a URLs públicas de GitHub
    body_md = re.sub(
        r'src="\./diario-images/([^"]+)"',
        rf'src="{GITHUB_RAW_BASE}diario-images/\1"',
        body_md,
    )
    body_md = re.sub(
        r'!\[(.*?)\]\(\./diario-images/([^)]+)\)',
        rf'![\1]({GITHUB_RAW_BASE}diario-images/\2)',
        body_md,
    )

    # 5. Transformar enlaces relativos al repositorio a URLs absolutas de GitHub
    def replace_relative_link(match):
        text = match.group(1)
        rel_url = match.group(2)
        if rel_url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        clean_path = re.sub(r"^(\.\./)+", "", rel_url).lstrip("./")
        target_base = GITHUB_REPO_BLOB if "." in Path(clean_path).name else GITHUB_REPO_TREE
        return f"[{text}]({target_base}{clean_path})"

    body_md = re.sub(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)', replace_relative_link, body_md)

    # Canonical URL apuntando al archivo en Buttondown si existe
    canonical_url = f"https://buttondown.com/chaconmoon/archive/decompilando-en-358-dias-dia-{dia_num}/" if dia_num else None

    return {
        "title": title,
        "body_markdown": body_md.strip(),
        "published": False,  # Estrictamente BORRADOR
        "series": "Decompilando en 358 Días",
        "main_image": cover_image,
        "canonical_url": canonical_url,
        "tags": tags,
    }


def find_existing_article_id(api_key, title):
    """Busca si ya existe un artículo con este título para actualizarlo (PUT) en lugar de duplicarlo."""
    headers = {
        "api-key": api_key,
        "User-Agent": "Decomp358-Publisher/1.0",
    }
    try:
        req = urllib.request.Request(f"{DEVTO_API_URL}/me/all?per_page=100", headers=headers)
        with urllib.request.urlopen(req) as resp:
            articles = json.loads(resp.read().decode("utf-8"))
            for a in articles:
                if a.get("title") == title:
                    return a.get("id")
    except Exception:
        pass
    return None


def upload_to_devto(api_key, article_payload):
    """Envía el artículo a Dev.to mediante POST (crear) o PUT (actualizar)."""
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "Decomp358-Publisher/1.0",
    }

    existing_id = find_existing_article_id(api_key, article_payload["title"])
    data = json.dumps({"article": article_payload}).encode("utf-8")

    if existing_id:
        url = f"{DEVTO_API_URL}/{existing_id}"
        req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
        action = "actualizado"
    else:
        req = urllib.request.Request(DEVTO_API_URL, data=data, headers=headers, method="POST")
        action = "creado"

    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            return resp_data, action
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ Error HTTP {e.code} desde Dev.to: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error de conexión: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_arguments()
    api_key = get_api_key()

    if not api_key:
        print("❌ Error: No se encontró DEVTO_API_KEY en .env ni en las variables de entorno.")
        sys.exit(1)

    dia_num = args.dia
    if args.archivo:
        target_path = Path(args.archivo)
        if dia_num is None:
            match = re.search(r"dia-(\d+)\.md", target_path.name)
            if match:
                dia_num = int(match.group(1))
    elif dia_num is not None:
        target_path = DIARIO_DIR / f"dia-{dia_num}.md"
    else:
        print("❌ Error: Debes especificar --dia [N] o --archivo [ruta].")
        sys.exit(1)

    if not target_path.exists():
        print(f"❌ Error: El archivo {target_path} no existe.")
        sys.exit(1)

    print(f"📖 Leyendo entrada: {target_path.relative_to(REPO_ROOT)}")
    content = target_path.read_text(encoding="utf-8")
    article = prepare_devto_article(content, dia_num=dia_num)

    print(f"📬 Título: '{article['title']}'")
    print(f"🏷️ Tags: {article['tags']}")
    print(f"📚 Serie: '{article['series']}'")
    print(f"🖼️ Cover Image: {article['main_image']}")
    print("📝 Subiendo a Dev.to en modo BORRADOR (draft)...")

    result, action = upload_to_devto(api_key, article)

    art_id = result.get("id")
    url = result.get("url")

    print(f"\n✅ ¡Borrador {action} exitosamente en Dev.to!")
    print(f"   🆔 ID: {art_id}")
    print(f"   📌 Estado: Draft (No publicado)")
    print(f"   🔗 URL previa: {url}")
    print(f"\n👉 Revisa y edita tu borrador cómodamente desde:")
    print(f"   https://dev.to/dashboard")


if __name__ == "__main__":
    main()
