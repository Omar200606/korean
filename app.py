import http.server
import os
import threading
import time


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def serve(port):
    try:
        srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
    except OSError:
        print(f"Port {port} is busy, skipped")
        return
    print(f"Serving on port {port}")
    srv.serve_forever()


ports = set()
for var in ("PORT", "WEB_PORT", "APP_PORT", "HTTP_PORT", "SERVER_PORT", "LISTEN_PORT"):
    val = os.environ.get(var)
    if val and val.isdigit():
        ports.add(int(val))
ports.update((8080, 8000, 3000, 5000, 80))

for p in sorted(ports):
    threading.Thread(target=serve, args=(p,), daemon=True).start()

print(f"Listening on ports: {sorted(ports)}")
while True:
    time.sleep(3600)
