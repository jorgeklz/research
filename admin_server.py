#!/usr/bin/env python3
"""
Servidor local para el sitio + panel de administración (admin.html).

Se usa exactamente igual que `python3 -m http.server`, pero además entiende
dos rutas especiales que admin.html usa para guardar cambios de verdad en
disco (funciona en cualquier navegador, no necesita nada especial):

    GET  /api/ping      -> {"ok": true}                (para saber si este server está corriendo)
    POST /api/posts     -> escribe el body en data/posts.json
    POST /api/profile   -> escribe el body en data/profile.json

Cada guardado hace antes una copia de respaldo (data/posts.json.bak, etc.)
por si algo sale mal.

Uso:
    cd ~/Claude/Projects/WebSiteResearch/investigador-web
    python3 admin_server.py
    (abre http://localhost:8000/admin.html — o /index.html para ver el sitio)

Esto es SOLO para edición local. El sitio publicado en GitHub Pages sigue
siendo estático de siempre; después de guardar, sigue haciendo falta
`git add -A && git commit -m "..." && git push` para publicar los cambios.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

SAVE_ENDPOINTS = {
    "/api/posts": DATA_DIR / "posts.json",
    "/api/profile": DATA_DIR / "profile.json",
}


class Handler(BaseHTTPRequestHandler):
    # serve static files from ROOT, same behaviour as `python3 -m http.server`
    def translate_path(self, path):
        import posixpath
        import urllib.parse
        path = path.split("?", 1)[0].split("#", 1)[0]
        path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        parts = [p for p in path.split("/") if p and p != ".."]
        return str(ROOT.joinpath(*parts)) if parts else str(ROOT)

    def _json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _static_file(self):
        target = Path(self.translate_path(self.path))
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return
        ctype = {
            ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
            ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".ico": "image/x-icon", ".webp": "image/webp",
        }.get(target.suffix.lower(), "application/octet-stream")
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/ping"):
            return self._json(200, {"ok": True})
        return self._static_file()

    def do_POST(self):
        target = SAVE_ENDPOINTS.get(self.path.split("?", 1)[0])
        if not target:
            return self._json(404, {"ok": False, "error": "endpoint desconocido"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            parsed = json.loads(raw.decode("utf-8"))
            if not isinstance(parsed, dict):
                raise ValueError("se esperaba un objeto JSON")

            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = target.with_name(target.name + ".bak")
                backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")

            target.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  guardado: {target.relative_to(ROOT)}")
            self._json(200, {"ok": True})
        except Exception as e:
            print(f"  ERROR guardando {target}: {e}", file=sys.stderr)
            self._json(500, {"ok": False, "error": str(e)})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    ThreadingHTTPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Sirviendo {ROOT}")
        print(f"Sitio:  http://localhost:{PORT}/index.html")
        print(f"Admin:  http://localhost:{PORT}/admin.html")
        print("Ctrl+C para salir\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
