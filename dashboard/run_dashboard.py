"""Launch the HuaGou Mall E-Commerce Analytics Dashboard.

Runs a lightweight local HTTP server and automatically opens the dashboard
in the default web browser.
"""

import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

PORT = 8080
DASHBOARD_DIR = Path(__file__).resolve().parent


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def log_message(self, format, *args):
        # Suppress routine log output for a cleaner console
        pass


def run():
    print("=" * 65)
    print("  🛍️ HuaGou Mall E-Commerce Interactive Analytics Dashboard")
    print("=" * 65)
    print(f"\nServing dashboard at: http://localhost:{PORT}/index.html")
    print("Opening your default browser...")
    print("Press Ctrl+C in this terminal to stop the server.\n")

    try:
        webbrowser.open(f"http://localhost:{PORT}/index.html")
    except Exception:
        pass

    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] Dashboard server stopped cleanly.")
    except OSError as e:
        if "address already in use" in str(e).lower() or e.errno == 98 or e.errno == 10048:
            alt_port = 8081
            print(f"[NOTE] Port {PORT} is busy, trying port {alt_port}...")
            with socketserver.TCPServer(("", alt_port), DashboardHandler) as httpd:
                webbrowser.open(f"http://localhost:{alt_port}/index.html")
                httpd.serve_forever()
        else:
            raise


if __name__ == "__main__":
    run()
