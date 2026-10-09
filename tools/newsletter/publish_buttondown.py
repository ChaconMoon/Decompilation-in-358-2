#!/usr/bin/env python3
"""
tools/newsletter/publish_buttondown.py

Publicador automatizado de entradas del diario en Buttondown como borradores (drafts).
Lee la API Key desde el archivo .env o la variable BUTTONDOWN_API_KEY.

Uso:
    python3 tools/newsletter/publish_buttondown.py --dia 1
    python3 tools/newsletter/publish_buttondown.py --archivo docs/diario/dia-1.md
    python3 tools/newsletter/publish_buttondown.py --dia 1 --status draft
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
        description="Publica una entrada del diario en Buttondown como borrador."
    )
    parser.add_argument("--dia", type=int, help="Número de día del diario (ej: 1)")
    parser.add_argument("--archivo", type=str, help="Ruta al archivo Markdown")
    parser.add_argument(
        "--status",
        type=str,
        default="draft",
        choices=["draft", "about_to_send"],
        help="Estado del email en Buttondown (default: draft)",
    )
    parser.add_argument(
        "--solo-web",
        action="store_true",
        help="Publica el artículo exclusivamente en el archivo web público sin enviar correos a los suscriptores.",
    )
    return parser.parse_args()


def extract_metadata_and_body(content):
    """Extrae título, tags y compila Markdown a HTML semántico compatible con Buttondown."""
    import markdown

    lines = content.splitlines()
    subject = "Diario de decompilación"
    for line in lines:
        if line.startswith("# "):
            subject = line[2:].strip()
            break

    tags = []
    tags_match = re.search(r"### Tags:\s*\n([^\n#]*#.*)", content)
    if tags_match:
        tag_line = tags_match.group(1)
        tags = [t.lstrip("#") for t in re.findall(r"#([\w-]+)", tag_line)]

    # 1. Eliminar título h1 redundante del cuerpo (Buttondown ya lo muestra como asunto del email)
    body_md = re.sub(r"^# .*\n+", "", content)

    # 2. Transformar rutas relativas de imágenes a URLs públicas raw de GitHub
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

    # 3. Transformar checkboxes de GFM a elementos visuales universales para email
    body_md = re.sub(r"^- \[x\] ", "- ✅ ", body_md, flags=re.M)
    body_md = re.sub(r"^- \[ \] ", "- ⬜ ", body_md, flags=re.M)

    # 4. Formatear tags como badges elegantes
    def format_tags(match):
        tags_str = match.group(1).strip()
        found_tags = re.findall(r"#([\w-]+)", tags_str)
        badges = [
            f'<span style="background:#eef2ff; color:#3730a3; padding:3px 10px; border-radius:12px; font-family:sans-serif; font-size:0.85em; margin-right:6px; display:inline-block;">#{t}</span>'
            for t in found_tags
        ]
        return "### Tags:\n\n" + " ".join(badges)

    body_md = re.sub(r"### Tags:\s*\n([^\n]+)", format_tags, body_md)

    # 5. Compilar a HTML limpio
    html_output = markdown.markdown(body_md, extensions=["extra", "sane_lists"])

    return subject, tags, html_output


def publish_to_buttondown(api_key, subject, body, tags, status="draft", solo_web=False):
    """Envía el email a la API de Buttondown. Si solo_web es True, se publica sin enviar correo."""
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Decomp358-Publisher/1.0",
    }

    payload = {
        "subject": subject,
        "body": body,
        "status": status,
    }
    if solo_web:
        payload["archival_mode"] = "archive_only"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BUTTONDOWN_API_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            
            # Si se solicitó publicar exclusivamente en la web, ejecutar la transición de publicación
            if solo_web:
                email_id = resp_data.get("id")
                publish_url = f"{BUTTONDOWN_API_URL}/{email_id}/publish"
                pub_req = urllib.request.Request(publish_url, data=json.dumps({}).encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(pub_req) as pub_resp:
                    resp_data = json.loads(pub_resp.read().decode("utf-8"))
                    
            return resp_data
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

    if args.archivo:
        target_path = Path(args.archivo)
    elif args.dia is not None:
        target_path = DIARIO_DIR / f"dia-{args.dia}.md"
    else:
        print("❌ Error: Debes especificar --dia [N] o --archivo [ruta].")
        sys.exit(1)

    if not target_path.exists():
        print(f"❌ Error: El archivo {target_path} no existe.")
        sys.exit(1)

    print(f"📖 Leyendo entrada: {target_path.relative_to(REPO_ROOT)}")
    content = target_path.read_text(encoding="utf-8")
    subject, tags, body = extract_metadata_and_body(content)

    print(f"📬 Asunto: '{subject}'")
    print(f"🏷️ Tags: {tags}")
    if args.solo_web:
        print("🌐 Modo: Publicación EXCLUSIVA EN WEB (sin enviar emails a suscriptores)...")
    else:
        print(f"🚀 Enviando a Buttondown con estado: '{args.status}'...")

    result = publish_to_buttondown(api_key, subject, body, tags, status=args.status, solo_web=args.solo_web)

    email_id = result.get("id", "Desconocido")
    slug = result.get("slug", "")
    public_url = result.get("absolute_url", f"https://buttondown.com/chaconmoon/archive/{slug}/")

    if args.solo_web:
        print("\n🎉 ¡Publicación en la web completada con éxito!")
        print(f"   🆔 ID: {email_id}")
        print(f"   🌐 Estado: Publicado en archivo web (Sin envíos por correo)")
        print(f"   🔗 URL Pública en vivo: {public_url}")
    else:
        print("\n✅ ¡Borrador creado exitosamente en Buttondown!")
        print(f"   🆔 ID: {email_id}")
        print(f"   🔗 Estado: {result.get('status', 'draft')}")
        if slug:
            print(f"   📝 Slug: {slug}")
        print(f"   👉 Puedes revisarlo en tu panel de Buttondown: https://buttondown.com/emails")


if __name__ == "__main__":
    main()
