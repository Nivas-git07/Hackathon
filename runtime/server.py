from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        requested = self.path.split("?", 1)[0]
        if requested != "/" and "." not in Path(requested).name:
            self.path = "/index.html"
        super().do_GET()

    def log_message(self, fmt, *args):
        print(f"[runtime] {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    port = int(os.environ.get("ECOMIND_RUNTIME_PORT", "4173"))
    server = ThreadingHTTPServer(("127.0.0.1", port), SpaHandler)
    print(f"EcoMind runtime listening on http://127.0.0.1:{port}")
    server.serve_forever()
