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
    return parser.parse_args()


def extract_metadata_and_body(content):
    """Extrae título, tags y adapta rutas de imágenes locales a GitHub raw."""
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

    # Transformar rutas relativas de imágenes locales a raw de GitHub para que carguen en el correo
    transformed_content = re.sub(
        r'src="\./diario-images/([^"]+)"',
        rf'src="{GITHUB_RAW_BASE}diario-images/\1"',
        content,
    )
    transformed_content = re.sub(
        r'!\[(.*?)\]\(\./diario-images/([^)]+)\)',
        rf'![\1]({GITHUB_RAW_BASE}diario-images/\2)',
        transformed_content,
    )

    return subject, tags, transformed_content


def publish_to_buttondown(api_key, subject, body, tags, status="draft"):
    """Envía el borrador a la API de Buttondown."""
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

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BUTTONDOWN_API_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
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
    print(f"🚀 Enviando a Buttondown con estado: '{args.status}'...")

    result = publish_to_buttondown(api_key, subject, body, tags, status=args.status)

    email_id = result.get("id", "Desconocido")
    slug = result.get("slug", "")
    print("\n✅ ¡Borrador creado exitosamente en Buttondown!")
    print(f"   🆔 ID: {email_id}")
    print(f"   🔗 Estado: {result.get('status', 'draft')}")
    if slug:
        print(f"   📝 Slug: {slug}")
    print(f"   👉 Puedes revisarlo en tu panel de Buttondown: https://buttondown.com/emails")


if __name__ == "__main__":
    main()
