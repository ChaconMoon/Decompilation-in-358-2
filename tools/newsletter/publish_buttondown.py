#!/usr/bin/env python3
"""
tools/newsletter/publish_buttondown.py

Sube entradas del diario a Buttondown como borradores (drafts) para revisión manual.
- Slugs configurados automáticamente para terminar en -dia-N.
- Modo archival_mode: archive_only (al publicarse manualmente en la web, no envía emails).
- NUNCA publica automáticamente: solo el autor pulsa 'Publish' desde el panel web.

Uso:
    python3 tools/newsletter/publish_buttondown.py --dia 13
    python3 tools/newsletter/publish_buttondown.py --archivo docs/diario/dia-13.md
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
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ChaconMoon/Decompilation-in-358-2/master/docs/diario/"
GITHUB_REPO_BLOB = "https://github.com/ChaconMoon/Decompilation-in-358-2/blob/master/"
GITHUB_REPO_TREE = "https://github.com/ChaconMoon/Decompilation-in-358-2/tree/master/"
BUTTONDOWN_API_URL = "https://api.buttondown.email/v1/emails"


def get_api_key():
    """Obtiene la API key desde .env o el entorno."""
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("BUTTONDOWN_API_KEY"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")

    key = os.environ.get("BUTTONDOWN_API_KEY")
    if key:
        return key.strip().strip('"').strip("'")

    return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sube una entrada del diario a Buttondown como borrador (draft) para revisión manual."
    )
    parser.add_argument("--dia", type=int, help="Número de día del diario (ej: 1)")
    parser.add_argument("--archivo", type=str, help="Ruta al archivo Markdown")
    return parser.parse_args()


def extract_metadata_and_body(content, dia_num=None):
    """Extrae título, tags, slug y compila Markdown a HTML semántico compatible con Buttondown."""
    import markdown

    lines = content.splitlines()
    subject = "Diario de decompilación"
    for line in lines:
        if line.startswith("# "):
            subject = line[2:].strip()
            break

    # Si no se pasó dia_num, intentar extraerlo del asunto o del texto
    if dia_num is None:
        dia_match = re.search(r"Dia\s+(\d+)", subject, re.IGNORECASE)
        if dia_match:
            dia_num = int(dia_match.group(1))

    slug = f"decompilando-en-358-dias-dia-{dia_num}" if dia_num is not None else None

    tags = []
    tags_match = re.search(r"### Tags:\s*\n([^\n#]*#.*)", content)
    if tags_match:
        tag_line = tags_match.group(1)
        tags = [t.lstrip("#") for t in re.findall(r"#([\w-]+)", tag_line)]

    # 1. Eliminar título h1 redundante del cuerpo (Buttondown ya lo muestra como asunto del email)
    body_md = re.sub(r"^# .*\n+", "", content)

    # 2. Eliminar cabecera redundante '### Entrada del diario:' manteniendo la parte de Info
    body_md = re.sub(r"### Entrada del diario:\s*\n+", "", body_md, flags=re.IGNORECASE)

    # 3. Transformar rutas relativas de imágenes a URLs públicas raw de GitHub
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

    # 4. Transformar enlaces relativos al repositorio a URLs absolutas de GitHub
    def replace_relative_link(match):
        text = match.group(1)
        rel_url = match.group(2)
        if rel_url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        clean_path = re.sub(r"^(\.\./)+", "", rel_url).lstrip("./")
        target_base = GITHUB_REPO_BLOB if "." in Path(clean_path).name else GITHUB_REPO_TREE
        return f"[{text}]({target_base}{clean_path})"

    body_md = re.sub(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)', replace_relative_link, body_md)

    # 5. Transformar checkboxes de GFM a elementos visuales universales para email
    body_md = re.sub(r"^- \[x\] ", "- ✅ ", body_md, flags=re.M)
    body_md = re.sub(r"^- \[ \] ", "- ⬜ ", body_md, flags=re.M)

    # 5. Formatear tags como badges elegantes
    def format_tags(match):
        tags_str = match.group(1).strip()
        found_tags = re.findall(r"#([\w-]+)", tags_str)
        badges = [
            f'<span style="background:#eef2ff; color:#3730a3; padding:3px 10px; border-radius:12px; font-family:sans-serif; font-size:0.85em; margin-right:6px; display:inline-block;">#{t}</span>'
            for t in found_tags
        ]
        return "### Tags:\n\n" + " ".join(badges)

    body_md = re.sub(r"### Tags:\s*\n([^\n]+)", format_tags, body_md)

    # 6. Compilar a HTML limpio
    html_output = markdown.markdown(body_md, extensions=["extra", "sane_lists"])

    return subject, tags, html_output, slug


def upload_draft_to_buttondown(api_key, subject, body, tags, slug=None):
    """
    Sube o actualiza la entrada en Buttondown estrictamente como BORRADOR (draft).
    Configura archival_mode: archive_only para que, al publicarse manualmente desde la web,
    no envíe correos electrónicos a los suscriptores. NUNCA publica de forma automática.
    """
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Decomp358-Publisher/1.0",
    }

    # 1. Comprobar si ya existe una entrada con ese slug para actualizarla (PATCH) en lugar de duplicarla
    existing_id = None
    existing_status = None
    if slug:
        try:
            req = urllib.request.Request(BUTTONDOWN_API_URL, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("results", []):
                    if item.get("slug") == slug:
                        existing_id = item.get("id")
                        existing_status = item.get("status")
                        break
        except Exception:
            pass

    payload = {
        "subject": subject,
        "body": body,
        "archival_mode": "archive_only",
    }
    if slug:
        payload["slug"] = slug

    # Si la entrada ya estaba publicada ('sent'), Buttondown rechaza pasarla a 'draft'.
    # Si es borrador o creación nueva, se asegura el estado 'draft'.
    if existing_status != "sent":
        payload["status"] = "draft"

    data = json.dumps(payload).encode("utf-8")

    if existing_id:
        url = f"{BUTTONDOWN_API_URL}/{existing_id}"
        req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
        action = "actualizado"
    else:
        req = urllib.request.Request(BUTTONDOWN_API_URL, data=data, headers=headers, method="POST")
        action = "creado"

    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            return resp_data, action
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ Error HTTP {e.code} desde Buttondown: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error de conexión: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_arguments()
    api_key = get_api_key()

    if not api_key:
        print("❌ Error: No se encontró BUTTONDOWN_API_KEY en .env ni en las variables de entorno.")
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
    subject, tags, body, slug = extract_metadata_and_body(content, dia_num=dia_num)

    print(f"📬 Asunto: '{subject}'")
    print(f"🏷️ Tags: {tags}")
    if slug:
        print(f"🔗 Slug configurado: '{slug}' (termina en -dia-{dia_num})")
    print("📝 Subiendo a Buttondown en modo BORRADOR (draft)...")

    result, action = upload_draft_to_buttondown(api_key, subject, body, tags, slug=slug)

    email_id = result.get("id", "Desconocido")
    res_slug = result.get("slug", slug or "")

    print(f"\n✅ ¡Borrador {action} exitosamente en Buttondown!")
    print(f"   🆔 ID: {email_id}")
    print(f"   📌 Estado: draft (Borrador protegido)")
    print(f"   🌐 Archival Mode: archive_only (Al publicarse solo irá a la web, sin emails)")
    print(f"   🔗 Slug: {res_slug}")
    print(f"   🌐 URL futura al publicar: https://buttondown.com/chaconmoon/archive/{res_slug}/")
    print(f"\n👉 Revisa y pulsa 'Publish' manualmente cuando quieras desde:")
    print(f"   https://buttondown.com/emails")


if __name__ == "__main__":
    main()
